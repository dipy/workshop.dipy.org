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
    'jinja'
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

html_css_files = ['css/workshop.css']

html_additional_pages = {
    "index": "dw_2025.html",
    "2025": "dw_2025.html"
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

