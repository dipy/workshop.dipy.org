from docutils import nodes
from docutils.parsers.rst import directives
from jinja2 import Template
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

logger = logging.getLogger(__name__)


class PricingListDirective(SphinxDirective):
    """Directive for creating a list of pricing items."""

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "template": directives.path,
        "title": directives.unchanged,
        "subtitle": directives.unchanged,
        "note": directives.unchanged,
        "description": directives.unchanged,
        "columns": directives.unchanged,
        "section_title": directives.unchanged,
        "section_subtitle": directives.unchanged,
        "wrap_section": directives.flag,
    }

    def run(self):
        # Get the template path from options or use default
        template_path = self.options.get("template", "_templates/pricing_template.html")

        # Create a container node for the pricing list
        pricing_list = nodes.container()
        pricing_list["classes"].append("pricing-list")

        # Process the content (pricing items)
        self.state.nested_parse(self.content, self.content_offset, pricing_list)

        # Collect pricing items and their features
        pricing_items = []
        for node in pricing_list:
            if isinstance(node, nodes.container) and "pricing-item" in node["classes"]:
                item = {
                    "name": node.get("name", ""),
                    "currency": node.get("currency", "$"),
                    "price": float(node.get("price", "0")),
                    "discount": float(node.get("discount", "0")),
                    "registration_link": node.get("registration_link", "#"),
                    "popular": node.get("popular", False),
                    "features": [],
                }

                # Extract features from bullet lists
                for child in node:
                    if isinstance(child, nodes.bullet_list):
                        for list_item in child:
                            if isinstance(list_item, nodes.list_item):
                                for para in list_item:
                                    if isinstance(para, nodes.paragraph):
                                        item["features"].append(para.astext())

                pricing_items.append(item)

        # Read the template file
        try:
            with open(template_path, "r") as f:
                template_content = f.read()
        except Exception as e:
            logger.error(f"Could not read template file {template_path}: {e}")
            return []

        columns = int(12 / int(self.options.get("columns", 2)))
        # Render the template
        try:
            template = Template(template_content)
            rendered = template.render(
                pricing_items=pricing_items,
                title=self.options.get("title", ""),
                subtitle=self.options.get("subtitle", ""),
                note=self.options.get("note", ""),
                description=self.options.get("description", ""),
                columns=columns,
                padding=f"p-l-{10 * columns}",
                section_title=self.options.get("section_title", ""),
                section_subtitle=self.options.get("section_subtitle", ""),
                wrap_section="wrap_section" in self.options,
            )

            # Create a raw HTML node with the rendered content
            raw_node = nodes.raw("", rendered, format="html")
            return [raw_node]
        except Exception as e:
            logger.error(f"Error rendering pricing template: {e}")
            return []


class PricingItemDirective(SphinxDirective):
    """Directive for individual pricing items."""

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "name": directives.unchanged,
        "currency": directives.unchanged,
        "price": directives.unchanged,
        "discount": directives.unchanged,
        "registration_link": directives.unchanged,
        "popular": directives.flag,
    }

    def run(self):
        # Create a container node for the pricing item
        pricing_item = nodes.container()
        pricing_item["classes"].append("pricing-item")

        # Add options as attributes
        pricing_item["name"] = self.options.get("name", "")
        pricing_item["currency"] = self.options.get("currency", "$")
        pricing_item["price"] = self.options.get("price", "0")
        pricing_item["discount"] = self.options.get("discount", "0")
        pricing_item["registration_link"] = self.options.get("registration_link", "#")
        pricing_item["popular"] = "popular" in self.options

        # Process the content (features list)
        self.state.nested_parse(self.content, self.content_offset, pricing_item)

        return [pricing_item]
