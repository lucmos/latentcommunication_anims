from manim import *
from manim_slides import Slide

from nn_core.common import PROJECT_ROOT


class Unireps(Slide):
    def construct(self):
        unireps = ImageMobject(filename_or_array=PROJECT_ROOT / "data" / "logos" / "unireps.png").scale(0.09)

        title = Tex("UniReps Workshop").scale_to_fit_height(unireps.height).scale(0.7)
        title.next_to(unireps, RIGHT)
        title = Group(unireps, title).move_to(ORIGIN).to_edge(UP)
        #

        longtitle = Tex("Unifying Representations in Neural Models")
        subtitle = Tex(r"\emph{NeurIPS 2023}").next_to(longtitle, DOWN)
        longtitle = VGroup(longtitle, subtitle).scale(1.15).next_to(title, DOWN, buff=LARGE_BUFF)

        unireps_qr = (
            ImageMobject(filename_or_array=PROJECT_ROOT / "data" / "logos" / "unireps_qr.png")
            .scale(0.4)
            .next_to(longtitle, DOWN, buff=LARGE_BUFF)
        )
        community = Tex(r"\emph{Join the community!}").next_to(unireps_qr, RIGHT, buff=LARGE_BUFF)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeIn(title),
                    FadeIn(longtitle),
                    FadeIn(unireps_qr),
                    run_time=1.5,
                    lag_ratio=0.2,
                ),
                FadeIn(community),
                lag_ratio=0.8,
            )
        )

        self.wait(duration=0.1)
        self.next_slide(auto_next=True)

        self.play(*(FadeOut(mob) for mob in (title, longtitle, unireps_qr, community)))

        self.wait(duration=0.1)
