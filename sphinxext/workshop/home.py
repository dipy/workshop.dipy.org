# from sphinx_design.cards import Card # Removed unused import
# from sphinx_design.grids import Grid, GridItemCard # Removed unused imports
from datetime import datetime
from venv import logger

import pytz
from docutils import nodes
from docutils.parsers.rst import directives

# from docutils.parsers.rst import Directive # Removed unused import
from jinja2 import Template
from sphinx.util.docutils import SphinxDirective


# Helper function to format dates
def format_date_range(start_date, end_date):
    if start_date.year != end_date.year:
        return f"{start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}"
    elif start_date.month != end_date.month:
        return f"{start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}"
    else:
        return f"{start_date.strftime('%B %d')} - {end_date.strftime('%d, %Y')}"


def parse_date(date_str, format="%Y-%m-%d %H:%M"):
    """Parse a date string into a datetime object."""
    try:
        return datetime.strptime(date_str, format)
    except ValueError as e:
        logger.error(f"Error parsing date '{date_str}': {e}")
        return None


def convert_to_iso(date_str, format="%Y-%m-%d %H:%M"):
    """Convert a date string to UTC timezone."""
    local_date = parse_date(date_str, format)
    if local_date:
        local_tz = pytz.timezone("America/New_York")  # Adjust to your local timezone
        local_date = local_tz.localize(local_date)
        return local_date.isoformat()
    return None


class HomeSlideDirective(SphinxDirective):
    has_content = False
    required_arguments = 1
    option_spec = {
        "alt": directives.unchanged,  # Alt text for the image
        "title": directives.unchanged,  # Optional title for the slide
        "code_name": directives.unchanged,  # Optional code name for the slide
        "start_date": directives.unchanged,  # Optional start date
        "end_date": directives.unchanged,  # Optional end date
        "location": directives.unchanged,  # Optional location
        "team_location": directives.unchanged,  # Optional team location
        "year": directives.unchanged,  # Optional year for the workshop
    }

    def run(self):
        env = self.env

        if not hasattr(env, "workshop_slides"):
            env.workshop_slides = []

        slide_info = {
            "image": self.arguments[0],  # Image path/URL
            "alt": self.options.get("alt", ""),  # Alt text for the image
        }

        env.workshop_slides.append(slide_info)

        return []


class HomeDirective(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "template": directives.unchanged_required,  # Template path is required
        "codename": directives.unchanged,  # Optional codename for the workshop
        "reg_start_date": directives.unchanged,  # Optional registration start date
        "start_date": directives.unchanged,  # Optional start date
        "end_date": directives.unchanged,  # Optional end date
        "location": directives.unchanged,  # Optional location
        "team_location": directives.unchanged,  # Optional team location
        "year": directives.unchanged,  # Optional year for the workshop
    }

    def run(self):
        env = self.env

        home_slides = nodes.container()

        self.state.nested_parse(self.content, self.content_offset, home_slides)

        collected_home_slides = getattr(env, "workshop_slides", [])

        if not collected_home_slides:
            logger.warning(
                "No home slides found within the 'home' directive.",
                location=self.get_location(),
            )
            return []

        template_path = self.options.get("template", "_templates/home_template.html")

        start_date = parse_date(self.options.get("start_date", ""))
        end_date = parse_date(self.options.get("end_date", ""))

        iso_start_date = convert_to_iso(self.options.get("start_date", ""))
        iso_reg_start_date = convert_to_iso(self.options.get("reg_start_date", ""))

        workshop_info = {
            "codename": self.options.get("codename", ""),
            "dates": format_date_range(start_date, end_date),
            "location": self.options.get("location", ""),
            "team_location": self.options.get("team_location", ""),
            "year": self.options.get("year", ""),
            "start_date": iso_start_date,
            "end_date": end_date.isoformat(),
            "reg_start_date": iso_reg_start_date,
        }

        try:
            with open(template_path, "r") as f:
                template = Template(f.read())
                rendered_html = template.render(
                    home_slides=collected_home_slides, workshop=workshop_info
                )
                return [nodes.raw(text=rendered_html, format="html")]
        except Exception as e:
            logger.error(f"Error rendering home template: {e}")
            return []
