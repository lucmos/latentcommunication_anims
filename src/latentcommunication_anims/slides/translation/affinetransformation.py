import itertools

from manim import *
from manim_slides import Slide
from powermanim.components.invariance import Invariance


class AffineTransformation(Slide):
    def construct(self):

        question = Tex(
            "Here, we are assuming $\mathcal{T}$ to be at most ",
            r"\emph{affine}",
        ).shift(UP * 2.5)

        invshowcase = Invariance(
            Axes(
                x_range=[-2, 2],
                y_range=[-2, 2],
                x_length=5,
                y_length=5,
                axis_config={"include_ticks": False},
            )
            .next_to(question, DOWN, buff=MED_LARGE_BUFF)
            .set_opacity(0.5)
        )

        self.play(Create(invshowcase), FadeIn(question))

        for _ in range(8):
            self.play(
                invshowcase.transformation_anim(
                    np.array(
                        [
                            [np.random.randn(), np.random.randn(), 0],
                            [np.random.randn(), np.random.randn(), 0],
                            [0, 0, 1],
                        ]
                    ),
                    bias=[np.random.randn() / 2, np.random.randn() / 2, 0],
                    run_time=1,
                )
            )

        self.wait(0.1)
        self.next_slide(auto_next=True)

        self.play(
            AnimationGroup(
                # AnimationGroup(*(FadeOut(x) for x in [triangle])),
                FadeOut(question),
                FadeOut(invshowcase),
                lag_ratio=0.1,
            )
        )
