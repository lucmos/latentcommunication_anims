from manim import *
from manim_slides.slide import Slide
from powermanim import Reference

from nn_core.common import PROJECT_ROOT


class CurationWVLP(Slide):
    def construct(self):
        slide_title = Tex("Why should it work?").to_edge(UP)

        wvlp = ImageMobject(PROJECT_ROOT / "data" / "datacuration" / "wvlp").scale(0.7).to_edge(LEFT)
        wvlp = Group(wvlp, Tex("State of the Art in WVLP").next_to(wvlp, DOWN))

        reference = Reference(
            text="Chi Chen, et al. 2023. “Weakly Supervised Vision-and-Language Pre-training with Relative Representations”. In: ACL 2023",
            font_size=24,
        )
        tldr = (
            VGroup(
                Tex("tldr."),
                Tex(r"Unify spaces with\\Relative Representations"),
                Arrow(UP * 0.5, DOWN * 0.5),
                Tex(r"Discover good alignments\\from unimodal datasets"),
            )
            .arrange(DOWN, buff=MED_LARGE_BUFF)
            .to_edge(RIGHT)
        )

        self.play(
            AnimationGroup(
                FadeIn(slide_title),
                AnimationGroup(
                    FadeIn(wvlp),
                    FadeIn(reference),
                ),
                AnimationGroup(*(FadeIn(x) for x in tldr), lag_ratio=0.5),
                lag_ratio=0.5,
                run_time=2,
            )
        )

        self.wait(0.1)
        self.next_slide(auto_next=True)

        self.play(
            # FadeOut(slide_title),
            FadeOut(wvlp),
            FadeOut(tldr),
            FadeOut(reference),
        )
