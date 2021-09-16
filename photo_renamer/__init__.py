"""Photo Renamer.

Enables you making collections of unique photos or videos with names are formatted by a specific template.

Renamer does it by executing the following actions:
- Iterating over the source and searching for files according with a preset extensions.
- Checking file uniqueness using SHA-256 comparison.
- Extracting time of creation from a file's attributes (metadata or filename).
- Generating a new name for a file, and applying it to a existed or a new one file.
"""

__version__ = '0.2.0'
__author__ = 'Evgeniy Kuzmin'
__email__ = 'evgeniy.a.kuzmin@gmail.com'
