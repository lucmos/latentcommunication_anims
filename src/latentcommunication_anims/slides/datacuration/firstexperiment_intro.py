from manim import *
from manim_slides.slide import Slide
from powermanim import SectionTitle

FONT_SIZE = 44


class DataExperimentIntro(Slide):
    def construct(self):
        slide_title = SectionTitle(section_title=r"First Experiment")

        self.play(
            AnimationGroup(
                AnimationGroup(
                    slide_title.show(),
                    run_time=1,
                ),
                lag_ratio=0.8,
            )
        )

        self.wait(0.1)
        self.next_slide(auto_next=True)

        self.play(slide_title.hide())
