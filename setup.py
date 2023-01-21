# -*- coding: utf-8 -*-

import os
import sys

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# 'python setup.py build' shortcut
if sys.argv[-1] == "build":
    os.system("python setup.py sdist bdist_wheel")
    sys.exit()

# 'python setup.py check' shortcut
if sys.argv[-1] == "check":
    os.system("python -m twine check dist/*")
    sys.exit()

# 'python setup.py deploy' shortcut
if sys.argv[-1] == "deploy":
    os.system("python -m twine upload dist/*")
    sys.exit()
    
# load the package's __version__.py module as a dictionary
about = {}
with open(os.path.join(here, "lscom", "__version__.py")) as f:
    exec(f.read(), about)

try:
    with open("README.md", "r") as f:
        readme = f.read()
except FileNotFoundError:
    long_description = about["__description__"]

requires = ["pyserial"]

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    keywords=["com", "com ports", "serial"],
    python_requires=">3.2,",
    license=about["__license__"],
    classifiers=[
        "Natural Language :: English",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.2",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Utilities",
    ],
    packages=find_packages(
        exclude=(
            "tests",
            "test",
        )
    ),
    install_requires=requires,
    entry_points={"console_scripts": ["lscom=lscom.__main__:main"]},
)
