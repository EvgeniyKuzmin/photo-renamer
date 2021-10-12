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
            'flake8==3.9.2',
            'flake8-builtins==1.5.3',
            'flake8-commas==2.0.0',
            'flake8-docstrings==1.6.0',
            'flake8-import-order==0.18.1',
            'coverage==5.5',
            'pytest==6.2.5',
        ],
        'dist': [
            'wheel==0.37.0',
            'twine==3.4.2',
        ],
    },
    entry_points={
        'console_scripts': [
            f'{_name.replace(" ", "-")} = photo_renamer.__main__:main',
        ],
    },
)
