from manim import *
from manim_slides.slide import Slide
from powermanim.layouts.arrangedbullets import Bullet
from powermanim.templates.bulletlist import BulletList


FONT_SIZE = 44


class DataExperiment2(Slide):
    def construct(self):
        title = Tex(
            r"2. Compare unified spaces",
        )
        title.to_edge(UP)

        bulletlist = (
            BulletList(
                Bullet(
                    "Choose a similarity (distance) function to compare the unified spaces",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                ),
                Bullet(
                    "e.g., MSE or cosine, with or without normalizations",
                    font_size=FONT_SIZE,
                    force_inline=True,
                    level=1,
                    adjustment=[0, 0.05, 0],
                ),
                Bullet(
                    r"This involves sanity checks to ensure spaces are similar \emph{iif} they are expected to be similar",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    adjustment=[0, -1, 0],
                    level=0,
                ),
                Bullet(
                    "e.g., changes in random seed induce similar spaces, change in data semantics do not",
                    font_size=FONT_SIZE,
                    force_inline=True,
                    level=1,
                    adjustment=[0, -1 - 0.05, 0],
                ),
                Bullet(
                    "...usually MSE or cosine are safe choices",
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
