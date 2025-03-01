from manim import *
from manim_slides import Slide
from powermanim.layouts.arrangedbullets import Bullet
from powermanim.templates.bulletlist import BulletList

FONT_SIZE = 38


class TranslationOtherResults(Slide):
    def construct(self):
        slidetitle = Tex("Other Results").to_edge(UP)

        conclusions = (
            Bullet(
                r"We achieve \textbf{zero-shot latent communication} in a variety of settings:",
                font_size=FONT_SIZE,
                level=0,
                group=0,
                symbol=None,
            ),
            Bullet(
                r"Both on generation and classification tasks",
                font_size=FONT_SIZE,
                level=1,
                group=0,
            ),
            Bullet(
                r"\textbf{Cross-architecture}: more than 10 pre-trained models!",
                font_size=FONT_SIZE,
                level=1,
                group=1,
            ),
            Bullet(
                r"\textbf{Cross-modality}: stitching between vision and language latent spaces",
                font_size=FONT_SIZE,
                level=1,
                group=2,
            ),
            Bullet(
                r"And evaluate it on more than 10 datasets ",
                font_size=FONT_SIZE,
                level=1,
                group=3,
            ),
            Bullet(
                r"We observe that the transformation $\mathcal{T}$ can be\\",
                r"often constrained to be \textbf{orthogonal} without performance loss",
                font_size=FONT_SIZE,
                level=0,
                group=4,
                symbol=None,
                adjustment=DOWN / 2 + RIGHT * 1.6,
            ),
        )

        bulletlist = BulletList(
            *conclusions,
            line_spacing=MED_LARGE_BUFF,
            left_buff=MED_LARGE_BUFF * 0.9,
            scale_active=1.02,
            inactive_opacity=0.35,
        ).next_to(slidetitle, DOWN, buff=LARGE_BUFF * 0.8)

        self.play(
            AnimationGroup(
                FadeIn(slidetitle),
                FadeIn(bulletlist),
                lag_ratio=0.5,
            ),
            run_time=1.25,
        )

        for group in range(max(x.group for x in conclusions) + 1):
            self.next_slide()
            to_play = [bulletlist.also_next()]
            if group == 5:
                to_play.append(
                    Circumscribe(conclusions[group], color=BLUE, buff=SMALL_BUFF)
                )
            self.play(*to_play)
        self.wait(0.1)

        self.next_slide(auto_next=True)
        self.play(
            FadeOut(slidetitle),
            AnimationGroup(
                FadeOut(bulletlist),
                lag_ratio=0.7,
            ),
            run_time=1.5,
        )
        self.wait(0.1)
