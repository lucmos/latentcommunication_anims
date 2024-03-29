from manim import *
from manim_slides.slide import Slide
from powermanim.layouts.arrangedbullets import Bullet
from powermanim.templates.bulletlist import BulletList


FONT_SIZE = 44


class DataResearch(Slide):
    def construct(self):
        title = Tex(
            r"Future Research in Data Curation",
        )
        title.to_edge(UP)

        bulletlist = (
            BulletList(
                Bullet(
                    "Curate multi-modal alignment",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                    group=0,
                ),
                Bullet(
                    "Disregard bad alignments or discover new ones",
                    font_size=FONT_SIZE,
                    level=1,
                    adjustment=0.05,
                    group=0,
                ),
                Bullet(
                    "Detection of conceptually comples samples (important!)",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                    group=1,
                ),
                Bullet(
                    "The ones that different models represent differently",
                    font_size=FONT_SIZE,
                    level=1,
                    adjustment=0.05,
                    group=1,
                ),
                Bullet(
                    "Handle OOD data",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                    group=2,
                ),
                Bullet(
                    "By translating the space induced by OOD data",
                    font_size=FONT_SIZE,
                    level=1,
                    adjustment=0.05,
                    group=2,
                ),
                Bullet(
                    "Detect semantically duplicated samples w.r.t. data relationships",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                    group=3,
                ),
                Bullet(
                    "Evaluate supervision consistency; deduplicate samples",
                    font_size=FONT_SIZE,
                    level=1,
                    adjustment=0.05,
                    group=3,
                ),
                Bullet(
                    "Detection of fairness unbalance in the dataset",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                    group=4,
                ),
                Bullet(
                    "e.g., exploiting the anchors selection: $d(mad, doctor) = d(woman, doctor)$",
                    font_size=FONT_SIZE,
                    level=1,
                    adjustment=0.05,
                    group=4,
                ),
                Bullet(
                    "...and many others!",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                    group=4,
                ),
                line_spacing=MED_LARGE_BUFF * 0.8,
                scale_active=1.025,
                inactive_opacity=0.35,
            )
            .scale(0.7)
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
