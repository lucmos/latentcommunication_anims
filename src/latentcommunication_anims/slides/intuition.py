from manim import *
from manim_slides import Slide
from powermanim.layouts.arrangedbullets import Bullet
from powermanim.templates.bulletlist import BulletList

from latentcommunication_anims.utils import section_slide

FONT_SIZE = 38


class Intuition(Slide):
    def construct(self) -> None:
        slidetitle_text = "Why do they work?"
        section_slide(self, section_title=slidetitle_text)

        conclusions = (
            Bullet(
                r"\textbf{Semantic correspondence} between the data distributions",
                font_size=FONT_SIZE,
                level=0,
                group=0,
                symbol="1)",
            ),
            Bullet(
                r"Do not unify the entire ambient spaces, i.e., the latent spaces",
                font_size=FONT_SIZE,
                level=0,
                group=1,
                symbol="2)",
            ),
            Bullet(
                "...only the ",
                r"\textbf{data manifolds}",
                " embedded in them!",
                font_size=FONT_SIZE,
                level=1,
                group=2,
                symbol=None,
                adjustment=UP,
            ),
        )

        bulletlist = BulletList(
            *conclusions,
            line_spacing=LARGE_BUFF * 1.5,
            left_buff=MED_SMALL_BUFF * 2,
            global_shift=DOWN * 0.5,
            scale_active=1.15,
            inactive_opacity=0.25,
        )

        self.play(
            FadeIn(x := Tex(slidetitle_text).to_edge(UP)),
            FadeIn(bulletlist),
            run_time=1,
        )

        for _ in range(len(conclusions)):
            self.wait(0.1)
            self.next_slide()
            self.play(bulletlist.also_next())

        self.wait(0.1)
        self.next_slide(auto_next=True)

        self.play(
            FadeOut(bulletlist),
            FadeOut(x),
            run_time=1.5,
        )
        self.wait(0.1)
