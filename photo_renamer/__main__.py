from collections import defaultdict, namedtuple
from datetime import datetime
import hashlib
import logging
from pprint import pprint
from shutil import copy


from .config import configure_logging, get_config
from .date_extractor import get_date


logger = logging.getLogger(__name__)
Task = namedtuple('Task', ('source', 'dest', 'mode'))


def error_report(report: dict[str, list]) -> None:
    if not report:
        print('No errors')
        return

    print('ERROR REPORT'.center(79, '='))
    print(f'Duplicates: {len(report["duplicate"])}')
    pprint(report["duplicate"])

    print(f'No date: {len(report["no date"])}')
    pprint(report["no date"])


def process_tasks(tasks: list[Task]) -> None:
    for task in tasks:
        if task.mode == 'copy':
            logger.info('Coping %s to %s', task.source, task.dest)
            copy(task.source, task.dest)
        else:
            logger.info('Renaming %s to %s', task.source, task.dest.name)
            task.source.rename(task.dest)


def main() -> None:
    config = get_config()
    configure_logging(**config['logging'])
    logger.info('Config is loaded: %s', config)

    hashes = {}
    errors = defaultdict(list)
    tasks = []

    source = s.iterdir() if (s := config['source']).is_dir() else [s]
    photos = (
        fp for fp in source if fp.suffix.lower()
        in (f'.{ext}' for ext in config['filter'])
    )
    for i, photo_path in enumerate(photos):

        logger.info('Handling of %s', photo_path.name)
        hsh = hashlib.sha256(photo_path.read_bytes()).hexdigest()
        logger.info(
            'The SHA256 value of %s is: %s',
            photo_path.name, hsh,
        )
        if hsh in hashes:
            logger.warning(
                'File %s is a dublicate of "%s"',
                photo_path.name, hashes[hsh].name,
            )
            errors['duplicate'].append(photo_path.name)
            continue
        else:
            hashes[hsh] = photo_path

        dt = get_date(photo_path, config['extraction_mode'])
        if not isinstance(dt, datetime):
            logger.error(
                "The creation date of %s wasn't extracted", photo_path.name,
            )
            errors['no date'].append(photo_path.name)
            continue
        logger.info("The creation date of %s is: %s", photo_path.name, dt)

        if config['dest'] is None:
            dest = photo_path.parent / dt.strftime(config['template'])
        else:
            dest = config['dest'] / \
                photo_path.relative_to(config['source']).parent / \
                f'{dt.strftime(config["template"])}{photo_path.suffix}'
        tasks.append(
            Task(source=photo_path, dest=dest, mode=config['file_mode']),
        )

    logger.info(
        'JPEG-files were reviewed %d, tasks were created %d',
        i + 1, len(tasks),
    )
    process_tasks(tasks)

    error_report(errors)


if __name__ == '__main__':
    main()
