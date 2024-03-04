from manim import *
from manim_slides import Slide

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
        section_slide(self, "Semantic Correspondence")

        left_space = Tex("Latent Space 1", font_size=FONT_SIZE).to_edge(UP)
        left_e = Ellipse(width=2.5, height=4.5, color=WHITE)
        left_space.to_corner(UL, buff=LARGE_BUFF)
        left_e.next_to(left_space, DOWN, buff=MED_LARGE_BUFF)

        right_space = Tex("Latent Space 2", font_size=FONT_SIZE).to_corner(UR, buff=LARGE_BUFF)
        right_e = Ellipse(width=2.5, height=4.5, color=WHITE).next_to(right_space, DOWN, buff=MED_LARGE_BUFF)
        self.play(
            Create(right_e),
            Create(right_space),
            Create(left_space),
            Create(left_e),
        )

        self.wait(0.1)
        self.next_slide()

        leftdots = [
            Star(color=WHITE, fill_opacity=0.5, outer_radius=0.1, z_index=2).move_to([-5, 1.5, 0]),
            Star(color=WHITE, fill_opacity=0.5, outer_radius=0.1, z_index=2).move_to([-4.5, -1, 0]),
            Star(color=WHITE, fill_opacity=0.5, outer_radius=0.1, z_index=2).move_to([-4.75, -2, 0]),
        ]
        rightdots = [
            Star(color=WHITE, fill_opacity=0.5, outer_radius=0.1, z_index=2).move_to([4, 1, 0]),
            Star(color=WHITE, fill_opacity=0.5, outer_radius=0.1, z_index=2).move_to([5, 0, 0]),
            Star(color=WHITE, fill_opacity=0.5, outer_radius=0.1, z_index=2).move_to([5.5, -1, 0]),
        ]

        self.play(
            AnimationGroup(
                *[AnimationGroup(Create(dot1), Create(dot2)) for dot1, dot2 in zip(leftdots, rightdots)],
                lag_ratio=0.5,
            )
        )

        self.wait(0.1)
        self.next_slide()

        arc0 = ArcBetweenPoints(
            leftdots[0].get_center(),
            rightdots[0].get_center(),
            angle=-TAU / 8,
            stroke_width=3,
        ).set_color([CORRESPONDENCE_COLOR[0], BLACK, BLACK, CORRESPONDENCE_COLOR[0]])

        arc1 = ArcBetweenPoints(
            leftdots[1].get_center(),
            rightdots[1].get_center(),
            angle=-TAU / 16,
            stroke_width=3,
        ).set_color([CORRESPONDENCE_COLOR[1], BLACK, BLACK, CORRESPONDENCE_COLOR[1]])

        arc2 = ArcBetweenPoints(
            leftdots[2].get_center(),
            rightdots[2].get_center(),
            angle=TAU / 32,
            stroke_width=3,
        ).set_color([CORRESPONDENCE_COLOR[2], BLACK, BLACK, CORRESPONDENCE_COLOR[2]])

        img0 = ImageMobject(CAT_IMG).scale(0.05).next_to(arc0, ORIGIN, buff=0).shift(0.85 * UP)
        img1 = ImageMobject(ELE_IMG).scale(0.225).next_to(arc1, ORIGIN, buff=0).shift(0.4 * UP)
        img2 = ImageMobject(KAK_IMG).scale(0.15).next_to(arc2, ORIGIN, buff=0).shift(0.45 * DOWN)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    AnimationGroup(
                        GrowFromPoint(arc0, point=img0.get_center()),
                        GrowFromPoint(img0, point=img0.get_center()),
                    ),
                    AnimationGroup(
                        leftdots[0].animate.set_color(CORRESPONDENCE_COLOR[0]),
                        rightdots[0].animate.set_color(CORRESPONDENCE_COLOR[0]),
                    ),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    AnimationGroup(
                        GrowFromPoint(arc1, point=img1.get_center()),
                        GrowFromPoint(img1, point=img1.get_center()),
                    ),
                    AnimationGroup(
                        leftdots[1].animate.set_color(CORRESPONDENCE_COLOR[1]),
                        rightdots[1].animate.set_color(CORRESPONDENCE_COLOR[1]),
                    ),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    AnimationGroup(
                        GrowFromPoint(arc2, point=img2.get_center()),
                        GrowFromPoint(img2, point=img2.get_center()),
                    ),
                    AnimationGroup(
                        leftdots[2].animate.set_color(CORRESPONDENCE_COLOR[2]),
                        rightdots[2].animate.set_color(CORRESPONDENCE_COLOR[2]),
                    ),
                    lag_ratio=0.5,
                ),
                lag_ratio=0.7,
            ),
            run_time=4,
        )

        partial_correspondence = (
            Tex("A partial semantic correspondence!", font_size=FONT_SIZE).to_edge(DOWN).set_opacity(0.9)
        )
        self.play(Create(partial_correspondence))

        self.wait(0.1)
        self.next_slide()

        left_sample = Dot(color=WHITE, z_index=2).move_to([-5, 0, 0])
        right_sample = Dot(color=WHITE, z_index=2).move_to([5.5, 0.5, 0])
        self.play(
            Create(left_sample),
            Create(right_sample),
        )

        self.wait(0.1)
        self.next_slide()

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

        self.play(
            GrowFromPoint(lines0[0], point_color=CORRESPONDENCE_COLOR[0], point=left_sample.get_center()),
            GrowFromPoint(lines0[1], point_color=CORRESPONDENCE_COLOR[0], point=right_sample.get_center()),
        )

        self.wait(0.1)
        self.next_slide()

        self.play(
            AnimationGroup(
                AnimationGroup(
                    GrowFromPoint(lines1[0], point_color=CORRESPONDENCE_COLOR[1], point=left_sample.get_center()),
                    GrowFromPoint(lines1[1], point_color=CORRESPONDENCE_COLOR[1], point=right_sample.get_center()),
                ),
                AnimationGroup(
                    GrowFromPoint(lines2[0], point_color=CORRESPONDENCE_COLOR[2], point=left_sample.get_center()),
                    GrowFromPoint(lines2[1], point_color=CORRESPONDENCE_COLOR[2], point=right_sample.get_center()),
                ),
                lag_ratio=0.5,
            ),
            run_time=2,
        )

        self.wait(0.1)
        self.next_slide(auto_next=True)

        self.play(
            AnimationGroup(
                Uncreate(partial_correspondence),
                AnimationGroup(
                    Uncreate(arc0),
                    FadeOut(img0, run_time=0.5),
                    Uncreate(lines0),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    Uncreate(arc1),
                    FadeOut(img1, run_time=0.5),
                    Uncreate(lines1),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    Uncreate(arc2),
                    FadeOut(img2, run_time=0.5),
                    Uncreate(lines2),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    Uncreate(left_sample),
                    Uncreate(right_sample),
                ),
                AnimationGroup(
                    *(Uncreate(x) for x in leftdots),
                    *(Uncreate(x) for x in rightdots),
                ),
                AnimationGroup(
                    Uncreate(left_space),
                    Uncreate(right_space),
                    Uncreate(left_e),
                    Uncreate(right_e),
                ),
                lag_ratio=0.1,
            ),
            run_time=2,
        )
