from sphinx.application import Sphinx

from .about import AboutDirective
from .carousel import CarouselDirective, CarouselItemDirective

# Import directive classes here (will be added later)
from .home import HomeDirective, HomeSlideDirective
from .participants import ParticipantItemDirective, ParticipantsDirective
from .pricing import PricingItemDirective, PricingListDirective
from .schedule import ScheduleDirective
from .speakers import SpeakerItemDirective, SpeakersDirective
from .timeline import TimelineDirective, TimelineItemDirective

# etc.


def setup(app: Sphinx):
    """Register custom directives with Sphinx."""
    # Add directives here (will be uncommented later)
    app.add_directive("workshop-home", HomeDirective)
    app.add_directive("workshop-home-slide", HomeSlideDirective)
    app.add_directive("workshop-about", AboutDirective)
    app.add_directive("workshop-speakers", SpeakersDirective)
    app.add_directive("workshop-speaker", SpeakerItemDirective)
    app.add_directive("workshop-schedule", ScheduleDirective)
    app.add_directive("workshop-timeline", TimelineDirective)
    app.add_directive("workshop-timeline-item", TimelineItemDirective)
    app.add_directive("pricing-list", PricingListDirective)
    app.add_directive("pricing-item", PricingItemDirective)
    app.add_directive("participants", ParticipantsDirective)
    app.add_directive("participant-item", ParticipantItemDirective)
    app.add_directive("carousel", CarouselDirective)
    app.add_directive("carousel-item", CarouselItemDirective)
    # app.add_directive("workshop-registration", RegistrationDirective)
    # app.add_directive("workshop-contact", ContactDirective)
    # app.add_directive("workshop-why", WhyDirective)
    # app.add_directive(
    #     "workshop-highlights", HighlightsDirective
    # ) # May need splitting (desktop/mobile) or CSS handling

    # Add roles if needed
    # app.add_role(...)

    # Add config values if needed
    # app.add_config_value(...)

    # Connect event listeners if needed
    # app.connect(...)

    # Return metadata
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
