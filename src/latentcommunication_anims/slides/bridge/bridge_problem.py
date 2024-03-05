import random
from typing import *

from manim import *
from manim.mobject.geometry.line import Arrow
from manim.mobject.geometry.polygram import Polygon
from manim_slides import Slide
from powermanim.templates.reference import Reference
from powermanim.templates.sectiontitle import SectionTitle

FONT_SIZE = 38

LABEL_SIZE = 30
OBJ_OPACITY = 0.5

ENC1_COLOR = PURPLE_A
ENC2_COLOR = TEAL_A
UNIFIED_COLOR = MAROON_A

DISABLED_OPACITY = 0.4
FONT_SIZE = 40
SCALE_ACTIVE = 1
LINE_SPACING = 0.3


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


class BridgeProblem(Slide):
    def construct(self) -> None:
        slide_title = SectionTitle(section_title="Unknown Latent Transformation")
        reference = Reference(
            text="Cannistraci, Moschella, et al. “From Bricks to Bridges: Product of Invariances to Enhance Latent Space Communication”, ICLR 2024 (spotlight)",
            font_size=20,
        )
        self.play(
            slide_title.show(),
            FadeIn(reference),
        )

        self.wait(0.1)
        self.next_slide()

        self.play(
            slide_title.hide(),
            FadeOut(reference),
        )
        # ---

        #  encoder 1
        enc1 = (
            Polygon(
                2 * UP + LEFT, RIGHT + UP, RIGHT + DOWN, 2 * DOWN + LEFT, fill_opacity=OBJ_OPACITY, color=ENC1_COLOR
            )
            .scale(0.5)
            .shift(UP * 2)
            .shift(LEFT * 1.7)
        )

        enc1_label = Tex("Encoder", z_index=2, font_size=LABEL_SIZE).next_to(enc1, DOWN)

        #  encoder 2
        enc2 = (
            Polygon(
                2 * UP + LEFT, RIGHT + UP, RIGHT + DOWN, 2 * DOWN + LEFT, fill_opacity=OBJ_OPACITY, color=ENC2_COLOR
            )
            .scale(0.5)
            .next_to(enc1_label, DOWN, buff=LARGE_BUFF)
        )

        enc2_label = Tex("Encoder", z_index=2, font_size=LABEL_SIZE).next_to(enc2, DOWN)

        self.play(
            Create(enc1),
            Create(enc1_label),
            Create(enc2),
            Create(enc2_label),
        )

        #  ENCODER 1
        enc1_in_arrow = Arrow(
            LEFT / 2,
            RIGHT / 2,
        ).next_to(enc1, LEFT)

        enc1_in_label = Tex("$\mathbf{X}$", z_index=2, font_size=LABEL_SIZE).next_to(enc1_in_arrow, LEFT)

        #  ENCODER 2
        enc2_in_arrow = Arrow(
            LEFT / 2,
            RIGHT / 2,
        ).next_to(enc2, LEFT)

        enc2_in_label = Tex("$\mathbf{Y}$", z_index=2, font_size=LABEL_SIZE).next_to(enc2_in_arrow, LEFT)

        enc1_lat_arrow = Arrow(
            LEFT / 2,
            RIGHT / 2,
        ).next_to(enc1, RIGHT)

        enc2_lat_arrow = Arrow(
            LEFT / 2,
            RIGHT / 2,
        ).next_to(enc2, RIGHT)

        enc1_ls_text = Tex(
            "Latent Space",
            color=WHITE,
            font_size=10,
        ).next_to(enc1_lat_arrow, RIGHT, buff=1.1)

        enc2_ls_text = Tex(
            "Latent Space",
            color=WHITE,
            font_size=10,
        ).next_to(enc2_lat_arrow, RIGHT, buff=1.1)

        enc1_ls = LatentSpace(enc1_ls_text, buff=0.7, color=ENC1_COLOR, fill_opacity=OBJ_OPACITY)
        enc2_ls = LatentSpace(enc2_ls_text, buff=0.7, color=ENC2_COLOR, fill_opacity=OBJ_OPACITY)

        enc1_ls_label = Tex("Latent Space", font_size=LABEL_SIZE, color=WHITE).next_to(enc1_label, RIGHT, buff=1.25)
        enc2_ls_label = Tex("Latent Space", font_size=LABEL_SIZE, color=WHITE).next_to(enc2_label, RIGHT, buff=1.25)

        start = [1, 0.6, 0]
        end = [1, -0.6, 0]

        transf_arrow = DoubleArrow(start, end)
        transf_label = Tex("{{ $\mathbb{T}$ }}", font_size=LABEL_SIZE).next_to(transf_arrow, RIGHT)

        self.play(
            AnimationGroup(
                Create(enc1_in_arrow),
                Create(enc1_in_label),
                Create(enc2_in_arrow),
                Create(enc2_in_label),
                Create(enc1_lat_arrow),
                Create(enc2_lat_arrow),
                Create(enc1_ls),
                Create(enc2_ls),
                Create(enc1_ls_label),
                Create(enc2_ls_label),
                AnimationGroup(GrowArrow(transf_arrow), Create(transf_label)),
                lag_ratio=0.1,
            )
        )

        pipeline = VGroup(
            enc1_in_arrow,
            enc1_in_label,
            enc2_in_arrow,
            enc2_in_label,
            enc1,
            enc1_label,
            enc2,
            enc2_label,
            enc1_lat_arrow,
            enc2_lat_arrow,
            enc1_ls,
            enc2_ls,
            enc1_ls_label,
            enc2_ls_label,
            transf_arrow,
            transf_label,
        )

        self.wait(0.1)
        self.next_slide()

        myBaseTemplate = TexTemplate(documentclass="\documentclass[preview]{standalone}")
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        question = (
            VGroup(
                Tex("Challenge", font_size=int(FONT_SIZE * 1.25)),
                Tex("determine a priori the", font_size=FONT_SIZE),
                Tex("transformations class {{ $\mathbb{T}$ }}", font_size=FONT_SIZE),
                Tex("connecting latent spaces!", font_size=FONT_SIZE),
            )
            .arrange(DOWN)
            .shift(RIGHT * 3.5)
        )

        self.play(AnimationGroup(pipeline.animate.shift(LEFT * 2), Create(question)))

        self.wait(0.1)
        self.next_slide(auto_next=True)
        self.play(AnimationGroup(FadeOut(pipeline), FadeOut(transf_arrow), FadeOut(transf_label), FadeOut(question)))
