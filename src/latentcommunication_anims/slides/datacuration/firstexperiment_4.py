from manim import *
from manim_slides.slide import Slide
from powermanim.layouts.arrangedbullets import Bullet
from powermanim.templates.bulletlist import BulletList

FONT_SIZE = 44


class DataExperiment4(Slide):
    def construct(self):
        title = Tex(
            r"Application: Improve Data Quality",
        )
        title.to_edge(UP)

        subtitle = Tex(r"\emph{if $M_1$ and $M_2$ have similar performace}").scale(0.75)
        subtitle.next_to(title, DOWN)

        bulletlist = (
            BulletList(
                Bullet(
                    "The samples with distance greater that $t$ in the unifies space are ``hard'' samples",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                    group=0,
                ),
                Bullet(
                    "In the multimodal setting:",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                    group=1,
                ),
                Bullet(
                    "The ``hard'' samples are bad alignments between the modalities",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=1,
                    group=2,
                ),
                Bullet(
                    "We can just remove them or give them less importance in the training process",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=1,
                    group=3,
                ),
                Bullet(
                    r"(new ``easy'' alignments may be discovered by retrieval!)",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=1,
                    group=4,
                ),
                Bullet(
                    "In the unimodal setting:",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                    group=5,
                ),
                Bullet(
                    "The ``hard'' samples represent concepts more complex to represent",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=1,
                    group=6,
                ),
                Bullet(
                    "Important to detect!",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=1,
                    group=7,
                ),
                Bullet(
                    r"e.g., deduplicate the ``easy'' samples, add more examples of the ``hard'' ones\\(depending on the amount of data available)",
                    font_size=FONT_SIZE,
                    level=1,
                    group=8,
                ),
                line_spacing=MED_LARGE_BUFF * 1.5,
                line_spacing_decay=0.5,
                scale_active=1.025,
                inactive_opacity=0.35,
            )
            .scale(0.7)
            .next_to(subtitle, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2.5)
            .to_edge(LEFT)
        )

        # print(bulletlist.ngroups, "GROUPS")
        # self.add(bulletlist, subtitle, title)
        # self.wait()

        self.play(
            AnimationGroup(
                Create(title),
                FadeIn(subtitle),
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
            FadeOut(subtitle),
            Uncreate(title),
        )
