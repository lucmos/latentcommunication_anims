from manim import *
from manim_slides import Slide
from powermanim.layouts.arrangedbullets import Bullet
from powermanim.templates.bulletlist import BulletList

from latentcommunication_anims.utils import section_slide

FONT_SIZE = 48


class Limitations(Slide):
    def construct(self) -> None:
        section_slide(self, section_title="Limitations")

        conclusions = (
            Bullet(
                r"Assumptions on $\mathcal{T}$",
                font_size=FONT_SIZE,
                level=0,
                group=0,
                symbol="1)",
            ),
            Bullet(
                r"Angle-norm preserving \textit{(relative representations)}",
                font_size=FONT_SIZE // 1.5,
                level=1,
                group=0,
                # symbol=None,
                adjustment=(UP * 0.4),
            ),
            Bullet(
                r"At most affine \textit{(latent translation)}",
                font_size=FONT_SIZE // 1.5,
                level=1,
                group=0,
                # symbol=None,
                adjustment=((UP * 2) * 0.4),
            ),
            Bullet(
                r"A large enough semantic correspondence to:",
                font_size=FONT_SIZE,
                level=0,
                group=1,
                symbol="2)",
            ),
            Bullet(
                r"Represent meaningful information \textit{(relative representations)}",
                font_size=FONT_SIZE // 1.5,
                level=1,
                group=1,
                # symbol=None,
                adjustment=(UP * 0.4),
            ),
            Bullet(
                r"Estimate $\mathcal{T}$ \textit{(latent translation)}",
                font_size=FONT_SIZE // 1.5,
                level=1,
                group=1,
                # symbol=None,
                adjustment=(UP * 0.4) * 2,
            ),
        )

        bulletlist = (
            BulletList(
                *conclusions,
                line_spacing=LARGE_BUFF * 0.7,
                scale_active=1.15,
                inactive_opacity=0.25,
            )
            .move_to(ORIGIN)
            .to_edge(LEFT, buff=LARGE_BUFF)
        )

        self.play(
            FadeIn(bulletlist),
            run_time=1,
        )

        for _ in range(bulletlist.ngroups):
            self.wait(0.1)
            self.next_slide()
            self.play(bulletlist.only_next())

        self.wait(0.1)
        self.next_slide(auto_next=True)

        self.play(
            FadeOut(bulletlist),
        )
