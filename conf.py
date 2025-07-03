# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "workshop.dipy.org"
copyright = "2025, DIPY Team"
author = "DIPY Team"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

sys.path.append(os.path.abspath("sphinxext"))
extensions = ["sphinx_design", "workshop", "jinja", "sphinx_reredirects"]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]

html_css_files = ["css/workshop.css"]
html_js_files = ["js/workshop.js", "js/countdown.js"]
html_logo = "_static/images/dipy-logo.png"

html_additional_pages = {
    "2019": "dw_2019.html",
    "2020": "dw_2020.html",
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
    "footer_start": [],
    "footer_center": [],
    "footer_end": [],
}

html_context = {
    "default_mode": "light",
}

html_sidebars = {"**": ["sidebar-nav-bs"]}

# -- Options for sphinx-reredirects -------------------------------------------
redirects = {
    "workshops/dipy-workshop-2019": "../2019.html",
    "workshops/dipy-workshop-2020": "../2020.html",
    "workshops/dipy-workshop-2021": "../2021.html",
    "workshops/dipy-workshop-2022": "../2022.html",
    "workshops/dipy-workshop-2023": "../2023.html",
    "workshops/dipy-workshop-2024": "../2024.html",
    "workshops/dipy-workshop-2025": "../2025.html",
    "dipy-workshop-2019": "2019.html",
    "dipy-workshop-2020": "2020.html",
    "dipy-workshop-2021": "2021.html",
    "dipy-workshop-2022": "2022.html",
    "dipy-workshop-2023": "2023.html",
    "dipy-workshop-2024": "2024.html",
    "dipy-workshop-2025": "2025.html",
}
