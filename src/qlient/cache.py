""" This file contains different caching mechanisms for the qlient library

:author: Daniel Seifert
:created: 09.09.2021
"""
from typing import Optional, Dict


class Cache:
    """ Base class for caching """

    def put(self, url: str, content: Dict):
        """ Put something in the cache """
        raise NotImplementedError()

    def get(self, url: str) -> Optional[Dict]:
        """ Get something from the cache """
        raise NotImplementedError()


class InMemoryCache(Cache):
    """ Cache that holds objects only in memory. """

    cache = {}  # global cache, thread-safe by default

    def put(self, url: str, content: Dict):
        """ Store the given schema in memory for later usage that can be referenced by url.

        :param url: holds the url
        :param content: hols the raw graphql schema
        """
        self.cache[url] = content
        return None

    def get(self, url) -> Optional[Dict]:
        """

        :param url:
        :return:
        """
        return self.cache.get(url)

    def __str__(self) -> str:
        """ Return a simple string representation of this instance """
        class_name = self.__class__.__name__
        return f"{class_name}(items={len(self.cache)})"

    def __repr__(self) -> str:
        """ Return a more detailed string representation of this instance """
        class_name = self.__class__.__name__
        return f"<{class_name}(cache={self.cache})>"
