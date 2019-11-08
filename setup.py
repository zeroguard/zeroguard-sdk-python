#!/usr/bin/env python3
"""ZeroGuard package build script."""
import os
import setuptools


PACKAGE_NAME = 'zeroguard'
PARENT_DIR = os.path.abspath(os.path.dirname(__file__))

ABOUT_FILE = os.path.join(PARENT_DIR, PACKAGE_NAME, '__version__.py')
README_FILE = 'README.md'

REQUIREMENTS = []
TEST_REQUIREMENTS = []


def load_package_info():
    """Load package information from corresponding files."""
    about = {}
    with open(ABOUT_FILE) as about_file:
        # pylint: disable=W0122
        exec(about_file.read(), about)

    readme = None
    with open(README_FILE) as readme_file:
        readme = readme_file.read()

    return about, readme


def main():
    """."""
    about, readme = load_package_info()

    setuptools.setup(
        name=about['__title__'],
        version=about['__version__'],
        license=about['__license__'],

        description=about['__description__'],
        long_description=readme,
        long_description_content_type='text/markdown',

        author=about['__author__'],
        author_email=about['__author_email__'],
        url=about['__docs_url__'],

        packages=[PACKAGE_NAME],
        package_data={'': ['CHANGELOG.md', 'LICENSE']},

        python_requires='>=3.5',
        install_requires=REQUIREMENTS,
        tests_require=TEST_REQUIREMENTS,

        classifiers=[
            'Development Status :: 1 - Planning',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Topic :: Security'
        ],

        project_urls={
            'Documentation': about['__docs_url__'],
            'Source': about['__source_url__']
        }
    )


if __name__ == '__main__':
    main()
