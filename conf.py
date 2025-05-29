# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
import os
from datetime import date

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'workshop.dipy.org'
copyright = '2024, DIPY Team'
author = 'DIPY Team'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

sys.path.append(os.path.abspath('sphinxext'))
extensions = [
    'sphinx_design',
    'workshop',
    'jinja'
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']

html_css_files = ['css/workshop.css']
html_js_files = ['js/workshop.js', 'js/countdown.js', 'js/main.js']
html_logo = "_static/images/dipy-logo.png"

html_additional_pages = {
    "2025": "dw_2025.html"
}

html_theme_options = {
    "logo": {
        "link": "https://dipy.org",
    },
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": [],
    "navbar_persistent": [],
    "primary_sidebar_end": [],
    "secondary_sidebar_items": [],
    "show_toc_level": 1,
    "navigation_with_keys": False,
    "show_prev_next": False,
    "navbar_align": "content",
}

html_context = {
    "workshop": {
        "year": 2025,
        "location": "online",
        "codename": "Online",
        "start_date": date(2025, 3, 17),
        "end_date": date(2025, 3, 21),
        "speakers": {
            "all": [
                {
                    "avatar_url": "https://picsum.photos/200",
                    "fullname": "John Doe",
                    "title": "Research Associate",
                    "affiliation": "Indiana University"
                }
            ]
        },
        "bg_images": {
            "all": [
                {
                    "url": "https://picsum.photos/800"
                }
            ]
        }
    },
}
