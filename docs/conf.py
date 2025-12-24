# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'asimov-pyomicron'
copyright = '2024, Daniel Williams'
author = 'Daniel Williams'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_multiversion',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'kentigern'
html_static_path = ['_static']

# -- Intersphinx configuration -----------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'asimov': ('https://docs.ligo.org/asimov/asimov/', None),
    'pyomicron': ('https://pyomicron.readthedocs.io/en/latest/', None),
}

# -- Autodoc configuration ---------------------------------------------------

autodoc_member_order = 'bysource'
autodoc_typehints = 'description'

# -- Napoleon configuration --------------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True

# -- Sphinx-multiversion configuration ---------------------------------------

# Whitelist pattern for tags (only release tags)
smv_tag_whitelist = r'^v\d+\.\d+\.\d+$'

# Whitelist pattern for branches (main/master and develop)
smv_branch_whitelist = r'^(main|master|develop)$'

# Whitelist pattern for remotes
smv_remote_whitelist = r'^(origin)$'

# Pattern for released versions
smv_released_pattern = r'^refs/tags/v\d+\.\d+\.\d+$'

# Output directory
smv_outputdir_format = '{ref.name}'
