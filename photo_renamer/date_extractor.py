from contextlib import suppress
from datetime import datetime
import logging
from pathlib import Path
import re
from typing import Literal, Optional

import exifread


logger = logging.getLogger(__name__)


def _get_date_via_exifread(file_path: Path) -> datetime:
    with open(file_path, 'rb') as file_desc:
        tags = exifread.process_file(file_desc)

    dt_str = None
    tag_names = (
        'EXIF DateTimeOriginal',
        'EXIF DateTimeDigitized',
        'Image DateTime',
    )
    for tag_name in tag_names:
        if tag_name in tags:
            dt_str = tags[tag_name].values
            break
    return datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S')



def _get_date_via_re_and_datetime(file_path: Path) -> Optional[datetime]:
    pattern = r'\d{8}_\d{6}'
    if match := re.search(pattern, file_path.name):
        return datetime.strptime(match.group(), '%Y%m%d_%H%M%S')


def get_date(
        file_path: Path,
        mode: Literal['meta', 'name', 'all'],
        ) -> Optional[datetime]:

    extractors = {
        'meta': _get_date_via_exifread,
        'name': _get_date_via_re_and_datetime,
    }

    if mode != 'all':
        extractors = {mode: extractors[mode]}

    for func in extractors.values():
        with suppress(KeyError, TypeError):
            dt = func(file_path)
            if isinstance(dt, datetime):
                return dt
        logger.error(
            'Date extractor "%s" was failed with %s', func.__name__, file_path,
        )
