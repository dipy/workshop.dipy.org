import os

from docutils import nodes
from docutils.parsers.rst import directives
from jinja2 import Environment, FileSystemLoader
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

# from sphinx.writers.html5 import HTML5Translator # Potentially complex/unused
# from docutils.io import StringOutput # Unused

logger = logging.getLogger(__name__)


class ImgridItemDirective(SphinxDirective):
    has_content = False
    required_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "url": directives.unchanged,  # Image path/URL
        "alt": directives.unchanged_required,
        "ref": directives.unchanged,  # Optional reference link
        "width": directives.unchanged,  # Optional width
        "height": directives.unchanged,  # Optional height
    }

    def run(self):
        env = self.env

        # Initialize the list of images in the environment if it doesn't exist
        if not hasattr(env, "imgrid_images"):
            env.imgrid_images = []

        im_info = {
            "url": self.options.get("url"),
            "alt": self.options.get("alt"),
            "ref": self.options.get("ref"),
            "width": self.options.get("width"),  # Default width
            "height": self.options.get("height"),  # Default height
        }

        env.imgrid_images.append(im_info)

        # This directive itself doesn't return visible nodes
        # It just collects data. The container directive will render it.
        return []


class ImgridDirective(SphinxDirective):
    has_content = True  # Process content to find image directives
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "template": directives.unchanged_required,  # Template path is required
        "width": directives.unchanged,  # Optional width
        "height": directives.unchanged,  # Optional height
    }

    def run(self):
        env = self.env
        app = env.app

        # Ensure the environment attribute exists and is cleared for this instance
        env.imgrid_images = []

        # Parse the content of the directive to run nested ImgridDirectives
        node = nodes.container()
        # Crucially, parsing the content populates env.imgrid_images
        # via ImgridItemDirective.run() defined in imgrid.py
        self.state.nested_parse(self.content, self.content_offset, node)

        # Data collected by ImgridDirective should now be in env.imgrid_images
        collected_images = getattr(env, "imgrid_images", [])

        if not collected_images:
            logger.warning(
                "No images found within the 'imgrid' directive.",
                location=self.get_location(),
            )
            return []

        # --- Prepare data for template (just use collected data directly) ---
        template_name = self.options.get("template")
        if not template_name:
            msg = "Imgrid directive requires a :template: option."
            logger.error(msg, location=self.get_location())
            return [nodes.error(None, nodes.paragraph(text=msg))]

        images_for_template = collected_images  # Use the data as collected

        # --- Render Jinja Template ---
        # Determine path relative to source directory
        # template_name is relative to the current RST file's directory
        # OR srcdir if starts with /
        # For simplicity, assume template path is relative to srcdir or absolute
        if template_name.startswith("/"):
            # If starts with /, treat as relative to srcdir
            template_abs_path = os.path.join(env.srcdir, template_name[1:])
        else:
            # Otherwise, relative to current document's directory
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
            # Provide pathto helper function
            jinja_env.globals["pathto"] = (
                lambda filename, *args: html_builder.get_relative_uri(
                    env.docname, filename
                )
            )

            # Template expects raw RST in 'bio_rst' variable

            template = jinja_env.get_template(template_basename)
            rendered_html = template.render(
                images=images_for_template,
                width=self.options.get("width", 200),
                height=self.options.get("height", 200),
            )

        except Exception as e:
            err_msg = f'Error rendering image template "{template_name}": {e}'
            logger.error(err_msg, location=self.get_location())
            return [nodes.error(None, nodes.paragraph(text=err_msg))]

        # Create a raw HTML node
        html_node = nodes.raw(text=rendered_html, format="html")

        # Add optional section wrapper
        section = nodes.section(ids=["images"])
        section["classes"] += ["images-section"]
        section += html_node

        # Clear the collected images (good practice)
        env.imgrid_images = []

        return [section]
