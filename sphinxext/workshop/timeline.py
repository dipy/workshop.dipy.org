from docutils import nodes
from docutils.parsers.rst import directives
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
        "info": directives.unchanged,
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
            "info": self.options.get("info", ""),
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
        "template": directives.unchanged,  # Optional, for backwards compatibility
    }

    def run(self):
        env = self.env

        # Initialize collection for this timeline's items
        env.current_timeline_items = []

        # Parse the content to run nested TimelineItemDirectives
        node = nodes.container()
        self.state.nested_parse(self.content, self.content_offset, node)

        # Data collected by TimelineItemDirective is now in env.current_timeline_items
        collected_items = env.current_timeline_items

        # Prepare timeline data
        timeline_data = {
            "title": self.options.get("title", ""),
            "subtitle": self.options.get("subtitle", ""),
            "date": self.options.get("date", ""),
            "timeline_entries": collected_items,
        }

        # Add this timeline to the workshop_timelines collection
        if not hasattr(env, "workshop_timelines"):
            env.workshop_timelines = []

        env.workshop_timelines.append(timeline_data)

        # This directive doesn't render anything itself
        # The parent ScheduleDirective will render all timelines
        return []
