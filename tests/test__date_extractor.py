from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from photo_renamer.date_extractor import (
    _get_date_via_re_and_datetime, get_date,
)


@pytest.fixture()
def fxt_get_date_via_exifread(request):
    with patch('photo_renamer.date_extractor._get_date_via_exifread') as mock:
        mock.__name__ = '_get_date_via_exifread'
        yield mock


@pytest.fixture()
def fxt_get_date_via_re_and_datetime(request):
    with patch(
            'photo_renamer.date_extractor.'
            '_get_date_via_re_and_datetime') as mock:
        mock.__name__ = '_get_date_via_re_and_datetime'
        yield mock


def test__get_date__meta__exifread_called_only(
        fxt_get_date_via_exifread, fxt_get_date_via_re_and_datetime,
        ):

    fake_jpg = Path('/fake.jpg')
    get_date(fake_jpg, 'meta')

    fxt_get_date_via_exifread.assert_called_once_with(fake_jpg)
    fxt_get_date_via_re_and_datetime.assert_not_called()


def test__get_date__name__via_re_dt_called_only(
        fxt_get_date_via_exifread, fxt_get_date_via_re_and_datetime,
        ):

    fake_jpg = Path('/fake.jpg')
    get_date(fake_jpg, 'name')

    fxt_get_date_via_exifread.assert_not_called()
    fxt_get_date_via_re_and_datetime.assert_called_once_with(fake_jpg)


def test__get_date__all__all_functions_called(
        fxt_get_date_via_exifread, fxt_get_date_via_re_and_datetime,
        ):

    fake_jpg = Path('/fake.jpg')
    get_date(fake_jpg, 'all')

    fxt_get_date_via_exifread.assert_called_once_with(fake_jpg)
    fxt_get_date_via_re_and_datetime.assert_called_once_with(fake_jpg)


def test__get_date__all_return_none__result_is_none(
        fxt_get_date_via_exifread, fxt_get_date_via_re_and_datetime,
        ):

    fake_jpg = Path('/fake.jpg')
    fxt_get_date_via_exifread.return_value = None
    fxt_get_date_via_re_and_datetime.return_value = None

    result = get_date(fake_jpg, 'all')
    assert result is None


def test__get_date__second_func_returns_dt__result_is_dt(
        fxt_get_date_via_exifread, fxt_get_date_via_re_and_datetime,
        ):

    fake_jpg = Path('/fake.jpg')
    dt = datetime.now()
    fxt_get_date_via_exifread.return_value = None
    fxt_get_date_via_re_and_datetime.return_value = dt

    result = get_date(fake_jpg, 'all')
    assert result == dt


def test__get_date_via_re_and_datetime__diff_files__correct_extraction():
    files_dates = {
        Path('20210131_101010.jpg'): datetime(2021, 1, 31, 10, 10, 10),
        Path('IMG_20210131_101010.jpeg'): datetime(2021, 1, 31, 10, 10, 10),
        Path('20210131_101010_111.JPG'): datetime(2021, 1, 31, 10, 10, 10),
    }
    for file_path, expected_dt in files_dates.items():
        actual_dt = _get_date_via_re_and_datetime(file_path)
        assert expected_dt == actual_dt
