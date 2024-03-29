"""Configure sphinx."""
import os
import sys
from datetime import date

import sphinx_bootstrap_theme

import remedian

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
curdir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(curdir, "..", "remedian")))

# -- Project information -----------------------------------------------------

project = 'remedian'
copyright = f"2018-{date.today().year}, Stefan Appelhoff"
author = 'Stefan Appelhoff'

# The short X.Y version
version = remedian.__version__
# The full version, including alpha/beta/rc tags
release = version


# -- General configuration ---------------------------------------------------


# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    'numpydoc',
    'sphinx_gallery.gen_gallery',
]

master_doc = "index"
autosummary_generate = True

# configure numpydoc
numpydoc_xref_param_type = True
numpydoc_show_class_members = False  # noqa: E501 https://stackoverflow.com/a/34604043/5201771

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# HTML options (e.g., theme)
# see: https://sphinx-bootstrap-theme.readthedocs.io/en/latest/README.html
# Clean up sidebar: Do not show "Source" link
html_show_sourcelink = False

html_theme = "bootstrap"
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

templates_path = ["_templates"]


# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "navbar_title": "remedian",
    "bootswatch_theme": "flatly",
    "navbar_sidebarrel": False,  # no "previous / next" navigation
    "navbar_pagenav": False,  # no "Page" navigation in sidebar
    "bootstrap_version": "3",
    "navbar_links": [
        ("Examples", "auto_examples/index"),
        ("API", "api"),
        ("Changelog", "changelog"),
        ("GitHub", "https://github.com/sappelhoff/remedian", True),
    ],
}


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://www.numpy.org/devdocs", None),
    "matplotlib": ("https://matplotlib.org", None),
}
intersphinx_timeout = 5

sphinx_gallery_conf = {
    "doc_module": ("remedian"),
    "reference_url": {
        "remedian": None,
    },
    'examples_dirs': '../examples',
    'gallery_dirs': 'auto_examples',
    'filename_pattern': '^((?!sgskip).)*$',
    'backreferences_dir': 'generated',
}
