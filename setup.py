from pathlib import Path

from setuptools import find_packages, setup

from photo_renamer import __author__, __doc__, __email__, __version__


_name = __doc__.split('\n\n')[0].replace('.', '').lower().strip()


setup(
    name=_name.replace(' ', '_'),
    version=__version__,
    description=' '.join(__doc__.split('\n\n')[1].split()),
    keywords=['photo', 'video', 'collection'],
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    author=__author__,
    author_email=__email__,
    license='MIT',
    license_files=('LICENSE',),
    platforms='Independent',
    url='https://github.com/EvgeniyKuzmin/photo_renamer',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Version Control :: Git',
    ],
    packages=find_packages(),
    install_requires=[
        'ExifRead',
    ],
    extras_require={
        'test': [
            'flake8',
            'flake8-builtins',
            'flake8-commas',
            'flake8-docstrings',
            'flake8-import-order',
            'coverage',
            'pytest',
        ],
        'dist': [
            'wheel',
            'twine',
        ],
    },
    entry_points={
        'console_scripts': [
            f'{_name.replace(" ", "-")} = photo_renamer.__main__:main',
        ],
    },
)
