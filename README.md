# Photo Renamer

## Description
Enables you making collections of unique JPEG-photos with names are formatted by a specific template.

Renamer does it by executing the following actions:
- Iterating over the source and searching for JPEG-files.
- Checking file uniqueness using SHA-256 comparison.
- Extracting time of creation from a file's attributes (metadata or filename).
- Generating a new name for a file, and applying it to a existed or a new one file.

## Usage
```
usage: photo-renamer [-h] [-c] [-r] [-t TEMPLATE] [-d DEST] [-m] [-1] [-2] [-3] [-4] SOURCE

positional arguments:
  SOURCE                A path to a source directory or a file

optional arguments:
  -h, --help            show this help message and exit
  -t TEMPLATE, --template TEMPLATE
                        Template for file naming based on time of creation
  -d DEST, --dest DEST  A path to the destination directory (in case of a copy-mode)
  -m, --meta            Extract file's date from metadata only

mode:
  -c, --copy            COPY mode: make copies of existed files
  -r, --rename          RENAME mode: rename existed files

logging:
  -1, --debug           Set DEBUG level
  -2, --info            Set INFO level
  -3, --warning         Set WARNING level
  -4, --error           Set ERROR level
```

## Installation
### For usage
    $ pip install .

### For development
    $ pip install -e .[dev]


## Testing
    $ flake8
    $ coverage run -m pytest
    $ coverage report -m


## License
Copyright © 2021, [Evgenii Kuzmin](mailto:evgeniy.a.kuzmin@gmail.com).
Released under the [MIT license](LICENSE).
