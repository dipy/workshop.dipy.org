from docutils import nodes
# from docutils.parsers.rst import Directive # Removed unused import
from sphinx.util.docutils import SphinxDirective
# from sphinx_design.cards import Card # Removed unused import
# from sphinx_design.grids import Grid, GridItemCard # Removed unused imports
import datetime

# Helper function to format dates
def format_date_range(start_date, end_date):
    if start_date.year != end_date.year:
        return f"{start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}"
    elif start_date.month != end_date.month:
        return f"{start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}"
    else:
        return f"{start_date.strftime('%B %d')} - {end_date.strftime('%d, %Y')}"

class HomeDirective(SphinxDirective):
    has_content = False # This directive does not take content

    def run(self):
        workshop_ctx = self.env.config.html_context.get('workshop', {})
        # year = workshop_ctx.get('year', 'YYYY') # Removed unused variable
        location = workshop_ctx.get('location', 'Location')
        codename = workshop_ctx.get('codename', 'Codename')
        start_date = workshop_ctx.get('start_date', datetime.date.today())
        end_date = workshop_ctx.get('end_date', datetime.date.today())
        # bg_images = workshop_ctx.get('bg_images', {}).get('all', []) # Removed unused variable

        # --- Create Nodes ---
        section = nodes.section(ids=['home'])
        section['classes'] += ['home']

        # Title (Add directly to section)
        title = nodes.title(text="DIPY WORKSHOP")
        title['classes'] += ['content-title', 'l1-txt1', 'p-b-10'] # Adjust classes if needed
        section += title

        # Background Image Handling (Placeholder/CSS)
        # ...

        content_div = nodes.container()
        content_div['classes'] += ['full-page', 'content-section'] # Maybe remove full-page here?

        # Divider (Now inside content_div)
        divider = nodes.container()
        divider['classes'] += ['speaker-divider', 'm-b-40']
        content_div += divider

        # Codename
        codename_p = nodes.paragraph(text=f"{codename.title()} Edition")
        codename_p['classes'] += ['m2-txt4', 'p-b-25']
        content_div += codename_p

        # Dates
        date_str = format_date_range(start_date, end_date)
        date_p = nodes.paragraph(text=date_str)
        date_p['classes'] += ['m2-txt3', 'p-b-10']
        content_div += date_p

        # Location
        location_p = nodes.paragraph(text=location)
        location_p['classes'] += ['m2-txt1', 'p-b-48']
        content_div += location_p

        # Countdown Placeholders
        # ... (add placeholders to content_div)
        countdown_placeholder = nodes.paragraph(text="[", classes=['text-muted', 'p-b-48'])
        countdown_placeholder += nodes.emphasis(text="Countdown timer placeholder")
        countdown_placeholder += nodes.Text("]")
        content_div += countdown_placeholder

        # Registration Button Placeholder
        # ... (add placeholder to content_div)
        reg_button_container = nodes.container()
        reg_button_container['classes'] += ['p-b-25']
        reg_button = nodes.raw(
            text='<a href="#Registration" role="button" class="btn btn-lg btn-secondary register-btn">Register Now</a>',
            format='html'
        )
        reg_button_container += reg_button
        content_div += reg_button_container

        # Registration Countdown Placeholder
        # ... (add placeholder to content_div)
        reg_countdown_placeholder = nodes.paragraph(text="[", classes=['text-muted', 'p-b-48'])
        reg_countdown_placeholder += nodes.emphasis(text="Registration countdown placeholder")
        reg_countdown_placeholder += nodes.Text("]")
        content_div += reg_countdown_placeholder

        # Add the content container to the section *after* the title
        section += content_div
        return [section] 