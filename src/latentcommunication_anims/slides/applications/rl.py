from manim import *
from manim_slides import Slide
from powermanim.templates.reference import Reference

from nn_core.common import PROJECT_ROOT


class RL(Slide):
    def construct(self):
        slide_title = Tex("Zero-shot stitching in Reinforcement Learning").to_edge(UP)
        reference = Reference(
            text="Ricciardi, et al. “Zeroshot stitching in Reinforcement Learning using Relative Representations”, EWRL 2023",
            font_size=24,
        )
        scale = 1.75
        green = ImageMobject(PROJECT_ROOT / "data" / "cr_intro_green.png").scale(scale)
        red = ImageMobject(PROJECT_ROOT / "data" / "cr_intro_red.png").scale(scale)
        images = Group(green, red).arrange(RIGHT, buff=LARGE_BUFF).move_to(ORIGIN).shift(DOWN * 0.25)

        self.play(
            AnimationGroup(
                Create(slide_title),
                Create(reference),
                FadeIn(images),
                lag_ratio=0.2,
                run_time=2,
            ),
        )

        self.wait(0.1)
        self.next_slide(auto_next=True)

        self.play(FadeOut(images), FadeOut(reference), FadeOut(slide_title))
