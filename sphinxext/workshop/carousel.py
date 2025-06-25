import os

from docutils import nodes
from docutils.parsers.rst import directives
from jinja2 import Environment, FileSystemLoader
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

logger = logging.getLogger(__name__)


class CarouselItemDirective(SphinxDirective):
    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "image": directives.unchanged_required,  # Image path or URL is required
        "title": directives.unchanged,  # Optional caption for the image
        "description": directives.unchanged,  # Optional description
    }

    def run(self):
        env = self.env

        # Initialize the list of carousel items in the environment if it doesn't exist
        if not hasattr(env, "workshop_carousel"):
            env.workshop_carousel = []

        # This directive itself doesn't return visible nodes
        # It just collects data. The container directive will render it.

        carousel_item_info = {
            "image": self.options.get("image"),
            "title": self.options.get("title", ""),
            "description": self.options.get("description", ""),
        }

        env.workshop_carousel.append(carousel_item_info)
        return []


class CarouselDirective(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "template": directives.unchanged_required,  # Template path is required
    }

    def run(self):
        env = self.env
        app = env.app

        env.workshop_carousel = []

        # Create a container for the carousel
        carousel_node = nodes.container()
        carousel_node["classes"].append("carousel")

        # Parse the content of the directive
        self.state.nested_parse(self.content, self.content_offset, carousel_node)
        template_name = self.options.get("template", "_templates/swipe_carousel.html")

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
            rendered_html = template.render(carousel_items=env.workshop_carousel)
        except Exception as e:
            err_msg = f'Error rendering timeline template "{template_name}": {e}'
            logger.error(err_msg, location=self.get_location())
            return [nodes.error(None, nodes.paragraph(text=err_msg))]

        # Create a raw HTML node
        html_node = nodes.raw(text=rendered_html, format="html")

        # Return the rendered HTML (could wrap in a container if needed)
        return [html_node]
