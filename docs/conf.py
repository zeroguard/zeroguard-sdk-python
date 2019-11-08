"""Configuration file for Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""
# pylint: disable=C0103,C0413,E0401,W0622
import os
import sys

# Inject ZeroGuard package into PYTHONPATH
sys.path.insert(0, os.path.abspath('..'))
import zeroguard  # noqa

###############################################################################
# Project information
###############################################################################
project = zeroguard.__description__
release = zeroguard.__version__

author = zeroguard.__author__
copyright = zeroguard.__copyright__

###############################################################################
# General configuration
###############################################################################
# The master toctree document
master_doc = "index"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store'
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None)
}

###############################################################################
# Options for HTML output
###############################################################################
# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_show_sphinx = False

###############################################################################
# Extensions configuration
###############################################################################
todo_include_todos = True
