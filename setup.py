""" This file contains the package setup

:author: Daniel Seifert
:created: 09.09.2021
:copyright: Swisscom
"""
from pathlib import Path

from setuptools import setup

PROJECT_DIR = Path(__file__).resolve().parent

ABOUT_PATH = PROJECT_DIR / "qlient" / "__about__.py"
README_PATH = PROJECT_DIR / "README.md"
REQUIREMENTS_PATH = PROJECT_DIR / "requirements.txt"
TEST_REQUIREMENTS_PATH = PROJECT_DIR / "requirements.test.txt"


def read_about() -> dict:
    """ Load the qlient/__about__.py globals into the about variable defined below

    :return: the globals from the __about__.py file
    """
    about = {}
    exec(ABOUT_PATH.read_text(encoding="UTF-8"), about)
    return about


def read_requirements_file(req_file_path: Path) -> list:
    """ Read and split the content of a requirements file

    :param req_file_path: holds the path to the requirements file
    :return: a list of strings with the requirements
    """
    content = req_file_path.read_text(encoding="UTF-8")
    return content.splitlines()


ABOUT = read_about()
README = README_PATH.read_text(encoding="UTF-8")
INSTALL_REQUIRES = read_requirements_file(REQUIREMENTS_PATH)
TEST_REQUIRES = read_requirements_file(TEST_REQUIREMENTS_PATH)

PACKAGES = ["qlient"]

setup(
    name=ABOUT["__title__"],
    version=ABOUT["__version__"],
    description=ABOUT["__description__"],
    long_description=README,
    long_description_content_type="text/markdown",
    author=ABOUT["__author__"],
    author_email=ABOUT["__author_email__"],
    url=ABOUT["__url__"],
    packages=PACKAGES,
    package_data={"": ["LICENSE"]},
    package_dir={"qlient": "qlient"},
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    test_requires=TEST_REQUIRES,
    license=ABOUT["__license__"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    project_urls={
        "Documentation": ABOUT["__url__"],
        "Source": ABOUT["__source__"],
    },
)
