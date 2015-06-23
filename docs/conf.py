# -*- coding: utf-8 -*-
#
# -- General configuration -----------------------------------------------------

source_suffix = '.rst'
master_doc = 'index'

project = u'Documentation'
copyright = u'2015, Das Aktienregister'

version = '0.1.0'

# -- Options for HTML output ---------------------------------------------------

#extensions = ['sphinxjp.themecore']
#html_theme = 'dotted'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.graphviz',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.pngmath',
    'sphinx.ext.ifconfig',
 ]
# -- HTML theme options for `dotted` style -------------------------------------

#html_theme_options = {
#    'slidetoc': True,
#    'enablesidebar': True,
#    'rightsidebar': True,
#}

htmlhelp_basename = 'DasAktienregisterDocu'

man_pages = [
    ('index', 'areg-dev-docs', u'Aktienregister Development Documentation',
     [u'Aktienregister IT'], 1)
]

todo_include_todos=True
