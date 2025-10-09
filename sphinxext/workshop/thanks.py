from docutils import nodes
from docutils.parsers.rst import directives
from jinja2 import Template
from sphinx.util.docutils import SphinxDirective


class ThanksItemDirective(SphinxDirective):
    has_content = False
    required_arguments = 0
    option_spec = {
        "name": directives.unchanged,
        "image": directives.unchanged,
        "url": directives.unchanged,
    }

    def run(self):
        env = self.env

        if not hasattr(env, "thanks_items"):
            env.thanks_items = []

        thanks_item = {
            "name": self.options.get("name", ""),
            "image": self.options.get("image", ""),
            "url": self.options.get("url", ""),
        }

        env.thanks_items.append(thanks_item)

        return []


class ThanksDirective(SphinxDirective):
    has_content = True
    required_arguments = 0
    option_spec = {
        "template": directives.unchanged,
        "title": directives.unchanged,
        "subtitle": directives.unchanged,
        "note": directives.unchanged,
    }

    def run(self):
        env = self.env

        env.thanks_items = []
        thanks_items_node = nodes.container()

        self.state.nested_parse(self.content, self.content_offset, thanks_items_node)

        collected_thanks_items = getattr(env, "thanks_items", [])

        template_path = self.options.get("template", "_templates/thanks_template.html")

        try:
            with open(template_path, "r") as f:
                template = Template(f.read())
                rendered_html = template.render(
                    title=self.options.get("title", "Special Thanks"),
                    subtitle=self.options.get("subtitle", ""),
                    note=self.options.get("note", ""),
                    thanks_items=collected_thanks_items,
                )
                return [nodes.raw(text=rendered_html, format="html")]
        except Exception as e:
            self.env.app.warn(f"Error rendering thanks template: {e}")
            return []


def setup(app):
    app.add_directive("workshop-thanks", ThanksDirective)
    app.add_directive("workshop-thanks-item", ThanksItemDirective)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
