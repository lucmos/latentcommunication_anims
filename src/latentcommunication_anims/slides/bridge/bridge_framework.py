import random

from lightning import seed_everything
from manim import *
from manim.mobject.geometry.line import Arrow
from manim.mobject.geometry.polygram import Polygon
from manim_slides import Slide

from latentcommunication_anims.utils import seed_everything

FONT_SIZE = 40

LABEL_SIZE = 30
OBJ_OPACITY = 0.5

ENC1_COLOR = PURPLE_A
ENC2_COLOR = TEAL_A

LS1_COLOR = MAROON_A
LS2_COLOR = GOLD_A
LS3_COLOR = BLUE_A

UNIFIED_COLOR = MAROON_A

seed_everything(42)


class LatentSpace(SurroundingRectangle):
    def __init__(self, mobject, num_puffs=10, puffiness=0.4, puff_angle=10 * DEGREES, randomness=0.1, **kwargs):
        super().__init__(mobject, **kwargs)

        def r():
            # Random multiplier
            return 1 + random.random() * randomness

        def rp(p):
            # Randomize proportion
            p += (random.random() - 0.5) * 2 * randomness / 10
            return p % 1

        points = [self.point_from_proportion(rp(i / num_puffs)) for i in range(num_puffs)]
        points += [points[0]]
        bezier_points = []
        for s, e in zip(points, points[1:]):
            vect = e - s
            normal = rotate_vector(vect, -90 * DEGREES)
            c1 = s + r() * puffiness * rotate_vector(normal, puff_angle * r())
            c2 = e + r() * puffiness * rotate_vector(normal, -puff_angle * r())
            bezier_points.extend([s, c1, c2, e])
        self.points = bezier_points


class BridgeFramework(Slide):
    def construct(self):
        slidetitle = Tex("Product Space of Invariant Components").to_edge(UP)

        enc = (
            Polygon(
                2 * UP + LEFT, RIGHT + UP, RIGHT + DOWN, 2 * DOWN + LEFT, fill_opacity=OBJ_OPACITY, color=ENC1_COLOR
            )
            .scale(0.5)
            .shift(LEFT * 5.2)
        )

        enc_label = Tex("Encoder", z_index=2, font_size=LABEL_SIZE).next_to(enc, DOWN)

        enc_in_arrow = Arrow(
            LEFT / 2,
            RIGHT / 2,
        ).next_to(enc, LEFT)

        enc_in_label = Tex("$\mathcal{X}$", z_index=2, font_size=LABEL_SIZE).next_to(enc_in_arrow, LEFT)

        enc_lat_arrow = Arrow(
            LEFT / 2,
            RIGHT / 2,
        ).next_to(enc, RIGHT)

        enc_ls_text = Tex(
            "LS",
            color=WHITE,
            font_size=10,
        ).next_to(enc_lat_arrow, RIGHT, buff=0.8)

        enc_ls = LatentSpace(enc_ls_text, buff=0.4, color=ENC1_COLOR, fill_opacity=OBJ_OPACITY)

        self.play(
            AnimationGroup(FadeIn(slidetitle), run_time=0.5),
            AnimationGroup(
                AnimationGroup(
                    Create(enc),
                    Create(enc_label),
                    Create(enc_in_arrow),
                    Create(enc_in_label),
                    Create(enc_lat_arrow),
                    Create(enc_ls),
                    lag_ratio=0.5,
                ),
                run_time=1.5,
            ),
        )

        self.wait(0.1)
        self.next_slide()

        rel_arrow = (
            Arrow(
                LEFT / 2,
                RIGHT / 2,
            )
            .next_to(enc_ls, RIGHT)
            .shift(RIGHT * 0.2)
        )

        rel_label = Tex("RR", font_size=LABEL_SIZE, color=WHITE).next_to(rel_arrow, UP)

        cos_text = Tex(
            "Cosine",
            color=WHITE,
            font_size=20,
            z_index=2,
        ).next_to(rel_arrow, RIGHT * 3)

        cos_ls = LatentSpace(cos_text, buff=0.3, color=LS1_COLOR, fill_opacity=OBJ_OPACITY, z_index=-1)

        self.play(
            Create(rel_arrow),
            Create(rel_label),
            Create(cos_text),
            Create(cos_ls),
        )

        self.wait(0.1)
        self.next_slide()

        euc_text = (
            Tex(
                "Euclidean",
                color=WHITE,
                font_size=20,
            )
            .next_to(cos_ls, UP)
            .shift(UP * 0.4)
        )

        l1_text = (
            Tex(
                "$L_1$",
                color=WHITE,
                font_size=20,
            )
            .next_to(cos_ls, DOWN)
            .shift(DOWN * 0.4)
        )

        euc_ls = LatentSpace(euc_text, buff=0.3, color=LS2_COLOR, fill_opacity=OBJ_OPACITY, z_index=-1)
        l1_ls = LatentSpace(l1_text, buff=0.3, color=LS3_COLOR, fill_opacity=OBJ_OPACITY, z_index=-1)

        euc_arrow = Arrow(
            start=[-2.4, 0, 0],
            end=[-1.6, 1, 0],
        )

        l1_arrow = Arrow(
            start=[-2.4, 0, 0],
            end=[-1.6, -1, 0],
        )

        more = Tex("...", font_size=60, color=WHITE).next_to(cos_ls, DOWN).shift(DOWN * 1.1)

        self.play(
            Create(euc_arrow),
            Create(l1_arrow),
            Create(euc_text),
            Create(euc_ls),
            Create(l1_text),
            Create(l1_ls),
            Create(more),
            rel_label.animate.shift(UP),
            # FadeOut(rel_label),
        )

        self.wait(0.1)
        self.next_slide()

        # brace = BraceBetweenPoints(
        #     [0.3, -1.6, 0],
        #     [0.3, 1.6, 0],
        # )

        cos_agg_arrow = (
            Arrow(
                LEFT / 2,
                RIGHT / 2,
            )
            .next_to(cos_ls, RIGHT)
            .shift(RIGHT * 0.1)
        )

        euc_agg_arrow = Arrow(
            start=[0.1, 1.1, 0],
            end=[0.85, 0, 0],
        )

        l1_agg_arrow = Arrow(
            start=[0.1, -1.1, 0],
            end=[0.85, 0, 0],
        )

        aggregator = (
            Rectangle(height=2, width=1, fill_opacity=OBJ_OPACITY).next_to(cos_agg_arrow, RIGHT).shift(RIGHT * 0.1)
        )
        agg_label = Tex("Aggregation", font_size=LABEL_SIZE, color=WHITE).next_to(aggregator, DOWN)

        deepset = Tex("DeepSet", font_size=LABEL_SIZE, color=WHITE).next_to(agg_label, DOWN * 3.5)
        agg_arrow = Arrow(start=agg_label.get_center(), end=deepset.get_center())

        self.play(
            AnimationGroup(
                Create(cos_agg_arrow),
                Create(euc_agg_arrow),
                Create(l1_agg_arrow),
                Create(agg_label),
                Create(aggregator),
                Create(agg_arrow),
                Create(deepset),
                lag_ratio=0.5,
            ),
            run_time=1,
        )

        self.wait(0.1)
        self.next_slide()

        dec_arrow = Arrow(
            LEFT / 2,
            RIGHT / 2,
        ).next_to(aggregator, RIGHT)

        dec = (
            Polygon(
                RIGHT + 2 * UP, RIGHT + 2 * DOWN, DOWN + LEFT, UP + LEFT, fill_opacity=OBJ_OPACITY, color=ENC1_COLOR
            )
            .scale(0.5)
            .next_to(dec_arrow, RIGHT)
        )

        mini_decoder = Polygon(
            RIGHT + 0.5 * UP, RIGHT + 0.5 * DOWN, DOWN + LEFT, UP + LEFT, fill_opacity=OBJ_OPACITY, color=ENC1_COLOR
        )
        mini_decoder.add_updater(lambda x: x.align_to(dec, LEFT))

        dec_label = Tex("Decoder", z_index=2, font_size=LABEL_SIZE).next_to(dec, DOWN)

        out_arrow = Arrow(
            LEFT / 2,
            RIGHT / 2,
        ).next_to(dec, RIGHT)

        out_label1 = Tex("Downstream", z_index=2, font_size=LABEL_SIZE).next_to(out_arrow, RIGHT)
        out_label2 = Tex("Task", z_index=2, font_size=LABEL_SIZE).next_to(out_label1, DOWN)

        self.play(
            Create(dec_arrow),
            Create(dec),
            Create(dec_label),
            Create(out_arrow),
            Create(out_label1),
            Create(out_label2),
        )

        self.wait(0.1)
        self.next_slide(auto_next=True)

        self.play(*(FadeOut(x) for x in self.mobjects))
