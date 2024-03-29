# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options.
# For a full list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------

import os

# If extensions (or modules to document with autodoc) are in another
# directory, add these directories to sys.path here.
# If the directory is relative to the documentation root,
# use os.path.abspath to make it absolute, like shown here.
#
import re
import sys

sys.path.insert(0, os.path.abspath(".."))
sys.path.append(os.path.abspath("extensions"))
autodoc_mock_imports = ["pytz", "aiohttp", "requests", "typing_extensions"]

# -- Project information -----------------------------------------------

project = "aladhan.py"
copyright = "2021, HETHAT"
author = "HETHAT"

# The version info for the project you're documenting,
# acts as replacement for |version| and |release|,
# also used in various other places throughout the
# built documents.
#
# The short X.Y version.

version = ""
with open("../aladhan/__init__.py") as f:
    version = re.search(
        r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", f.read(), re.MULTILINE
    ).group(1)

# The full version, including alpha/beta/rc tags
release = version

branch = "master" if version.endswith("a") else "v" + version

# -- General configuration ---------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = "3.0"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.coverage",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_inline_tabs",
    "sphinx_copybutton",
    "resourcelinks",
]

# Links used for cross-referencing stuff in other documentation
intersphinx_mapping = {
    "py": ("https://docs.python.org/3", None),
}

rst_prolog = """
.. |coro| replace:: This function is a |coroutine_link|_.
.. |coroutine_link| replace:: *coroutine*
.. _coroutine_link: 
    https://docs.python.org/3/library/asyncio-task.html#coroutine
"""

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build"]


# -- Options for HTML output -------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation
# for a list of builtin themes.
#
html_title = "Aladhan.py"
html_theme = "furo"
html_theme_options = {
    "navigation_with_keys": True,
}

# Add any paths that contain custom static files (such as style sheets)
# here, relative to this directory.
#
# They are copied after the builtin static files,
# so a file named "default.css"
# will overwrite the builtin "default.css".

html_static_path = ["_static"]

resource_links = {
    "discord": "https://discord.gg/jeBGF8Veud",
    "issues": "https://github.com/HETHAT/aladhan.py/issues",
    "examples": f"https://github.com/HETHAT/aladhan.py/tree/{branch}/examples",
}

# remove type hints in docs
autodoc_typehints = "none"  # ('signature', 'description', 'none')

# display TODOs in docs
todo_include_todos = True

# avoid confusion between section references
autosectionlabel_prefix_document = True

# pygments styles
pygments_style = "sphinx"
