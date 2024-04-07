from manim import *
from manim_slides.slide import Slide
from powermanim import (
    Bullet,
    BulletList,
    GroupActivable,
    Reference,
    SectionTitle,
    VAutoActivable,
)

from latentcommunication_anims.utils import section_slide

FONT_SIZE = 44


class CurationIntro(Slide):
    def construct(self):
        slide_title = SectionTitle(
            section_title=r"Automatic Data Curation\\ {\scriptsize with Latent Communication}"
        )
        curation_goal = (
            GroupActivable(
                VAutoActivable(
                    Tex("Good Data"),
                    scale_about_edge=ORIGIN,
                    active_fill_opacity=0.5,
                    active_stroke_opacity=0.5,
                    inactive_fill_opacity=0,
                    inactive_stroke_opacity=0,
                    group=0,
                ),
                VAutoActivable(
                    Arrow(LEFT * 0.5, RIGHT * 0.5),
                    scale_about_edge=ORIGIN,
                    active_fill_opacity=0.5,
                    active_stroke_opacity=0.5,
                    inactive_fill_opacity=0,
                    inactive_stroke_opacity=0,
                    group=1,
                ),
                VAutoActivable(
                    Tex("Good Models"),
                    scale_about_edge=ORIGIN,
                    active_fill_opacity=0.5,
                    active_stroke_opacity=0.5,
                    inactive_fill_opacity=0,
                    inactive_stroke_opacity=0,
                    group=1,
                ),
                VAutoActivable(
                    Arrow(LEFT * 0.5, RIGHT * 0.5),
                    scale_about_edge=ORIGIN,
                    active_fill_opacity=0.5,
                    active_stroke_opacity=0.5,
                    inactive_fill_opacity=0,
                    inactive_stroke_opacity=0,
                    group=2,
                ),
                VAutoActivable(
                    Tex("Better Data"),
                    scale_about_edge=ORIGIN,
                    active_fill_opacity=0.5,
                    active_stroke_opacity=0.5,
                    inactive_fill_opacity=0,
                    inactive_stroke_opacity=0,
                    group=2,
                ),
            )
            .arrange(RIGHT, buff=MED_LARGE_BUFF)
            .scale(0.8)
            .next_to(slide_title, DOWN, buff=LARGE_BUFF * 1.25)
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    slide_title.show(),
                    run_time=1,
                ),
                AnimationGroup(
                    *(curation_goal.also_next() for _ in range(curation_goal.ngroups)),
                    lag_ratio=0.5,
                    run_time=1,
                ),
                lag_ratio=0.8,
            )
        )

        self.wait(0.1)
        self.next_slide(auto_next=True)

        self.play(slide_title.hide(), FadeOut(curation_goal))

        # Goal of data curation

        # title = Tex(
        #     r"Possible Research Directions",
        # )
        # title.to_edge(UP)

        # bulletlist = (
        #     BulletList(
        #         Bullet(
        #             "Analyze Multimodal Data: discover semantic correspondences (e.g. DNA \& RNA)",
        #             force_inline=True,
        #             font_size=FONT_SIZE,
        #             level=0,
        #         ),
        #         Bullet("Modular Neural Components: reusable decoders", font_size=FONT_SIZE, level=0),
        #         Bullet(
        #             "Relative Representations Interpretability: each dimension has a meaning",
        #             font_size=FONT_SIZE,
        #             level=0,
        #         ),
        #         Bullet(
        #             "Learnable Similarity Functions to infuse a data-driven invariance",
        #             font_size=FONT_SIZE,
        #             level=0,
        #         ),
        #         Bullet(
        #             "Geodesic Relative Representations to better describe the data manifold",
        #             font_size=FONT_SIZE,
        #             level=0,
        #         ),
        #         Bullet(
        #             r"Automatic Data Curation: exploit \emph{multiple good models} to curate the data",
        #             font_size=FONT_SIZE,
        #             level=0,
        #         ),
        #         line_spacing=LARGE_BUFF * 0.8,
        #         scale_active=1.025,
        #         inactive_opacity=0.35,
        #     )
        #     .scale(0.75)
        #     .to_edge(LEFT)
        #     .shift(DOWN * 0.5)
        # )

        # self.play(
        #     AnimationGroup(
        #         Create(title),
        #         FadeIn(bulletlist),
        #         lag_ratio=0.5,
        #     ),
        #     run_time=1.25,
        # )

        # self.wait()

        # for _ in range(bulletlist.ngroups):
        #     self.wait(0.1)
        #     self.next_slide()
        #     self.play(bulletlist.also_next())

        # self.wait(0.1)
        # self.next_slide(auto_next=True)
        # self.play(
        #     FadeOut(bulletlist),
        #     Uncreate(title),
