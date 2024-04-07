from manim import *
from manim_slides.slide import Slide
from powermanim.layouts.arrangedbullets import Bullet
from powermanim.templates.bulletlist import BulletList

FONT_SIZE = 44


class DataExperiment5(Slide):
    def construct(self):
        title = Tex(
            r"Research question: Critical Samples",
        )
        title.to_edge(UP)

        subtitle = Tex(r"\emph{if $M_1$ and $M_2$ have different performance}").scale(0.75)
        subtitle.next_to(title, DOWN)

        bulletlist = (
            BulletList(
                Bullet(
                    r"Are the samples represented differently\\[1.5ex]the ones responsible for the improvement in performance?",
                    font_size=int(FONT_SIZE * 1.5),
                    symbol="",
                    level=1,
                    group=0,
                ),
                line_spacing=MED_LARGE_BUFF * 5,
                line_spacing_decay=0.5,
                scale_active=1.025,
                inactive_opacity=0.35,
            )
            .scale(0.7)
            .move_to(ORIGIN)
        )

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
