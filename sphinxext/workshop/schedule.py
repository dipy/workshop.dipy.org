import os

from docutils import nodes
from docutils.parsers.rst import directives
from jinja2 import Environment, FileSystemLoader
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

logger = logging.getLogger(__name__)


class ScheduleDirective(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        "template": directives.unchanged,
        "title": directives.unchanged,
        "subtitle": directives.unchanged,
    }

    def run(self):
        env = self.env
        app = env.app

        # Initialize collection for all timelines
        env.workshop_timelines = []

        # Parse the nested timeline directives
        node = nodes.container()
        self.state.nested_parse(self.content, self.content_offset, node)

        # Get collected timelines
        collected_timelines = getattr(env, "workshop_timelines", [])

        if not collected_timelines:
            logger.warning(
                "No timelines found within the 'workshop-schedule' directive.",
                location=self.get_location(),
            )
            return []

        # Get template
        template_name = self.options.get(
            "template", "_templates/schedule_template.html"
        )

        if template_name.startswith("/"):
            template_abs_path = os.path.join(env.srcdir, template_name[1:])
        else:
            doc_dir = os.path.dirname(env.doc2path(env.docname, base=None))
            template_abs_path = os.path.join(doc_dir, template_name)

        template_dir = os.path.dirname(template_abs_path)
        template_basename = os.path.basename(template_abs_path)

        # Get HTML builder
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
                timelines=collected_timelines,
                title=self.options.get("title", "Workshop Schedule"),
                subtitle=self.options.get("subtitle", ""),
            )

        except Exception as e:
            err_msg = f'Error rendering schedule template "{template_name}": {e}'
            logger.error(err_msg, location=self.get_location())
            return [nodes.error(None, nodes.paragraph(text=err_msg))]

        # Create a raw HTML node
        html_node = nodes.raw(text=rendered_html, format="html")

        # Clear collection
        env.workshop_timelines = []

        return [html_node]
