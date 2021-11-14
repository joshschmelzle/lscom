# PUBLISHING.md

## depends

```shell
python -m pip install -U pip wheel setuptools twine
```

## build

Create source archive and wheel:

```shell
python setup.py sdist bdist_wheel
```

## test

Check output with twine

```shell
python -m twine check dist/*
```

## deploy

Uploading to production PyPI:

```shell
python -m twine upload dist/*
```

Enter your username and password when requested.