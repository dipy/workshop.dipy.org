import os

from docutils import nodes
from docutils.parsers.rst import directives
from jinja2 import Environment, FileSystemLoader
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

logger = logging.getLogger(__name__)


class ContactItemDirective(SphinxDirective):
    has_content = True  # Contact item content (description)
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "title": directives.unchanged_required,  # e.g., "Email Us"
        "link": directives.unchanged_required,  # e.g., "mailto:workshop@dipy.org"
        "link_text": directives.unchanged_required,  # e.g., "workshop@dipy.org"
        "icon": directives.unchanged,  # e.g., "email" or "forum"
    }

    def run(self):
        env = self.env

        # Initialize the list of contact items in the environment if it doesn't exist
        if not hasattr(env, "workshop_contact_items"):
            env.workshop_contact_items = []

        # Store content as description
        description = "\n".join(self.content)

        contact_info = {
            "title": self.options.get("title"),
            "link": self.options.get("link"),
            "link_text": self.options.get("link_text"),
            "icon": self.options.get("icon", "email"),  # default to email
            "description": description,
        }

        env.workshop_contact_items.append(contact_info)

        # This directive itself doesn't return visible nodes
        return []


class ContactDirective(SphinxDirective):
    has_content = True  # Process content to find contact-item directives
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "template": directives.unchanged_required,  # Template path is required
        "title": directives.unchanged,  # Optional custom title
        "subtitle": directives.unchanged,  # Optional custom subtitle
    }

    def run(self):
        env = self.env
        app = env.app

        # Ensure the environment attribute exists and is cleared for this instance
        env.workshop_contact_items = []

        # Parse the content of the directive to run nested ContactItemDirectives
        node = nodes.container()
        self.state.nested_parse(self.content, self.content_offset, node)

        # Data collected by ContactItemDirective should now be in env.workshop_contact_items
        collected_items = getattr(env, "workshop_contact_items", [])

        if not collected_items:
            logger.warning(
                "No contact items found within the 'workshop-contact' directive.",
                location=self.get_location(),
            )
            return []

        # Get template name
        template_name = self.options.get("template")
        if not template_name:
            msg = "Contact directive requires a :template: option."
            logger.error(msg, location=self.get_location())
            return [nodes.error(None, nodes.paragraph(text=msg))]

        # Determine template path
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
                contact_items=collected_items,
                title=self.options.get("title", "Contact"),
                subtitle=self.options.get(
                    "subtitle", "Contact us for more information"
                ),
            )

        except Exception as e:
            err_msg = f'Error rendering contact template "{template_name}": {e}'
            logger.error(err_msg, location=self.get_location())
            return [nodes.error(None, nodes.paragraph(text=err_msg))]

        # Create a raw HTML node
        html_node = nodes.raw(text=rendered_html, format="html")

        # Clear the collected items
        env.workshop_contact_items = []

        return [html_node]
