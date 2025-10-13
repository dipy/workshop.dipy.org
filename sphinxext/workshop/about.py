import os

from docutils import nodes
from docutils.parsers.rst import directives
from jinja2 import Environment, FileSystemLoader
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

logger = logging.getLogger(__name__)


class AboutStatCardDirective(SphinxDirective):
    """Directive for individual stat cards within the about section."""

    has_content = False
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        "icon": directives.unchanged_required,  # Icon/emoji for the stat
        "number": directives.unchanged_required,  # The stat number
        "label": directives.unchanged_required,  # Description label
    }

    def run(self):
        # Store stat card data in environment
        if not hasattr(self.env, "about_stat_cards"):
            self.env.about_stat_cards = []

        stat_card = {
            "icon": self.options.get("icon", ""),
            "number": self.options.get("number", ""),
            "label": self.options.get("label", ""),
        }
        self.env.about_stat_cards.append(stat_card)

        # Return empty node as the parent directive will render everything
        return []


class AboutDirective(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        "template": directives.unchanged_required,
        "watermark_image_url": directives.unchanged,  # Optional watermark image URL
        "note_name": directives.unchanged,  # Optional note name
    }

    def run(self):
        env = self.env
        app = env.app

        # Initialize stat cards storage
        env.about_stat_cards = []

        # Parse nested content to collect stat cards
        node = nodes.container()
        self.state.nested_parse(self.content, self.content_offset, node)

        # Extract text content (non-directive lines)
        # Simpler approach: just filter out directive-related lines
        note_content = []
        skip_until_blank = False
        for line in self.content:
            stripped = line.strip()
            # If we encounter a directive, skip it and its options
            if stripped.startswith(".. about-stat-card::"):
                skip_until_blank = True
                continue
            # Skip option lines that start with ":"
            if skip_until_blank and (stripped.startswith(":") or not stripped):
                if not stripped:  # Empty line ends the directive
                    skip_until_blank = False
                continue
            # Reset skip flag if we hit non-option content
            if skip_until_blank and stripped and not stripped.startswith(":"):
                skip_until_blank = False
            # Add content lines
            if not skip_until_blank:
                note_content.append(line)

        template_name = self.options.get("template", "_templates/about_template.html")

        if template_name.startswith("/"):
            template_abs_path = os.path.join(env.srcdir, template_name[1:])
        else:
            doc_dir = os.path.dirname(env.doc2path(env.docname, base=None))
            template_abs_path = os.path.join(doc_dir, template_name)

        template_dir = os.path.dirname(template_abs_path)
        template_basename = os.path.basename(template_abs_path)

        # Need HTML builder for pathto helper
        if app.builder.format != "html":
            html_builder = app.env.app.registry.create_builder(app, "html")
        else:
            html_builder = app.builder

        try:
            jinja_loader = FileSystemLoader(template_dir)
            jinja_env = Environment(loader=jinja_loader, autoescape=True)
            jinja_env.globals["pathto"] = (
                lambda filename, *args: html_builder.get_relative_uri(
                    env.docname, filename
                )
            )
            template = jinja_env.get_template(template_basename)
            rendered_html = template.render(
                watermark_image_url=self.options.get("watermark_image_url", ""),
                note_name=self.options.get("note_name", ""),
                note_content=note_content,
                stat_cards=env.about_stat_cards,
            )
        except Exception as e:
            err_msg = f'Error rendering timeline template "{template_name}": {e}'
            logger.error(err_msg, location=self.get_location())
            return [nodes.error(None, nodes.paragraph(text=err_msg))]

        # Create a raw HTML node
        html_node = nodes.raw(text=rendered_html, format="html")

        # Return the rendered HTML (could wrap in a container if needed)
        return [html_node]
