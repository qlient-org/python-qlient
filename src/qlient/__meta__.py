"""This file contains the metadata information about this python package.

Attributes:
    __title__: holds the name of the package
    __description__: holds a brief summary of this package
    __url__: holds the url to the git repository
    __version__: holds the currently installed version of this package
    __author__: holds the name of the package author
    __author_email__: holds the email address of the author
"""
try:
    from importlib import metadata as imp_meta
except ImportError:
    import importlib_metadata as imp_meta

qlient_metadata: imp_meta.PackageMetadata = imp_meta.metadata("qlient")

__title__: str = qlient_metadata.json["name"]
__description__: str = qlient_metadata.json["summary"]
__url__: str = qlient_metadata.json["home_page"]
__version__: str = qlient_metadata.json["version"]
__author__: str = qlient_metadata.json["author"]
__author_email__: str = qlient_metadata.json["author_email"]
