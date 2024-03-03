import itertools
from typing import *

import numpy as np
import pandas as pd
from manim import *
from manim_slides import Slide
from torchvision.datasets import MNIST

from nn_core.common import PROJECT_ROOT

from latentcommunication_anims.utils import TARGET_COLORS, get_run_opt

DATASET = MNIST(root=PROJECT_ROOT / "data", train=True, download=True)
ROWS = 14
COLS = 14

LEFT_RUN_ID = "m5m4fznr"
RIGHT_RUN_ID = "1oktw6sl"

POINTS = 100
CHOSEN_SAMPLE = 2
ANCHORS_IDX = [0, 5]


class ParallelOpt(Slide):
    def build_optimization(self, axes, run_opt: pd.DataFrame, sample_ids: Sequence[int], max_lim: int):
        left_dots = []
        left_anims = []
        for sample_id in sample_ids[:max_lim]:
            point_df = run_opt[run_opt["sample_id"] == sample_id]

            points = np.asarray([(x, y, 0) for x, y in zip(point_df.dim_0, point_df.dim_1)])
            # points = ((points - points.min(0)) / (points.max(0) - points.min())) * 2 - 1
            points = axes.coords_to_point(points)
            zero_point = points[0]
            point_target = int(point_df[point_df["step"] == 0].target)
            dot = Dot(zero_point, stroke_width=1, fill_opacity=0.75, color=TARGET_COLORS[point_target], radius=0.05)
            dot.target = point_target
            dot.sample_id = point_df.sample_id
            left_dots.append(dot)

            path = VMobject()
            path.set_points_smoothly(points)
            left_anims.append(MoveAlongPath(dot, path, rate_func=rate_functions.smooth))
        return left_dots, left_anims

    def construct(self):
        self.next_slide()

        left_run_opt = get_run_opt(LEFT_RUN_ID)
        sample_ids = left_sample_ids = list(left_run_opt[left_run_opt["step"] == 0]["sample_id"])
        left_images = [
            ImageMobject(DATASET[sample_idx][0], image_mode="RGB") for sample_idx in left_sample_ids[: COLS * ROWS]
        ]
        left_group = Group(*left_images).arrange_in_grid(rows=ROWS, cols=COLS).to_edge(LEFT + DOWN)

        right_run_opt = get_run_opt(RIGHT_RUN_ID)
        perm = np.random.permutation(COLS * ROWS)
        right_group_ref = left_group.copy().to_edge(RIGHT + DOWN)

        mnist_left = Tex("MNIST").next_to(left_group, UP)
        self.play(
            Create(mnist_left),
            FadeIn(left_group, lag_ratio=0.1, run_time=1),
        )

        self.wait(0.1)
        self.next_slide()

        right_group = left_group.copy()
        anims = []
        for idx, p in enumerate(perm):
            anims.append(
                right_group.submobjects[idx].animate(run_time=3).move_to(right_group_ref.submobjects[p].get_center())
            )

        mnist_right = Tex("MNIST").next_to(right_group_ref, UP)
        self.play(Create(mnist_right), *anims)

        self.wait(0.1)
        self.next_slide()

        self.play(
            Uncreate(mnist_left),
            Uncreate(mnist_right),
            FadeOut(left_group, lag_ratio=0.05, run_time=1),
            FadeOut(right_group, lag_ratio=0.05, run_time=1),
        )
        x_range = (
            min(right_run_opt.dim_0.min(), left_run_opt.dim_0.min()),
            max(right_run_opt.dim_0.max(), left_run_opt.dim_0.max()),
            100,
        )
        y_range = (
            min(right_run_opt.dim_1.min(), left_run_opt.dim_1.min()),
            max(right_run_opt.dim_1.max(), left_run_opt.dim_1.max()),
            100,
        )

        NumberLine()
        left_axis = (
            Axes(
                x_range=x_range,
                y_range=y_range,
                # axis_config={"unit_size": 10},
                x_length=6,
                y_length=6,
                tips=True,
            )
            .to_edge(LEFT)
            .set_color(GRAY)
        )
        right_axis = (
            Axes(
                x_range=x_range,
                y_range=y_range,
                # axis_config={"unit_size": 10},
                x_length=6,
                y_length=6,
                tips=True,
            )
            .to_edge(RIGHT)
            .set_color(GRAY)
        )

        left_dots, left_anims = self.build_optimization(
            axes=left_axis, run_opt=left_run_opt, sample_ids=sample_ids, max_lim=POINTS
        )
        right_dots, right_anims = self.build_optimization(
            axes=right_axis, run_opt=right_run_opt, sample_ids=sample_ids, max_lim=POINTS
        )

        self.play(
            Create(left_axis),
            Create(right_axis),
        )
        # self.play(*(Create(x) for x in itertools.chain(left_dots, right_dots)), run_time=0.1)

        self.play(
            *left_anims,
            *right_anims,
            run_time=10,
        )

        self.wait(0.1)
        self.next_slide()

        different_text = Tex("...different latent spaces!").to_edge(DOWN)
        self.play(Create(different_text))

        self.wait(0.1)
        self.next_slide(auto_next=True)

        self.play(
            AnimationGroup(*(Uncreate(x) for x in left_dots), lag_ratio=0.2),
            AnimationGroup(*(Uncreate(x) for x in right_dots), lag_ratio=0.2),
            Uncreate(left_axis),
            Uncreate(right_axis),
            FadeOut(different_text),
            # Uncreate(midline),
            run_time=1.5,
        )


if __name__ == "__main__":
    ParallelOpt().construct()
