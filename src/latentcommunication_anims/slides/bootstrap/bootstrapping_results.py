from pathlib import Path
from typing import Sequence

import pandas as pd
from manim import *
from manim_slides import Slide

from nn_core.common import PROJECT_ROOT

folder_path: Path = PROJECT_ROOT / "data" / "bootstrapping" / "csv"
COLORS: dict = {1: RED_B, 2: BLUE_B, 3: GREEN_B, 4: PURPLE_A}

FONT_SIZE = 42

DOMAIN_X_COLOR = GREEN
DOMAIN_Y_COLOR = BLUE
SEED_COLOR = ORANGE
PERMUTATION_COLOR = PURPLE


class Count(Animation):
    def __init__(self, number: DecimalNumber, start: float, end: float, **kwargs) -> None:
        # Pass number as the mobject of the animation
        super().__init__(number, **kwargs)
        # Set start and end
        self.start = start
        self.end = end

    def interpolate_mobject(self, alpha: float) -> None:
        # Set value of DecimalNumber according to alpha
        value = self.start + (alpha * (self.end - self.start))
        self.mobject.set_value(value)


class BootstrappingResults(Slide):
    def build_optimization(
        self, axes, run_opt: pd.DataFrame, sample_ids: Sequence[int], max_lim: int, resolution: int = 1
    ):
        left_dots = []
        left_anims = []

        for sample_id in sample_ids[:max_lim]:
            point_df = run_opt[run_opt["point_id"] == sample_id]
            points = np.asarray([(x, y, 0) for x, y in zip(point_df.point_x, point_df.point_y)])[::resolution]
            points = axes.c2p(points)

            zero_point = points[0]
            color_point = point_df.iloc[0].manim_color

            dot = Dot(zero_point, stroke_width=1, fill_opacity=0.75, color=color_point, radius=0.05)
            dot.target = color_point
            dot.sample_id = point_df.point_id
            left_dots.append(dot)

            path = VMobject()
            path.set_points_smoothly(points)
            left_anims.append(MoveAlongPath(dot, path, rate_func=rate_functions.smooth))

        return left_dots, left_anims

    def construct(self):
        fix_axis = Axes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            x_length=5.5,
            y_length=5.5,
            tips=True,
        ).to_edge(LEFT, buff=LARGE_BUFF)

        fix_points = []
        fix_space = pd.read_csv(folder_path / "fix_space.csv")
        fix_space["manim_color"] = fix_space["point_color"].replace(COLORS)

        for _, row in fix_space.iterrows():
            fix_points.append(
                Dot(
                    point=fix_axis.coords_to_point(*[row["point_x"], row["point_y"], 0]),
                    color=row["manim_color"],
                    stroke_width=1,
                    radius=0.05,
                    fill_opacity=0.75,
                )
            )

        opt_axis = Axes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            x_length=5.5,
            y_length=5.5,
            tips=True,
        ).to_edge(RIGHT, buff=LARGE_BUFF)

        opt_space = pd.read_csv(folder_path / "opt_space.csv")
        opt_space["manim_color"] = opt_space["point_color"].replace(COLORS)
        sample_ids = opt_space["point_id"].unique()

        opt_points, opt_anims = self.build_optimization(
            axes=opt_axis, run_opt=opt_space, sample_ids=sample_ids, max_lim=700, resolution=20
        )

        label1 = Tex("Relative FastText", font_size=FONT_SIZE, color=DOMAIN_X_COLOR)
        label1.next_to(fix_axis, UP, buff=MED_LARGE_BUFF)

        label2 = Tex("Relative Word2Vec", font_size=FONT_SIZE, color=DOMAIN_Y_COLOR)
        label2.next_to(opt_axis, UP, buff=MED_LARGE_BUFF)

        label3 = Tex("Step:", font_size=FONT_SIZE)
        label3.next_to(opt_axis.get_critical_point(DL), DOWN)

        number = Integer().set_color(WHITE).scale(1)
        number.next_to(label3, RIGHT)

        self.play(
            AnimationGroup(
                FadeIn(label3),
                FadeIn(number),
                Create(fix_axis),
                Create(opt_axis),
                Create(label1),
                Create(label2),
            ),
            AnimationGroup(
                *(
                    AnimationGroup(
                        FadeIn(left_dot),
                        FadeIn(right_dot),
                    )
                    for left_dot, right_dot in zip(fix_points, opt_points)
                ),
                lag_ratio=0.1,
                run_time=1,
            ),
        )

        self.wait(0.1)
        self.next_slide()

        self.play(
            AnimationGroup(
                *opt_anims,
                Count(number, 0, 250),
                run_time=10,
            )
        )

        self.wait(0.1)
        self.next_slide(auto_next=True)

        self.play(
            AnimationGroup(
                FadeOut(fix_axis), FadeOut(opt_axis), FadeOut(label1), FadeOut(label2), FadeOut(label3), FadeOut(number)
            ),
            AnimationGroup(
                *(
                    AnimationGroup(
                        FadeOut(left_dot),
                        FadeOut(right_dot),
                    )
                    for left_dot, right_dot in zip(fix_points, opt_points)
                ),
            ),
        )

        self.wait(0.1)
