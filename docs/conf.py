# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
# sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))
sys.path.append(os.path.abspath('exts'))

# -- Project information -----------------------------------------------------

project = 'Charger_RPi_sphinx'
copyright = '2021, Zhansen Akhmetov, Stephen Paul'
author = 'Zhansen Akhmetov, Stephen Paul'

# The full version, including alpha/beta/rc tags
release = '1.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Mock imports for libraries that were missed in the python environment
autodoc_mock_imports = ["bluedot",
                        "PyQt5",
                        "pymongo",
                        "spidev",
                        "bluetooth",
                        "busio",
                        "gpiozero",
                        "concurrent.futures",
                        "board",
                        "micropython",
                        "smbus",
                        "pynmea2",
                        "serial",
                        "pickle5",
                        "subprocess",
                        "main_code",
                        "signal"]