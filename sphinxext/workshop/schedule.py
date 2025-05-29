from docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.util import logging

logger = logging.getLogger(__name__)


class ScheduleDirective(SphinxDirective):
    has_content = True

    def run(self):
        section = nodes.section(ids=['schedule'])
        section['classes'] += ['full-page', 'program', 'p-b-50'] # Outer section styling

        # Add title directly to section
        title = nodes.title(text="Schedule")
        title['classes'] += ['content-title', 'l1-txt1', 'p-b-10', 'color-black']
        section += title

        # Container for the timeline content rendered by nested directives
        content_node = nodes.container()
        content_node['classes'] += ['full-page-content', 'program-content']

        # Add divider and timezone note at the top of the content area
        divider = nodes.container()
        divider['classes'] += ['speaker-divider', 'm-b-10']
        timezone_note = nodes.strong(
            text="All times mentioned are according to EST Time Zone.",
            classes=['s2-txt2', 'fs-16', 'm-b-20']
        )
        content_node += divider
        content_node += timezone_note

        # Parse the nested timeline directives, their output will be added to
        # content_node
        self.state.nested_parse(self.content, self.content_offset, content_node)
        section += content_node

        return [section]
