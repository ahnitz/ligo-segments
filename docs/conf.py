# -*- coding: utf-8 -*-
#
# ligo-segments documentation build configuration file

import glob
import os.path
import re

from ligo.segments import __version__ as VERSION

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

# General information about the project.
project = u'ligo-segments'
copyright = u'2018, Kipp Cannon'
author = u'Kipp Cannon'

# The short X.Y version.
version = re.split('[\w-]', VERSION)[0]
# The full version, including alpha/beta/rc tags.
release = VERSION

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'monokai'

# Don't complain about remote URIs for images
suppress_warnings = ['image.nonlocal_uri']

# Intersphinx directory
intersphinx_mapping = {
    'https://docs.python.org/': None,  # python
}

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'ligo-segmentsdoc'

# -- add static files----------------------------------------------------------

def setup_static_content(app):
    curdir = os.path.abspath(os.path.dirname(__file__))
    # configure stylesheets
    for sdir in html_static_path:
        staticdir = os.path.join(curdir, sdir)

        # add stylesheets
        for cssf in glob.glob(os.path.join(staticdir, 'css', '*.css')):
            app.add_css_file(cssf[len(staticdir)+1:])

        # add custom javascript
        for jsf in glob.glob(os.path.join(staticdir, 'js', '*.js')):
            app.add_javascript(jsf[len(staticdir)+1:])

# -- setup --------------------------------------------------------------------

def setup(app):
    setup_static_content(app)
