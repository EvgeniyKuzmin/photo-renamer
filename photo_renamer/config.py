from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
import logging
from pathlib import Path
from textwrap import fill
from typing import Any

from . import __doc__


logger = logging.getLogger(__name__)

DEFAULTS = {
    'file_mode': 'copy',
    'extraction_mode': 'all',
    'template': '%Y-%m-%d_%H-%M-%S',
    'extensions': ['jpg'],
    'logging_level': logging.INFO,
    'logging_format': (
        '%(asctime)s[%(levelname).4s]'
        '%(name)s.%(funcName)s:%(lineno)d %(message)s'
    ),
}
_name = __doc__.split('\n\n')[0].replace('.', '').lower().strip()
_desc_short = ' '.join(__doc__.split('\n\n')[1].split())
_desc_add = ' '.join(__doc__.split('\n\n')[2].split())


def _read_args() -> Namespace:
    parser = ArgumentParser(
        prog=_name.replace(' ', '-'),
        formatter_class=RawDescriptionHelpFormatter,
        description='\n\n'.join((
            f'{_name.title()}.',
            fill(_desc_short),
            '\n- '.join(fill(e) for e in _desc_add.split(' - ')),
        )),
    )
    parser.set_defaults(**DEFAULTS)
    parser.add_argument(
        'source', metavar='SOURCE', type=Path,
        help='A path to a source directory or a file',
    )

    parser.add_argument(
        '-t', '--template',
        help='Template for file naming based on time of creation',
    )
    parser.add_argument(
        '-e', '--extensions', nargs='+', metavar='EXT',
        help='File extensions that are suitable for processing',
    )
    parser.add_argument(
        '-d', '--dest', type=Path,
        help='A path to the destination directory (in case of a copy-mode)',
    )

    mode_group = parser.add_argument_group('mode')
    mode_group_me = mode_group.add_mutually_exclusive_group()
    mode_group_me.add_argument(
        '-c', '--copy', dest='file_mode', const='copy', action='store_const',
        help='COPY mode: make copies of existed files',
    )
    mode_group_me.add_argument(
        '-r', '--rename', dest='file_mode', const='rename',
        action='store_const', help='RENAME mode: rename existed files',
    )

    extraction_group = parser.add_argument_group('extraction mode')
    extraction_group_me = extraction_group.add_mutually_exclusive_group()
    extraction_group_me.add_argument(
        '-m', '--meta', dest='extraction_mode', const='meta',
        action='store_const', help='Extract a date from a metadata only',
    )
    extraction_group_me.add_argument(
        '-n', '--name', dest='extraction_mode', const='name',
        action='store_const', help='Extract a date from a filename only',
    )
    extraction_group_me.add_argument(
        '-f', '--file', dest='extraction_mode', const='file',
        action='store_const',
        help="Extract a date from a file's statistic only",
    )
    extraction_group_me.add_argument(
        '-a', '--all', dest='extraction_mode', const='all',
        action='store_const', help='Extract a date via all available methods',
    )

    logging_group = parser.add_argument_group('logging')
    logging_group_me = logging_group.add_mutually_exclusive_group()
    logging_group_me.add_argument(
        '-1', '--debug', dest='logging_level', action='store_const',
        const=logging.DEBUG, help='Set DEBUG level',
    )
    logging_group_me.add_argument(
        '-2', '--info', dest='logging_level', action='store_const',
        const=logging.INFO, help='Set INFO level',
    )
    logging_group_me.add_argument(
        '-3', '--warning', dest='logging_level', action='store_const',
        const=logging.WARNING, help='Set WARNING level',
    )
    logging_group_me.add_argument(
        '-4', '--error', dest='logging_level', action='store_const',
        const=logging.ERROR, help='Set ERROR level',
    )

    args = parser.parse_args()
    if args.file_mode == 'copy' and not args.dest:
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
