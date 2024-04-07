from manim import *
from manim_slides.slide import Slide
from powermanim.layouts.arrangedbullets import Bullet
from powermanim.templates.bulletlist import BulletList


FONT_SIZE = 44


class DataAdvantages(Slide):
    def construct(self):
        title = Tex(
            r"Advantages",
        )
        title.to_edge(UP)

        bulletlist = (
            BulletList(
                Bullet(
                    r"Offers a \emph{tradeoff between performance and flexibility}",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                    group=0,
                ),
                Bullet(
                    r"Compute embeddings online {\footnotesize (choose the models $M_1$ and $M_2$ at runtime)}",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=1,
                    group=1,
                ),
                Bullet(
                    r"Compute embeddings offline and compare them online {\footnotesize (change the threshold $t$ at runtime)}",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=1,
                    group=2,
                ),
                Bullet(
                    r"Pre-compute everything, and just mark bad samples to be skipped accordingly",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=1,
                    group=3,
                ),
                Bullet(
                    "A lot to explore in possible variations between $M_1$ and $M_2$",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                    group=4,
                ),
                Bullet(
                    r"Seed, data modality, architecture, task, data quantity, data quality, ...",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=1,
                    group=5,
                ),
                Bullet(
                    r"Scale to more models $M_1, M_2, \ldots, M_k$ for better approximation and performance",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                    group=6,
                ),
                Bullet(
                    r"Improve the feature extractors quality to indirectly improve the data curation quality",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                    group=7,
                ),
                line_spacing=MED_LARGE_BUFF * 2,
                line_spacing_decay=0.5,
                scale_active=1.025,
                inactive_opacity=0.35,
            )
            .scale(0.7)
            .next_to(title, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2)
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
