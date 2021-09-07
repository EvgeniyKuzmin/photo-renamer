from pathlib import Path

from setuptools import find_packages, setup


setup(
    name='photo_renamer',
    version='0.1.1',
    description=(
        'Enables you making collections of unique photos or '
        'videos with names are formatted by a specific template.'
    ),
    keywords='jpeg',
    long_description=Path(__file__).parent.joinpath('README.md').read_text(),
    author='Evgeniy Kuzmin',
    author_email='evgeniy.kuzmin.a.kuzmin@gmail.com',
    url='https://github.com/EvgeniyKuzmin/photo_renamer',
    classifiers=[
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
    install_requires=[
        'ExifRead',
    ],
    extras_require={
        'dev': [
            'flake8',
            'flake8-builtins',
            'flake8-commas',
            'flake8-docstrings',
            'flake8-import-order',
            'coverage',
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'photo-renamer = photo_renamer.__main__:main',
        ],
    },
)
