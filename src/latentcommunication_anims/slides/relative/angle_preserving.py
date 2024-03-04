import itertools

from manim import *
from manim_slides import Slide
from powermanim.components.invariance import Invariance
from pytorch_lightning import seed_everything

from nn_core.common import PROJECT_ROOT

from latentcommunication_anims.utils import section_slide


def ncycles(iterable, n):
    "Returns the sequence elements n times"

    return itertools.chain.from_iterable(itertools.repeat(tuple(iterable), n))


class AnglePreserving(Slide):
    def construct(self):

        question = Tex(
            r"Can we model how these\\[1.5ex] ",
            "distinct latent spaces",
            " are related?",
        )

        self.play(AnimationGroup(FadeIn(question)))

        self.wait()
        self.next_slide()

        answer = Tex(r"Yes!").scale(1.5).shift(UP * 2.5)
        answer2 = Tex(
            r"Here, we assume\\",
            "an angle-norm preserving transformation $\mathcal{T}$ of the latent space",
            font_size=44,
        ).next_to(answer, DOWN, buff=MED_LARGE_BUFF)

        self.play(
            AnimationGroup(
                FadeIn(answer),
                ReplacementTransform(question, answer2),
                lag_ratio=0.5,
            )
        )

        inv_showcase = Invariance(
            Axes(
                x_range=[-1.5, 1.5],
                y_range=[-1.5, 1.5],
                x_length=4,
                y_length=4,
                axis_config={"include_ticks": False},
            )
            .to_edge(DOWN)
            .set_opacity(0.5)
        )

        self.play(Create(inv_showcase))

        for i in [
            np.pi * 0.1,
            np.pi * 0.15,
            np.pi * 0.2,
        ]:
            self.play(
                inv_showcase.transformation_anim(
                    np.array(
                        [
                            [np.cos(i), -np.sin(i), 0],
                            [np.sin(i), np.cos(i), 0],
                            [0, 0, 1],
                        ]
                    ),
                    run_time=0.5,
                )
            )

        for i in range(2, 5):
            self.play(
                inv_showcase.transformation_anim(
                    inv_showcase.get_random_ortho_matrix(),
                    run_time=0.5,
                )
            )

        point_indices = [0, 1, 2, 7, 8]
        radii_anim, lines = inv_showcase.radii_anim(point_indices, run_time=0.275)
        self.play(radii_anim)

        self.play(inv_showcase.rescale_along_radius_anim(point_indices, lines=lines))

        self.next_slide()

        self.play(
            inv_showcase.rescale_all_to_unit_anim(
                run_time=1.0,
            )
        )

        self.next_slide()
        relrep_need = (
            Tex(r"...we need a representation invariant to $\mathcal{T}$")
            .scale(1.25)
            .next_to(answer2, DOWN, buff=LARGE_BUFF * 2)
        )
        self.play(
            AnimationGroup(
                # AnimationGroup(*(FadeOut(x) for x in [triangle])),
                FadeOut(inv_showcase),
                FadeIn(relrep_need),
                lag_ratio=0.5,
            )
        )

        self.play(ShowPassingFlash(Underline(relrep_need, color=YELLOW)))
        self.wait()

        self.next_slide(auto_next=True)
        self.play(*(Uncreate(x) for x in [relrep_need, answer, answer2]))
        self.wait(0.1)
