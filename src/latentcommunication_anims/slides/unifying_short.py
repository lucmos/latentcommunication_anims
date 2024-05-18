from manim import *
from manim_slides import Slide
from powermanim.layouts.arrangedbullets import Bullet
from powermanim.templates.bulletlist import BulletList


class UnifyingShort(Slide):
    def construct(self):
        question = Tex(
            r"Can we \textbf{unify} these latent spaces?",
        ).scale(1.5)

        self.play(
            FadeIn(question),
        )

        self.wait(0.1)
        self.next_slide()

        slidetitle = Tex(r"Can we \textbf{unify} these latent spaces?").to_edge(UP)

        FONT_SIZE = 38
        strategies = (
            Bullet(
                "Project them into a universal space",
                font_size=FONT_SIZE,
                level=0,
                group=0,
            ),
            Bullet(
                r"Directly translate from one to another",
                font_size=FONT_SIZE,
                level=0,
                group=1,
            ),
        )

        bulletlist = BulletList(
            *strategies,
            line_spacing=LARGE_BUFF * 1.5,
            left_buff=LARGE_BUFF * 1.5,
            scale_active=1.25,
            inactive_opacity=0.35,
        ).shift(DOWN * 0.4)

        self.play(
            AnimationGroup(
                TransformMatchingTex(question, slidetitle),
                FadeIn(bulletlist),
                lag_ratio=0.25,
            )
        )

        self.play(bulletlist.only_next())

        self.wait(0.1)
        self.next_slide()

        self.play(bulletlist.also_next())

        self.wait(0.1)
        self.next_slide(auto_next=True)

        self.play(
            FadeOut(bulletlist),
            Uncreate(slidetitle),
            run_time=1,
        )

        self.wait(0.1)


if __name__ == "__main__":
    Unifying().construct()
