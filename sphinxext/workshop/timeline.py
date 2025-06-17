import os

from docutils import nodes
from docutils.parsers.rst import directives
from jinja2 import Environment, FileSystemLoader
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

logger = logging.getLogger(__name__)


class TimelineItemDirective(SphinxDirective):
    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "time": directives.unchanged,
        "title": directives.unchanged,
        "speaker": directives.unchanged,
        "image": directives.unchanged,
    }

    def run(self):
        env = self.env

        # Check if we are inside a timeline context
        if (
            not hasattr(env, "current_timeline_items")
            or env.current_timeline_items is None
        ):
            logger.warning(
                "TimelineItemDirective used outside a TimelineDirective context.",
                location=self.get_location(),
            )
            return []

        item_info = {
            "time": self.options.get("time", ""),
            "title": self.options.get("title", "TBA"),
            "speaker": self.options.get("speaker", "TBA"),
            "image": self.options.get("image"),
        }

        env.current_timeline_items.append(item_info)

        return []


class TimelineDirective(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "title": directives.unchanged_required,
        "subtitle": directives.unchanged,
        "date": directives.unchanged,
        "template": directives.unchanged_required,
    }

    def run(self):
        env = self.env
        app = env.app

        # --- Initialize context for nested items ---
        # Store previous context if exists (for nested timelines, though unlikely here)
        # prev_items_context = getattr(env, 'current_timeline_items', None)
        env.current_timeline_items = []

        # Parse the content to run nested TimelineItemDirectives
        node = nodes.container()
        self.state.nested_parse(self.content, self.content_offset, node)

        # Data collected by TimelineItemDirective is now in env.current_timeline_items
        collected_items = env.current_timeline_items

        # Restore previous context if needed
        # env.current_timeline_items = prev_items_context

        # --- Prepare data for template ---
        template_name = self.options.get("template")
        if not template_name:
            msg = "Timeline directive requires a :template: option."
            logger.error(msg, location=self.get_location())
            return [nodes.error(None, nodes.paragraph(text=msg))]

        timeline_data = {
            "title": self.options.get("title", ""),
            "subtitle": self.options.get("subtitle", ""),
            "date": self.options.get("date", ""),
            "timeline_entries": collected_items,
        }

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
            rendered_html = template.render(timeline=timeline_data)
        except Exception as e:
            err_msg = f'Error rendering timeline template "{template_name}": {e}'
            logger.error(err_msg, location=self.get_location())
            return [nodes.error(None, nodes.paragraph(text=err_msg))]

        # Create a raw HTML node
        html_node = nodes.raw(text=rendered_html, format="html")

        # Return the rendered HTML (could wrap in a container if needed)
        return [html_node]
