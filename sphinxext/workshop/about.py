from docutils import nodes
from sphinx.util.docutils import SphinxDirective

# from docutils.parsers.rst.directives.images import Image # Removed unused import
# import os # Removed unused import


class AboutDirective(SphinxDirective):
    has_content = False

    def run(self):
        section = nodes.section(ids=["about"])
        section["classes"] += ["full-page", "about"]

        # Add divider after title, but still associated with heading conceptually
        heading_div = nodes.container()
        heading_div["classes"] += ["full-page-heading"]  # Keep class for styling?
        divider = nodes.container()
        divider["classes"] += ["speaker-divider", "m-b-40"]
        heading_div += divider
        section += heading_div  # Add divider container to section

        # Content
        content_div = nodes.container()
        content_div["classes"] += ["full-page-content", "about-content", "p-t-20"]

        # Watermark
        watermark_wrapper = nodes.container()
        watermark_wrapper["classes"] += [
            "flex-col-c-m",
            "pos-absolute",
            "watermark-wrapper",
        ]
        # Resolve static path - this might need refinement
        # watermark_uri = os.path.join(self.env.app.builder.srcdir,
        # '_static/images/dipy-watermark.svg') # Removed unused variable
        # Check if file exists, Sphinx should handle path resolution
        # For now, creating the node; builder might handle missing images
        # Use relative URI for HTML, Sphinx should resolve this correctly
        watermark_image = nodes.image(uri="/_static/images/dipy-watermark.svg", alt="")
        watermark_image["classes"] += ["watermark"]
        watermark_wrapper += watermark_image
        content_div += watermark_wrapper

        # Paragraphs
        p1_text = (
            "Attention grads, researchers, physicists, radiologists, doctors and "
            "technicians interested in medical imaging! Join us for an exciting "
            "online workshop hosted by DIPY. Our comprehensive program is designed "
            "to equip you with the skills and knowledge needed to master the latest "
            "techniques and tools in structural and diffusion imaging."
        )
        p1 = nodes.paragraph(text=p1_text, classes=["s2-txt4", "txt-justify", "fs-18"])

        p2_text = (
            "Our team of expert instructors will guide you through the fundamentals "
            "of diffusion theory, data pre-processing, fiber tracking, and much more. "
            "You'll have the opportunity to learn from industry-leading professionals, "
            "ask questions, and network with like-minded peers."
        )
        p2 = nodes.paragraph(
            text=p2_text, classes=["s2-txt4", "txt-justify", "fs-18", "p-t-20"]
        )

        p3_text = (
            "Whether you're new to diffusion imaging or an experienced practitioner, "
            "this workshop is perfect for you. Our curriculum is tailored to meet "
            "the needs of individuals at all levels of expertise. Don't miss this "
            "chance to enhance your skills and advance your career."
        )
        # Note: fa-18 class might be typo in original HTML? Using fs-18.
        p3 = nodes.paragraph(
            text=p3_text, classes=["s2-txt4", "txt-justify", "fs-18", "p-t-20"]
        )

        p4_text = (
            "Register today to secure your spot in this highly anticipated event. "
            "We can't wait to see you in the event!"
        )
        p4 = nodes.paragraph(
            text=p4_text, classes=["s2-txt4", "txt-justify", "fs-18", "p-t-20"]
        )

        p5 = nodes.paragraph(
            text="– DIPY Team!", classes=["s2-txt2", "txt-right", "p-t-20"]
        )

        content_div += [p1, p2, p3, p4, p5]
        section += content_div

        return [section]
