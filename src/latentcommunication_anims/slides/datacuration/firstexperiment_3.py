from manim import *
from manim_slides.slide import Slide
from powermanim.layouts.arrangedbullets import Bullet
from powermanim.templates.bulletlist import BulletList

FONT_SIZE = 44


class DataExperiment3(Slide):
    def construct(self):
        title = Tex(
            r"3. Choose a threshold $t$",
        )
        title.to_edge(UP)

        bulletlist = (
            BulletList(
                Bullet(
                    "Consider the sample-wise similariteis in the unified space",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                    group=0,
                ),
                Bullet(
                    "Sort the samples according to the chosen similarity function",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                    group=1,
                ),
                Bullet(
                    r"Determine a threshold $t$ that divides ``easy'' samples from ``hard'' samples.This involves:",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                    group=2,
                ),
                Bullet(
                    "Visual inspection of the samples at different thresholds $t$",
                    font_size=FONT_SIZE,
                    force_inline=True,
                    level=1,
                    adjustment=[0, 0.35, 0],
                    group=3,
                ),
                Bullet(
                    "Measuring the agreement of $M_1$ and $M_2$ on a downstream task",
                    font_size=FONT_SIZE,
                    force_inline=True,
                    level=1,
                    adjustment=[0, 0.35 * 2, 0],
                    group=4,
                ),
                Bullet(
                    "e.g., if $t$ does not change their agreement ratio in the good samples, probably $t$ is not good",
                    font_size=int(FONT_SIZE * 0.9),
                    force_inline=True,
                    level=2,
                    symbol="",
                    adjustment=[0, 0.35 * 3 + 0.15, 0],
                    group=4,
                ),
                Bullet(
                    r"Trial \& Error",
                    font_size=FONT_SIZE,
                    force_inline=True,
                    level=1,
                    adjustment=[0, 0.35 * 4 + 0.15, 0],
                    group=5,
                ),
                line_spacing=MED_LARGE_BUFF * 2,
                scale_active=1.025,
                inactive_opacity=0.35,
            )
            .scale(0.7)
            .move_to(ORIGIN)
            .to_edge(LEFT)
            .shift(DOWN * 0.5)
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
