import os

from docutils import nodes
from docutils.parsers.rst import directives
from jinja2 import Environment, FileSystemLoader
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

logger = logging.getLogger(__name__)


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
                note_content=self.content,
            )
        except Exception as e:
            err_msg = f'Error rendering timeline template "{template_name}": {e}'
            logger.error(err_msg, location=self.get_location())
            return [nodes.error(None, nodes.paragraph(text=err_msg))]

        # Create a raw HTML node
        html_node = nodes.raw(text=rendered_html, format="html")

        # Return the rendered HTML (could wrap in a container if needed)
        return [html_node]
