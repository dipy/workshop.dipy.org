from docutils import nodes
from docutils.parsers.rst import directives
from jinja2 import Template
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

logger = logging.getLogger(__name__)


class ParticipantsDirective(SphinxDirective):
    """Directive for creating a participants carousel."""

    has_content = True
    option_spec = {
        "template": directives.path,
        "title": directives.unchanged,
        "subtitle": directives.unchanged,
    }

    def run(self):
        # Create container for participants
        participants = nodes.container()
        participants["classes"].append("participants-carousel")

        # Process content
        self.state.nested_parse(self.content, self.content_offset, participants)

        # Get template path
        template_path = self.options.get(
            "template", "_templates/participants_template.html"
        )

        # Collect participant items
        items = []
        for node in participants:
            if (
                isinstance(node, nodes.container)
                and "participant-item" in node["classes"]
            ):
                items.append(
                    {
                        "name": node.get("name", ""),
                        "image": node.get("image", ""),
                        "url": node.get("url", "#"),
                    }
                )

        # Read and render template
        try:
            with open(template_path, "r") as f:
                template = Template(f.read())
                rendered = template.render(
                    participant_items=items,
                    title=self.options.get("title", "Participants From"),
                    subtitle=self.options.get("subtitle", "")
                )
                return [nodes.raw("", rendered, format="html")]
        except Exception as e:
            logger.error(f"Error rendering participants: {e}")
            return []


class ParticipantItemDirective(SphinxDirective):
    """Directive for individual participant items."""

    has_content = False
    option_spec = {
        "name": directives.unchanged,
        "image": directives.unchanged,
        "url": directives.unchanged,
    }

    def run(self):
        item = nodes.container()
        item["classes"].append("participant-item")
        item["name"] = self.options.get("name", "")
        item["image"] = self.options.get("image", "")
        item["url"] = self.options.get("url", "#")
        return [item]
