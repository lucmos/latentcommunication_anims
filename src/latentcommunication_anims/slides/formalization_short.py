import typing as tp
from functools import partial
from math import copysign

from manim import *
from manim_slides.slide import Slide
from powermanim import (
    Bullet,
    BulletList,
    DirectionalArrow,
    GroupActivable,
    VAutoActivable,
)
from powermanim.templates.sectiontitle import Color

from latentcommunication_anims.utils import section_slide

X_COLOR = RED
Y_COLOR = GREEN

MANIFOLD_EMBEDDING_Y_SHIFT = 0.325

MANIFOLD_BUFF = 1.75
AMBIENTS_HORIZ_BUFF = 1.5
AMBIENTS_VERT_BUFF = 1.25

LABEL_SCALE = 0.8

LABEL_BUFF = 0.075

FONT_SIZE = 38


class FormalizationShort(Slide):
    def construct(self) -> None:
        section_slide(self, section_title=r"The Latent Communication\\Problem")

        general_problem = Tex(r"Finding a universal space or a direct translation")
        general_problem2 = Tex(
            r"...are instances of the same \textbf{general} problem!"
        ).next_to(general_problem, DOWN, buff=MED_LARGE_BUFF * 2)
        VGroup(general_problem, general_problem2).move_to(ORIGIN)
        self.play(
            AnimationGroup(
                FadeIn(general_problem),
                FadeIn(general_problem2),
                lag_ratio=1,
            ),
            run_time=2,
        )
        self.wait(0.1)
        self.next_slide()

        intuitiontitle = Tex("What are we doing?").to_edge(UP)
        intuition = Tex("Searching for transformations of the latent ambient spaces")
        intuition2 = Tex("that implicitly align the manifolds embedded into them")
        VGroup(intuition, intuition2).arrange(DOWN, buff=1).move_to(ORIGIN)

        self.play(
            FadeOut(general_problem),
            FadeOut(general_problem2),
        )
        self.play(
            AnimationGroup(
                FadeIn(intuitiontitle),
                FadeIn(intuition),
                FadeIn(intuition2),
                lag_ratio=0.5,
            )
        )

        referto = Tex("Refer to the manuscript for the formalization")
        referto.scale(0.75).set_opacity(0.5)
        referto.to_corner(DR)

        self.play(Write(referto), run_time=0.75)

        self.wait(0.1)
        self.next_slide(auto_next=True)
        self.play(
            AnimationGroup(
                FadeOut(referto),
                FadeOut(intuitiontitle),
                FadeOut(intuition),
                FadeOut(intuition2),
            )
        )
