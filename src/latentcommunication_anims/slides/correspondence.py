import typing as T
from functools import partial

from manim import *
from manim_slides.slide import Slide
from powermanim import GroupActivable, ImageAutoActivable, VActivable, VAutoActivable

from nn_core.common import PROJECT_ROOT

from latentcommunication_anims.utils import section_slide

FONT_SIZE = 42

CORRESPONDENCE_COLOR = [
    GREEN,
    YELLOW,
    BLUE,
]

CAT_IMG = PROJECT_ROOT / "data" / "assets" / "cat2.jpg"
ELE_IMG = PROJECT_ROOT / "data" / "assets" / "elephant.jpg"
KAK_IMG = PROJECT_ROOT / "data" / "assets" / "kakapo.jpg"


class Correspondence(Slide):
    def construct(self):
        # section_slide(self, "Semantic Correspondence")
        slide_title = Tex("Intuition").to_edge(UP)

        left_space = Tex("Latent Space 1", font_size=FONT_SIZE).to_edge(UP)
        left_e = Ellipse(width=2.5, height=4.5, color=WHITE)
        left_space.to_corner(UL, buff=LARGE_BUFF)
        left_e.next_to(left_space, DOWN, buff=MED_LARGE_BUFF)

        right_space = Tex("Latent Space 2", font_size=FONT_SIZE).to_corner(UR, buff=LARGE_BUFF)
        right_e = Ellipse(width=2.5, height=4.5, color=WHITE).next_to(right_space, DOWN, buff=MED_LARGE_BUFF)
        leftdots = [
            Star(color=WHITE, fill_opacity=0.5, outer_radius=0.1, z_index=2).move_to([-5, 1.5, 0]),  # type: ignore
            Star(color=WHITE, fill_opacity=0.5, outer_radius=0.1, z_index=2).move_to([-4.5, -1, 0]),  # type: ignore
            Star(color=WHITE, fill_opacity=0.5, outer_radius=0.1, z_index=2).move_to([-4.75, -2, 0]),  # type: ignore
        ]
        rightdots = [
            Star(color=WHITE, fill_opacity=0.5, outer_radius=0.1, z_index=2).move_to([4, 1, 0]),  # type: ignore
            Star(color=WHITE, fill_opacity=0.5, outer_radius=0.1, z_index=2).move_to([5, 0, 0]),  # type: ignore
            Star(color=WHITE, fill_opacity=0.5, outer_radius=0.1, z_index=2).move_to([5.5, -1, 0]),  # type: ignore
        ]

        arc0 = ArcBetweenPoints(
            leftdots[0].get_center(),
            rightdots[0].get_center(),
            angle=-TAU / 8,
            stroke_width=3,
        ).set_color(
            [CORRESPONDENCE_COLOR[0], BLACK, BLACK, CORRESPONDENCE_COLOR[0]]  # type: ignore
        )

        arc1 = ArcBetweenPoints(
            leftdots[1].get_center(),
            rightdots[1].get_center(),
            angle=-TAU / 16,
            stroke_width=3,
        ).set_color(
            [CORRESPONDENCE_COLOR[1], BLACK, BLACK, CORRESPONDENCE_COLOR[1]]  # type: ignore
        )

        arc2 = ArcBetweenPoints(
            leftdots[2].get_center(),
            rightdots[2].get_center(),
            angle=TAU / 32,
            stroke_width=3,
        ).set_color(
            [CORRESPONDENCE_COLOR[2], BLACK, BLACK, CORRESPONDENCE_COLOR[2]]  # type: ignore
        )

        img0 = ImageMobject(CAT_IMG, z_index=10).scale(0.05).next_to(arc0, ORIGIN, buff=0).shift(0.85 * UP)
        img1 = ImageMobject(ELE_IMG, z_index=10).scale(0.225).next_to(arc1, ORIGIN, buff=0).shift(0.4 * UP)
        img2 = ImageMobject(KAK_IMG, z_index=10).scale(0.15).next_to(arc2, ORIGIN, buff=0).shift(0.45 * DOWN)

        partial_correspondence = (
            Tex("$\pi$ is an observable semantic correspondence!", font_size=FONT_SIZE).to_edge(DOWN).set_opacity(0.9)
        )
        left_sample = Dot(color=WHITE, z_index=2).move_to([-5, 0, 0])
        right_sample = Dot(color=WHITE, z_index=2).move_to([5.5, 0.5, 0])

        lines0 = VGroup(
            DashedLine(
                left_sample.get_center(),
                leftdots[0].get_center(),
                color=CORRESPONDENCE_COLOR[0],
                stroke_width=DEFAULT_STROKE_WIDTH * 2,
            ),
            DashedLine(
                right_sample.get_center(),
                rightdots[0].get_center(),
                color=CORRESPONDENCE_COLOR[0],
                stroke_width=DEFAULT_STROKE_WIDTH * 2,
            ),
        ).set_opacity(0.5)

        lines1 = VGroup(
            DashedLine(
                left_sample.get_center(),
                leftdots[1].get_center(),
                color=CORRESPONDENCE_COLOR[1],
                stroke_width=DEFAULT_STROKE_WIDTH * 2,
            ),
            DashedLine(
                right_sample.get_center(),
                rightdots[1].get_center(),
                color=CORRESPONDENCE_COLOR[1],
                stroke_width=DEFAULT_STROKE_WIDTH * 2,
            ),
        ).set_opacity(0.5)

        lines2 = VGroup(
            DashedLine(
                left_sample.get_center(),
                leftdots[2].get_center(),
                color=CORRESPONDENCE_COLOR[2],
                stroke_width=DEFAULT_STROKE_WIDTH * 2,
            ),
            DashedLine(
                right_sample.get_center(),
                rightdots[2].get_center(),
                color=CORRESPONDENCE_COLOR[2],
                stroke_width=DEFAULT_STROKE_WIDTH * 2,
            ),
        ).set_opacity(0.5)

        INACTIVE = 0.15

        image_highlightable = partial(
            ImageAutoActivable,
            scale_active=None,
            active_opacity=1,
            inactive_opacity=INACTIVE,
            activation_anim_run_time=0.5,
            deactivation_anim_run_time=0.5,
        )
        label_highlightable = partial(
            VAutoActivable,
            scale_active=None,
            active_fill_opacity=1.0,
            inactive_fill_opacity=INACTIVE,
            active_stroke_opacity=1.0,
            inactive_stroke_opacity=INACTIVE,
            activation_anim_run_time=0.5,
            deactivation_anim_run_time=0.5,
        )
        shape_highlightable = partial(
            VAutoActivable,
            scale_active=None,
            active_fill_opacity=0,
            inactive_fill_opacity=0,
            active_stroke_opacity=1.0,
            inactive_stroke_opacity=INACTIVE,
            activation_anim_run_time=0.5,
            deactivation_anim_run_time=0.5,
        )
        diagram = GroupActivable(
            label_highlightable(left_space, group=0),
            shape_highlightable(left_e, group=0),
            label_highlightable(right_space, group=0),
            shape_highlightable(right_e, group=0),
            label_highlightable(VGroup(*leftdots), group=1),
            label_highlightable(VGroup(*rightdots), group=1),
            shape_highlightable(arc0, group=2),
            shape_highlightable(arc1, group=2),
            shape_highlightable(arc2, group=2),
            image_highlightable(img0, group=2),
            image_highlightable(img1, group=2),
            image_highlightable(img2, group=2),
            VAutoActivable(
                partial_correspondence,
                group=3,
                scale_active=None,
                active_fill_opacity=1.0,
                inactive_fill_opacity=0,
                active_stroke_opacity=1.0,
                inactive_stroke_opacity=0,
                activation_anim_run_time=0.5,
                deactivation_anim_run_time=0.5,
            ),
            label_highlightable(left_sample, group=4),
            label_highlightable(right_sample, group=4),
            label_highlightable(lines0, group=4),
            label_highlightable(lines1, group=5),
            label_highlightable(lines2, group=6),
        ).scale(0.9)

        self.play(AnimationGroup(FadeIn(slide_title), FadeIn(diagram), lag_ratio=0.25))

        for i in range(diagram.ngroups):
            self.play(diagram.also_next())
            self.wait(0.1)
            self.next_slide(auto_next=i == diagram.ngroups - 1)

        self.play(FadeOut(diagram), FadeOut(slide_title))
