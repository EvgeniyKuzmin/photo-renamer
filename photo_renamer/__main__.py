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

    exts = [f'.{e}' for e in config['extensions']]
    source = s.rglob('**/*') if (s := config['source']).is_dir() else [s]
    i = -1
    for i, file_path in enumerate(filter(lambda f: f.is_file(), source)):
        relative_path = str(file_path.relative_to(config['source']))

        logger.info('Handling of "%s"', relative_path)
        if file_path.suffix.lower() not in exts:
            logging.warning(
                'The extension of the file "%s" was filtered', relative_path,
            )
            continue

        hsh = hashlib.sha256(file_path.read_bytes()).hexdigest()
        logger.info(
            'The SHA256 value of "%s" is: %s',
            relative_path, hsh,
        )
        if hsh in hashes:
            logger.warning(
                'File "%s" is a dublicate of "%s"',
                relative_path, str(hashes[hsh].relative_to(config['source'])),
            )
            errors['duplicate'].append((
                relative_path,
                str(hashes[hsh].relative_to(config['source'])),
            ))
            continue

        hashes[hsh] = file_path

        dt = get_date(file_path, config['extraction_mode'])
        if not isinstance(dt, datetime):
            logger.error(
                'The creation date of "%s" wasn\'t extracted', relative_path,
            )
            errors['no date'].append(relative_path)
            continue
        logger.info('The creation date of "%s" is: %s', relative_path, dt)

        if config['dest'] is None:
            dest = file_path.parent / dt.strftime(config['template'])
        else:
            dest = config['dest'] / \
                file_path.relative_to(config['source']).parent / \
                f'{dt.strftime(config["template"])}{file_path.suffix}'
        tasks.append(
            Task(source=file_path, dest=dest, mode=config['file_mode']),
        )

    logger.info(
        'Files were reviewed %d, tasks were created %d',
        i + 1, len(tasks),
    )
    process_tasks(tasks)

    error_report(errors)


if __name__ == '__main__':
    main()
