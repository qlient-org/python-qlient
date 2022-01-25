""" This file contains different caching mechanisms for the qlient library

:author: Daniel Seifert
:created: 09.09.2021
"""
import base64
import collections.abc
import datetime
import errno
import json
import logging
import os
import sqlite3
import threading
import time
from contextlib import contextmanager
from typing import Iterator, Optional, Tuple, Union

import platformdirs

from qlient.schema.types import RawSchema

logger = logging.getLogger("qlient")


class Cache(collections.abc.MutableMapping):
    """ Base class for caching """

    def __setitem__(self, url: str, schema: RawSchema):
        raise NotImplementedError()

    def __delitem__(self, url: str):
        raise NotImplementedError()

    def __getitem__(self, url: str) -> RawSchema:
        raise NotImplementedError()

    def __len__(self) -> int:
        raise NotImplementedError()

    def __iter__(self) -> Iterator[Tuple[str, RawSchema]]:
        raise NotImplementedError()

    def __missing__(self, url: str):
        raise KeyError(f"URL `{url}` not in cache")


class InMemoryCache(Cache):
    __memory__ = {}

    def __setitem__(self, url: str, schema: RawSchema):
        logger.debug(f"In-Memory caching schema for url `{url}`")
        self.__memory__.__setitem__(url, schema)

    def __delitem__(self, url: str):
        logger.debug(f"In-Memory deleting schema for url `{url}`")
        self.__memory__.__delitem__(url)

    def __getitem__(self, url: str) -> RawSchema:
        logger.debug(f"In-Memory getting schema for url `{url}`")
        return self.__memory__.__getitem__(url)

    def __len__(self) -> int:
        logger.debug(f"In-Memory counting records")
        return self.__memory__.__len__()

    def __iter__(self) -> Iterator[Tuple[str, RawSchema]]:
        logger.debug(f"In-Memory iterating records")
        return self.__memory__.__iter__()


def _get_default_sqlite_cache_dir() -> str:
    path_to_cache_dir = platformdirs.user_cache_dir("qlient", False)

    try:
        os.makedirs(path_to_cache_dir)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path_to_cache_dir):
            pass
        else:
            raise e
    return os.path.join(path_to_cache_dir, "schemas.sqlite")


SQLITE_IN_MEMORY = ":memory:"
ONE_HOUR = datetime.timedelta(seconds=3600)


class SqliteCache(Cache):
    TABLE_NAME = "QLIENT_SCHEMA_CACHE"

    TABLE_STMT = f"""
           CREATE TABLE IF NOT EXISTS {TABLE_NAME}
           (
               URL                  TEXT PRIMARY KEY,
               SCHEMA               TEXT,
               TIMESTAMP_CREATED    INTEGER
           )
       """

    INSERT_STMT = f"INSERT INTO {TABLE_NAME} (URL, SCHEMA, TIMESTAMP_CREATED) VALUES (?, ?, ?)"
    DELETE_STMT = f"DELETE FROM {TABLE_NAME} WHERE URL = ?"
    DELETE_EXPIRED_STMT = f"DELETE FROM {TABLE_NAME} WHERE TIMESTAMP_CREATED <= ?"
    SELECT_STMT = f"SELECT SCHEMA, TIMESTAMP_CREATED FROM {TABLE_NAME} WHERE URL = ?"
    LENGTH_STMT = f"SELECT COUNT(URL) AS CACHE_SIZE FROM {TABLE_NAME}"
    ITER_STMT = f"SELECT URL, SCHEMA FROM {TABLE_NAME}"

    @staticmethod
    def _encode_schema(schema: RawSchema) -> str:
        schema_string = json.dumps(schema, ensure_ascii=False)
        return base64.b64encode(schema_string.encode()).decode()

    @staticmethod
    def _decode_schema(encoded_schema: str) -> RawSchema:
        decoded_raw_schema = base64.b64decode(encoded_schema.encode()).decode()
        return json.loads(decoded_raw_schema)

    def __init__(
            self,
            path: Optional[str] = None,
            expires_in: Union[int, datetime.timedelta] = ONE_HOUR
    ):
        """ Initialize a new sqlite cache

        :param path: holds the path of the sqlite db
        :param expires_in: holds either the amount of seconds when it expires or a datetime.timedelta instance
        """
        if path == SQLITE_IN_MEMORY:
            raise ValueError(
                f"The {SqliteCache.__name__} doesn't support {SQLITE_IN_MEMORY} since it is not thread-safe. "
                + "Please use qlient.cache.InMemoryCache()."
            )

        self.path: str = path or _get_default_sqlite_cache_dir()

        if isinstance(expires_in, int):
            expires_in = datetime.timedelta(seconds=expires_in)
        self.expires_in: datetime.timedelta = expires_in
        self.__lock = threading.RLock()

        # preparing the database
        self.create_cache_table_if_not_exists()

    @contextmanager
    def connect(self) -> sqlite3.Connection:
        logger.debug(f"Creating sqlite3 connection to {self.path}")
        with self.__lock:
            connection = sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES)
            yield connection
            connection.close()

    def create_cache_table_if_not_exists(self):
        logger.debug(f"Creating table {self.TABLE_NAME}")
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(self.TABLE_STMT)
            connection.commit()

    def __setitem__(self, url: str, schema: RawSchema):
        logger.debug(f"Sqlite caching schema for url `{url}`")
        encoded_schema = self._encode_schema(schema)

        with self.connect() as connection:
            cursor = connection.cursor()
            # Delete the old record to prevent a duplicate key
            # we do not use the delete function here because we don't want to open another connection
            cursor.execute(self.DELETE_STMT, (url,))
            # Insert the new record into the cache
            cursor.execute(self.INSERT_STMT, (url, encoded_schema, int(time.time())))
            # commit the changes
            connection.commit()

    def __delitem__(self, url: str):
        logger.debug(f"Sqlite deleting schema for url `{url}`")
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(self.DELETE_STMT, (url,))
            connection.commit()

    def __getitem__(self, url: str) -> RawSchema:
        logger.debug(f"Sqlite selecting schema for url `{url}`")
        self.delete_expired_records()
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(self.SELECT_STMT, (url,))
            result_row: Optional[sqlite3.Row] = cursor.fetchone()

        if result_row is None:
            raise self.__missing__(url)

        encoded_schema, timestamp_created = result_row
        if self._is_expired(timestamp_created):
            del self[url]
            raise self.__missing__(url)

        decoded_schema = self._decode_schema(encoded_schema)
        return decoded_schema

    def __len__(self) -> int:
        logger.debug(f"Sqlite counting records in `{self.TABLE_NAME}`")
        self.delete_expired_records()
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(self.LENGTH_STMT)
            result_row = cursor.fetchone()

        return int(result_row[0])

    def __iter__(self) -> Iterator[Tuple[str, RawSchema]]:
        logger.debug(f"Sqlite iterating records in `{self.TABLE_NAME}`")
        self.delete_expired_records()
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(self.ITER_STMT)
            for row in cursor:
                url, encoded_schema = row
                decoded_schema = self._decode_schema(encoded_schema)
                yield url, decoded_schema

    def delete_expired_records(self):
        logger.debug(f"Sqlite deleting expired records")
        with self.connect() as connection:
            cursor = connection.cursor()
            expiry = int(time.time()) - self.expires_in.seconds
            cursor.execute(self.DELETE_EXPIRED_STMT, (expiry,))
            logger.debug(f"Deleted {cursor.rowcount} expired records")
            connection.commit()

    def _is_expired(self, timestamp_created: int) -> bool:
        return int(time.time()) > timestamp_created + self.expires_in.seconds
