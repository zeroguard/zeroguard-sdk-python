#!/usr/bin/env python3
"""ZeroGuard package build script."""
import os
import setuptools

import zeroguard


PACKAGE_NAME = 'zeroguard'
PARENT_DIR = os.path.abspath(os.path.dirname(__file__))

ABOUT_FILE = os.path.join(PARENT_DIR, PACKAGE_NAME, '__version__.py')
README_FILE = 'README.md'

REQUIREMENTS = []
TEST_REQUIREMENTS = []


def main():
    """Set up the package."""
    with open(README_FILE) as readme_file:
        readme = readme_file.read()

    setuptools.setup(
        name=zeroguard.__title__,
        version=zeroguard.__version__,
        license=zeroguard.__license__,

        description=zeroguard.__description__,
        long_description=readme,
        long_description_content_type='text/markdown',

        author=zeroguard.__author__,
        author_email=zeroguard.__author_email__,
        url=zeroguard.__home_url__,

        packages=[PACKAGE_NAME],
        package_data={'': ['CHANGELOG.md', 'LICENSE']},

        python_requires='>=3.4',
        install_requires=REQUIREMENTS,
        tests_require=TEST_REQUIREMENTS,

        classifiers=[
            'Development Status :: 1 - Planning',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU Affero General Public License v3',
            'Natural Language :: English',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Topic :: Security'
        ],

        project_urls={
            'Documentation': zeroguard.__docs_url__,
            'Source': zeroguard.__source_url__
        }
    )


if __name__ == '__main__':
    main()
