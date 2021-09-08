from collections import defaultdict
from datetime import datetime
import hashlib
import logging
from pathlib import Path
from shutil import copy
from typing import NamedTuple

from .config import configure_logging, get_config
from .date_extractor import get_date


logger = logging.getLogger(__name__)


class Task(NamedTuple):

    source: Path
    dest: Path
    mode: str


def show_report(report: dict[str, list], files_count: int) -> None:
    if not report:
        logger.info(f'No errors, {files_count} successfully processed files')
        return

    errors_count = sum(len(errs) for errs in report.values())
    logger.info('Processed files: %d', files_count)
    logger.info('Errors count: %d', errors_count)
    logger.info(
        'Persent of errors: %d', int(100 * (errors_count / files_count)),
    )

    for error_type, typed_errors in report.items():
        logger.info(f'{error_type}: %d'.capitalize(), len(typed_errors))
        logger.info(
            f'{error_type}:\n\t%s'.capitalize(),
            '\n\t'.join(str(f) for f in typed_errors),
        )


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
            errors['wrong extension'].append(relative_path)
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
            errors['duplicates'].append((
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

    show_report(errors, files_count=i + 1)


if __name__ == '__main__':
    main()
