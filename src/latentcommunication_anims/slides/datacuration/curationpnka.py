from manim import *
from manim_slides.slide import Slide

from nn_core.common import PROJECT_ROOT


class CurationPNKA(Slide):
    def construct(self):
        slide_title = Tex("Why should it work?").to_edge(UP)
        self.add(slide_title)
        pnka = ImageMobject(PROJECT_ROOT / "data" / "datacuration" / "pnka").scale(0.9).to_edge(LEFT)
        pnka = Group(
            pnka,
            Tex("PNKA is essentially comparing relative representations sample-wise").scale(0.75).to_edge(DOWN),
        )

        # reference = Reference(
        #     text="Chi Chen, et al. 2023. “Weakly Supervised Vision-and-Language Pre-training with Relative Representations”. In: ACL 2023",
        #     font_size=24,
        # )
        tldr = (
            Group(
                Tex("tldr."),
                Tex(r"Models disagree on samples with\\different relative representations"),
                ImageMobject(PROJECT_ROOT / "data" / "datacuration" / "pnka_plot").scale(0.8),
            )
            .arrange(DOWN, buff=MED_LARGE_BUFF)
            .scale(0.8)
            .to_edge(RIGHT)
        )

        self.play(
            AnimationGroup(
                # FadeIn(slide_title),
                FadeIn(pnka),
                AnimationGroup(*(FadeIn(x) for x in tldr), lag_ratio=0.5),
                lag_ratio=0.5,
                run_time=2,
            )
        )

        self.wait(0.1)
        self.next_slide(auto_next=True)

        self.play(
            FadeOut(slide_title),
            FadeOut(pnka),
            FadeOut(tldr),
        )
