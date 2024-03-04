from manim import *
from manim_slides import Slide
from powermanim.layouts.arrangedbullets import Bullet
from powermanim.templates.bulletlist import BulletList

from latentcommunication_anims.utils import section_slide

FONT_SIZE = 38


class Conclusions(Slide):
    def construct(self):
        section_slide(self, "Conclusions")
        self.next_slide()

        zeroshot = Tex(
            r"\textbf{Latent communication} between different latent spaces",
        )
        zeroshot.to_edge(UP)

        bulletlist_left = (
            BulletList(
                Bullet("It is possible!", font_size=int(FONT_SIZE * 2.25), level=0, symbol=None),
                Bullet("Either:", font_size=int(FONT_SIZE * 1.15), level=0, symbol=None),
                Bullet(r"Projecting into a universal space", font_size=FONT_SIZE, level=1),
                Bullet(r"Direct Latent Translation", font_size=FONT_SIZE, level=1),
                line_spacing=MED_LARGE_BUFF * 0.8,
                scale_active=1.025,
                inactive_opacity=0.35,
            )
            .scale(0.75)
            .to_edge(LEFT)
        )

        bulletlist_right = (
            BulletList(
                Bullet("Possible limitations:", font_size=FONT_SIZE, level=0, symbol=None),
                Bullet(r"Knowledge of the latent transformation $\mathcal{T}$", font_size=FONT_SIZE, level=1),
                Bullet(r"Availability of the semantic correspondence", font_size=FONT_SIZE, level=1),
                Bullet("Applications in:", font_size=FONT_SIZE, level=0, symbol=None, adjustment=DOWN * 0.5),
                Bullet(r"Zero-Shot Stitching", font_size=FONT_SIZE, level=1, adjustment=DOWN * 0.5),
                Bullet(r"Latent Model Evaluation", font_size=FONT_SIZE, level=1, adjustment=DOWN * 0.5),
                Bullet(
                    r"Retrieval: querying from one space into another",
                    font_size=FONT_SIZE,
                    level=1,
                    adjustment=DOWN * 0.5,
                ),
                Bullet(
                    r"Generalizing unimodal to multimodal models", font_size=FONT_SIZE, level=1, adjustment=DOWN * 0.5
                ),
                line_spacing=MED_LARGE_BUFF,
                scale_active=1.025,
                inactive_opacity=0.5,
            )
            .scale(0.75)
            .to_edge(RIGHT, buff=LARGE_BUFF * 0.9)
            .shift(DOWN * 0.5)
        )

        self.play(
            AnimationGroup(
                Create(zeroshot),
                FadeIn(bulletlist_left),
                FadeIn(bulletlist_right),
                lag_ratio=0.5,
            ),
            run_time=1.25,
        )

        self.wait()

        for _ in range(bulletlist_left.ngroups):
            self.wait(0.1)
            self.next_slide()
            self.play(bulletlist_left.also_next())

        for _ in range(bulletlist_right.ngroups):
            self.wait(0.1)
            self.next_slide()
            self.play(bulletlist_right.also_next())

        self.wait(0.1)
        self.next_slide(auto_next=True)
        self.play(
            FadeOut(bulletlist_left),
            FadeOut(bulletlist_right),
            Uncreate(zeroshot),
        )
