from manim import *
from manim_slides import Slide

from nn_core.common import PROJECT_ROOT

FONT_SIZE = 30
FONT_TABLE = 26
VISION_TABLE = 24

REC_PATH = PROJECT_ROOT / "data" / "bridge" / "aes_stitching_qualitative.jpg"


class BridgeResults(Slide):
    def construct(self):
        slidetitle = Tex("Reconstruction Performance").to_edge(UP)

        rec_image = ImageMobject(REC_PATH).scale(0.7)
        rec_label = Tex("AEs trained on CIFAR100", font_size=FONT_SIZE, z_index=2).to_corner(DR).set_opacity(0.75)

        labels_up = VGroup(
            Tex(r"$D_1 \circ E_2 $", font_size=28, z_index=2).next_to(rec_image, UP).shift(LEFT * 4),
            Tex(r"$D_2 \circ E_1 $", font_size=28, z_index=2).next_to(rec_image, UP).shift(LEFT * 1.3),
            Tex(r"$D_1 \circ E_1 $", font_size=28, z_index=2).next_to(rec_image, UP).shift(RIGHT * 1.3),
            Tex(r"$D_2 \circ E_2 $", font_size=28, z_index=2).next_to(rec_image, UP).shift(RIGHT * 4),
        )

        l1 = Tex(r"Source", font_size=FONT_TABLE, z_index=2).next_to(rec_image, LEFT).shift(UP * 1.5)
        l2 = (
            Tex(r"Cos, Euc, $L_1$, $L_{\infty}$", font_size=FONT_TABLE, z_index=2)
            .next_to(rec_image, LEFT)
            .shift(UP * 1.1)
        )
        l3 = Tex(r"Cos, Euc, $L_1$", font_size=FONT_TABLE, z_index=2).next_to(rec_image, LEFT).shift(UP * 0.6)
        l4 = Tex(r"Cosine", font_size=FONT_TABLE, z_index=2).next_to(rec_image, LEFT).shift(UP * 0.2)
        l5 = Tex(r"Euclidean", font_size=FONT_TABLE, z_index=2).next_to(rec_image, LEFT).shift(DOWN * 0.2)
        l6 = Tex(r"$L_1$", font_size=FONT_TABLE, z_index=2).next_to(rec_image, LEFT).shift(DOWN * 0.6)
        l7 = Tex(r"$L_\infty$", font_size=FONT_TABLE, z_index=2).next_to(rec_image, LEFT).shift(DOWN * 1)
        l8 = Tex(r"Absolute", font_size=FONT_TABLE, z_index=2).next_to(rec_image, LEFT).shift(DOWN * 1.5)

        labels_left = VGroup(l1, l2, l3, l4, l5, l6, l7, l8)
        Group(rec_image, labels_up, labels_left).move_to(ORIGIN).scale(1.05)

        self.play(
            FadeIn(rec_image),
            AnimationGroup(
                AnimationGroup(Create(slidetitle), Create(rec_label)),
                Write(labels_up),
                Write(labels_left),
                lag_ratio=0.5,
            ),
            run_time=1.5,
        )

        self.wait(0.1)
        self.next_slide()
        self.play(
            AnimationGroup(Indicate(l2)),
            AnimationGroup(l2.animate.set_color(ORANGE)),
        )

        self.wait(0.1)
        self.next_slide()
        self.play(
            AnimationGroup(Indicate(l7)),
            AnimationGroup(l7.animate.set_color(ORANGE)),
        )

        self.wait(0.1)
        self.next_slide()
        self.play(
            AnimationGroup(Indicate(l3)),
            AnimationGroup(l3.animate.set_color(ORANGE)),
        )

        self.wait(0.1)
        self.next_slide(auto_next=True)

        self.play(
            FadeOut(slidetitle),
            FadeOut(rec_label),
            FadeOut(rec_image),
            FadeOut(labels_up),
            FadeOut(labels_left),
        )
