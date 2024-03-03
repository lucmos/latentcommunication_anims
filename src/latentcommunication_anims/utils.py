from manim import *
from manim_slides import Slide
from powermanim.templates.sectiontitle import SectionTitle


def section_slide(slide: Slide, section_title: str):

    slide_title = SectionTitle(section_title=section_title)

    slide_title.show(scene=slide)

    slide.wait(0.1)
    slide.next_slide()

    slide_title.hide(scene=slide)
