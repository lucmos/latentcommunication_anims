from manim import *
from manim_slides.slide import Slide
from powermanim.layouts.arrangedbullets import Bullet
from powermanim.templates.bulletlist import BulletList

FONT_SIZE = 44


class DataExperiment1(Slide):
    def construct(self):
        title = Tex(
            r"1. Unify the spaces",
        )
        title.to_edge(UP)

        bulletlist = (
            BulletList(
                Bullet(
                    "Consider two models $M_1$ and $M_2$",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                ),
                Bullet(
                    "If available, use a third known-to-be-good reference model to choose $M_1$ and $M_2$",
                    font_size=FONT_SIZE,
                    force_inline=True,
                    level=1,
                    adjustment=[0, 0.05, 0],
                ),
                Bullet(
                    "Unify their spaces as best as possible. To define ``best'', evaluate with:",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    adjustment=[0, -1, 0],
                    level=0,
                ),
                Bullet(
                    "Zero-Shot Stitching: train neural components in one space, re-use on the other ",
                    font_size=FONT_SIZE,
                    force_inline=True,
                    level=1,
                    adjustment=[0, -1 - 0.05, 0],
                ),
                Bullet(
                    "Retrieval: retrieval of data points from one space using queries from another space",
                    font_size=FONT_SIZE,
                    force_inline=True,
                    level=1,
                    adjustment=[0, -1 - 0.05, 0],
                ),
                line_spacing=MED_LARGE_BUFF * 1.5,
                scale_active=1.025,
                inactive_opacity=0.35,
            )
            .scale(0.7)
            .to_edge(LEFT)
        )

        self.play(
            AnimationGroup(
                Create(title),
                FadeIn(bulletlist),
                lag_ratio=0.5,
            ),
            run_time=1.25,
        )

        self.wait(0.1)

        for _ in range(bulletlist.ngroups):
            self.wait(0.1)
            self.next_slide()
            self.play(bulletlist.also_next())

        self.wait(0.1)
        self.next_slide(auto_next=True)
        self.play(
            FadeOut(bulletlist),
            Uncreate(title),
        )
        self.wait(0.1)
