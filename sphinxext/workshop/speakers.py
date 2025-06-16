import os

from docutils import nodes
from docutils.parsers.rst import directives
from jinja2 import Environment, FileSystemLoader
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

# from sphinx.writers.html5 import HTML5Translator # Potentially complex/unused
# from docutils.io import StringOutput # Unused

logger = logging.getLogger(__name__)


class SpeakerItemDirective(SphinxDirective):
    has_content = True  # Speaker bio goes in the content
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "name": directives.unchanged_required,  # Make name required
        "image": directives.unchanged,  # Image path/URL
        "title": directives.unchanged,
        "affiliation": directives.unchanged,
    }

    def run(self):
        env = self.env

        # Initialize the list of speakers in the environment if it doesn't exist
        if not hasattr(env, "workshop_speakers"):
            env.workshop_speakers = []

        # Store raw RST content instead of parsing nodes here
        # self.content is a StringList (list of lines)
        bio_rst = "\n".join(self.content)  # Join lines into a single string

        speaker_info = {
            "name": self.options.get("name"),
            "image": self.options.get("image"),
            "bio_rst": bio_rst,  # Store raw RST content
            "title": self.options.get("title"),
            "affiliation": self.options.get("affiliation"),
        }

        env.workshop_speakers.append(speaker_info)

        # This directive itself doesn't return visible nodes
        # It just collects data. The container directive will render it.
        return []


class SpeakersDirective(SphinxDirective):
    has_content = True  # Process content to find speaker directives
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "template": directives.unchanged_required,  # Template path is required
    }

    def run(self):
        env = self.env
        app = env.app

        # Ensure the environment attribute exists and is cleared for this instance
        env.workshop_speakers = []

        # Parse the content of the directive to run nested SpeakerDirectives
        node = nodes.container()
        # Crucially, parsing the content populates env.workshop_speakers
        # via SpeakerDirective.run() defined in speaker.py
        self.state.nested_parse(self.content, self.content_offset, node)

        # Data collected by SpeakerDirective should now be in env.workshop_speakers
        collected_speakers = getattr(env, "workshop_speakers", [])

        if not collected_speakers:
            logger.warning(
                "No speakers found within the 'speakers' directive.",
                location=self.get_location(),
            )
            return []

        # --- Prepare data for template (just use collected data directly) ---
        template_name = self.options.get("template")
        if not template_name:
            msg = "Speakers directive requires a :template: option."
            logger.error(msg, location=self.get_location())
            return [nodes.error(None, nodes.paragraph(text=msg))]

        speakers_for_template = collected_speakers  # Use the data as collected

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
            rendered_html = template.render(speakers=speakers_for_template)

        except Exception as e:
            err_msg = f'Error rendering speaker template "{template_name}": {e}'
            logger.error(err_msg, location=self.get_location())
            return [nodes.error(None, nodes.paragraph(text=err_msg))]

        # Create a raw HTML node
        html_node = nodes.raw(text=rendered_html, format="html")

        # Add optional section wrapper
        # section = nodes.section()
        # section["classes"] += ["workshop-speakers-section"]
        # section += html_node

        # Clear the collected speakers (good practice)
        env.workshop_speakers = []

        return [html_node]
