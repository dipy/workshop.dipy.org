import os

from docutils import nodes
from docutils.parsers.rst import directives
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

logger = logging.getLogger(__name__)


class WhyItemDirective(SphinxDirective):
    has_content = True  # Content can be used for description or additional info
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "title": directives.unchanged,  # Optional caption for the image
    }

    def run(self):
        env = self.env

        # Initialize the list of why items in the environment if it doesn't exist
        if not hasattr(env, "workshop_why"):
            env.workshop_why = []

        description_rst = "\n".join(self.content)  # Join lines into a single string

        # Collect data for the why item
        why_item_info = {
            "title": self.options.get("title", ""),
            "description": Markup(description_rst),
        }

        env.workshop_why.append(why_item_info)
        return []


class WhyDirective(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "template": directives.unchanged_required,  # Template path is required
        "subtitle": directives.unchanged,  # Optional subtitle for the section
    }

    def run(self):
        env = self.env
        app = env.app

        env.workshop_why = []

        why_node = nodes.container()
        why_node["classes"].append("why")

        self.state.nested_parse(self.content, self.content_offset, why_node)
        template_name = self.options.get("template", "_templates/why_template.html")

        # --- Render Jinja Template ---
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
                why_items=env.workshop_why, subtitle=self.options.get("subtitle", "")
            )
        except Exception as e:
            err_msg = f'Error rendering timeline template "{template_name}": {e}'
            logger.error(err_msg, location=self.get_location())
            return [nodes.error(None, nodes.paragraph(text=err_msg))]

        # Create a raw HTML node
        html_node = nodes.raw(text=rendered_html, format="html")

        # Return the rendered HTML (could wrap in a container if needed)
        return [html_node]
