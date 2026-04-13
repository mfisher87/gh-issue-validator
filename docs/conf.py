# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
from pathlib import Path

sys.path.insert(0, Path("..").resolve())

project = "gh-issue-valiator"
# copyright = ...
# author = ...

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

nitpicky = True

extensions = [
    "sphinx.ext.autodoc",  # Generate docs from docstrings
    "sphinx.ext.napoleon",  # Support Google-style docstrings
    "sphinx_autodoc_typehints",  # Generate docs from typehints
    "sphinx.ext.intersphinx",  # Link to other projects' docs
    "sphinx.ext.viewcode",  # Add links to source code
    # "sphinx_tabs.tabs",  # Support for tabbed "cards"
    "myst_parser",  # Parse Markdown files
]

myst_enable_extensions = [
    "colon_fence",
]

exclude_patterns = [
    "README.md",
]


# -- Options for autodoc -----------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "mistletoe": ("https://mistletoe-ebp.readthedocs.io/en/latest/", None),
}

# Support Google style docstrings, no mixing
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# Combine return description with return type
napoleon_use_rtype = False
typehints_use_rtype = False

# Display the parameter's default value alongside the parameter's type
typehints_defaults = "comma"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"

html_theme_options = {
    "logo": {
        "text": "gh-issue-validator",
    },
    "github_url": "https://github.com/mfisher87/gh-issue-validator",
    "use_edit_page_button": True,
    "show_prev_next": False,
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "show_nav_level": 2,
}

html_context = {
    "github_user": "mfisher87",
    "github_repo": "gh-issue-validator",
    "github_version": "main",
    "doc_path": "docs",
}

# -- Autodoc Options ---------------------------------------------------------
# Ensure methods are documented
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "undoc-members": True,
}
