# Photo Renamer

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/EvgeniyKuzmin/photo-renamer)
![PyPI](https://img.shields.io/pypi/v/photo-renamer)
[![Python 3.6+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![codecov](https://codecov.io/gh/EvgeniyKuzmin/photo-renamer/branch/master/graph/badge.svg?token=H5VYO0JKPS)](https://codecov.io/gh/EvgeniyKuzmin/photo-renamer)


## Description
Enables you making collections of unique photos or videos with names are formatted by a specific template.

Renamer does it by executing the following actions:
- Iterating over the source and searching for files according with a preset extensions.
- Checking file uniqueness using SHA-256 comparison.
- Extracting time of creation from a file's attributes (metadata or filename).
- Generating a new name for a file, and applying it to a existed or a new one file.


## Usage

### Installation

#### From PyPI
    $ pip install photo_renamer

#### From source code
    $ git clone https://github.com/EvgeniyKuzmin/photo-renamer.git
    $ cd photo-renamer
    $ pip install .

### Help message
```
usage: photo-renamer [-h] [-t TEMPLATE] [-e EXT [EXT ...]] [-d DEST] [-c | -r] [-m | -n | -a] [-1 | -2 | -3 | -4] SOURCE

positional arguments:
  SOURCE                A path to a source directory or a file

optional arguments:
  -h, --help            show this help message and exit
  -t TEMPLATE, --template TEMPLATE
                        Template for file naming based on time of creation
  -e EXT [EXT ...], --extensions EXT [EXT ...]
                        File extensions that are suitable for processing
  -d DEST, --dest DEST  A path to the destination directory (in case of a copy-mode)

mode:
  -c, --copy            COPY mode: make copies of existed files
  -r, --rename          RENAME mode: rename existed files

extraction mode:
  -m, --meta            Extract a date from a metadata only
  -n, --name            Extract a date from a filename only
  -a, --all             Extract a date via all available methods

logging:
  -1, --debug           Set DEBUG level
  -2, --info            Set INFO level
  -3, --warning         Set WARNING level
  -4, --error           Set ERROR level
```

### Versioning
The package follows [Semantic Versioning](http://semver.org) and [PEP440](https://www.python.org/dev/peps/pep-0440/). Given a version number MAJOR.MINOR.PATCH, increment the:
- MAJOR version when you make incompatible API changes,
- MINOR version when you add functionality in a backwards compatible manner, and
- PATCH version when you make backwards compatible bug fixes.


## Contribution

### Testing

#### Installation for testing
    $ pip install -e .[test]

#### Run tests
    $ flake8
    $ coverage run -m pytest
    $ coverage report -m

### Installation for distributing
    $ pip install -e .[dist]

#### Upload a release to PyPI
    $ python setup.py bdist_wheel
    $ twine upload -r testpypi dist/*


## License
Copyright © 2021, [Evgenii Kuzmin](mailto:evgeniy.a.kuzmin@gmail.com).
Released under the [MIT license](LICENSE).
