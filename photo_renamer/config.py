from argparse import ArgumentParser, Namespace
import logging
from pathlib import Path
from typing import Any


logger = logging.getLogger(__name__)

DEFAULTS = {
    'mode': 'copy',
    'template': '%Y-%m-%d_%H-%M-%S.jpg',
    'meta': False,
    'logging_level': logging.INFO,
    'logging_format': (
        '%(asctime)s[%(levelname).4s]'
        '%(name)s.%(funcName)s:%(lineno)d %(message)s'
    ),
}


def _read_args() -> Namespace:
    """Return a dict with configuration."""
    parser = ArgumentParser(
        prog='photo-renamer',
        description=''
        'Photo Renamer. '
        'Enables you making collections of unique JPEG-photos with names are '
        'formatted by a specific template. '

        'Renamer does it by executing the following actions: '
        '1. Iterating over the source and searching for JPEG-files. '
        '2. Checking file uniqueness using SHA-256 comparison. '
        '3. Extracting time of creation from a file\'s attributes (metadata '
        'or filename). '
        '4. Generating a new name for a file, and applying it to a existed or '
        'a new one file.',
    )
    parser.set_defaults(**DEFAULTS)
    parser.add_argument(
        'source', metavar='SOURCE', type=Path,
        help='A path to a source directory or a file',
    )

    mode_group = parser.add_argument_group('mode')
    mode_group.add_argument(
        '-c', '--copy', dest='mode', const='copy', action='store_const',
        help='COPY mode: make copies of existed files',
    )
    mode_group.add_argument(
        '-r', '--rename', dest='mode', const='rename', action='store_const',
        help='RENAME mode: rename existed files',
    )

    parser.add_argument(
        '-t', '--template',
        help='Template for file naming based on time of creation',
    )
    parser.add_argument(
        '-d', '--dest', type=Path,
        help='A path to the destination directory (in case of a copy-mode)',
    )
    parser.add_argument(
        '-m', '--meta', action='store_true',
        help='Extract file\'s date from metadata only',
    )

    logging_group = parser.add_argument_group('logging')
    logging_group.add_argument(
        '-1', '--debug', dest='logging_level', action='store_const',
        const=logging.DEBUG, help='Set DEBUG level',
    )
    logging_group.add_argument(
        '-2', '--info', dest='logging_level', action='store_const',
        const=logging.INFO, help='Set INFO level',
    )
    logging_group.add_argument(
        '-3', '--warning', dest='logging_level', action='store_const',
        const=logging.WARNING, help='Set WARNING level',
    )
    logging_group.add_argument(
        '-4', '--error', dest='logging_level', action='store_const',
        const=logging.ERROR, help='Set ERROR level',
    )

    args = parser.parse_args()
    if args.mode == 'copy' and not args.dest:
        parser.error('--dest is required when --copy is set')

    if not (args.source.is_dir() or args.source.is_file()):
        parser.error('source doesn\'t exist')

    if args.dest and not args.dest.is_dir():
        args.dest.expanduser()
        args.dest.mkdir(parents=True, exist_ok=True)

    return args


def get_config() -> dict[str, Any]:
    config = vars(_read_args())
    config['logging'] = {
        'level': config.pop('logging_level'),
        'format': config.pop('logging_format'),
    }
    return config


def configure_logging(format: str, level: int, **kwargs) -> None:  # noqa: A002
    logging.basicConfig(format=format, level=level, **kwargs)
