![pypi-badge](https://img.shields.io/pypi/v/lscom) ![pypi-format](https://img.shields.io/pypi/format/lscom) ![pypi-implementation](https://img.shields.io/pypi/implementation/lscom) ![pypi-version](https://img.shields.io/pypi/pyversions/lscom) [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](https://github.com/joshschmelzle/lscom/blob/main/CODE_OF_CONDUCT.md)

# lscom: list and discover available COM ports

More quickly identify which COM ports are available for use. Any COM ports already in use will not be listed. `lscom` should work cross platform (Linux, macOS, Windows), but has not been extensively tested. Have a problem? Open an issue.

## Usage Example

```
$ lscom
['COM3']
```

## Installation from PyPI

```bash
python -m pip install lscom
```

## Local Installation Example

To install manually:

1. Clone repository.

2. Open the terminal to the root of the repository.

3. Run-

```bash
python -m pip install .
```

You should now be able to run `lscom` from your terminal

If you can't, check and make sure the scripts directory is included in the system path environment variable.

To remove:

```bash
python -m pip uninstall lscom
```
