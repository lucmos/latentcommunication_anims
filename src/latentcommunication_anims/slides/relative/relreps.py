import itertools
from typing import *

import pandas as pd
from manim import *
from manim_slides import Slide
from powermanim.templates.reference import Reference
from powermanim.templates.sectiontitle import SectionTitle

from latentcommunication_anims.slides.parallel_opt import ANCHORS_IDX, CHOSEN_SAMPLE, LEFT_RUN_ID, POINTS, RIGHT_RUN_ID
from latentcommunication_anims.utils import TARGET_COLORS, get_run_opt


class RelReps(Slide):
    def resume_optimization(self, axes, run_opt: pd.DataFrame, sample_ids: Sequence[int], max_lim: int):
        dots = []
        for sample_id in sample_ids[:max_lim]:
            point_df = run_opt[run_opt["sample_id"] == sample_id].iloc[-1]
            point = np.asarray([point_df.dim_0, point_df.dim_1, 0])
            point = axes.coords_to_point([point])
            point_target = int(point_df.target)
            dot = Dot(point, stroke_width=1, fill_opacity=0.75, color=TARGET_COLORS[point_target], radius=0.05)
            dot.target = point_target
            dot.sample_id = point_df.sample_id
            dots.append(dot)
        return dots

    def build_relative_trasnform(
        self,
        dots,
        anchors_idx,
        alignement,
    ):
        distances = [
            Line(dots[anchor_idx], dots[CHOSEN_SAMPLE], color=dots[anchor_idx].color).set_opacity(0.5)
            for anchor_idx in anchors_idx
        ]
        mid_point_a = distances[0].get_midpoint()
        mid_point_b = distances[1].get_midpoint()
        mid_mid_point = Line(mid_point_a, mid_point_b).get_midpoint()

        dir_a = distances[0].copy().rotate(PI / 2)
        if np.linalg.norm(dir_a.get_end() - mid_mid_point) < np.linalg.norm(dir_a.get_start() - mid_mid_point):
            dir_a = dir_a.rotate(PI)
        dir_a = dir_a.get_unit_vector()

        dir_b = distances[1].copy().rotate(PI / 2)
        if np.linalg.norm(dir_b.get_end() - mid_mid_point) < np.linalg.norm(dir_b.get_start() - mid_mid_point):
            dir_b = dir_b.rotate(PI)
        dir_b = dir_b.get_unit_vector()

        num_a = DecimalNumber(distances[0].get_length(), font_size=32).next_to(
            distances[0].get_midpoint(), direction=dir_a
        )
        num_a.add_updater(
            lambda x: x.set_value(distances[0].get_length()).next_to(distances[0].get_midpoint(), direction=dir_a)
        )

        num_b = DecimalNumber(distances[1].get_length(), font_size=32).next_to(
            distances[1].get_midpoint(), direction=dir_b
        )
        num_b.add_updater(
            lambda x: x.set_value(distances[1].get_length()).next_to(distances[1].get_midpoint(), direction=dir_b)
        )

        #
        axes = Axes(
            x_range=[-0.5, 4, 10],
            y_range=[-0.5, 4, 10],
            # axis_config={"unit_size": 10},
            x_length=6,
            y_length=6,
            tips=True,
        )
        axes = axes.to_edge(alignement)

        def relative_transform(points, anchors_coords):
            for point in points:
                point: Dot
                point.generate_target()

                point_coords = []
                for anchor_coord in anchors_coords:
                    point_coords.append(np.linalg.norm(point.get_center() - anchor_coord))

                point.target.move_to(axes.coords_to_point([point_coords]))

        relative_transform(dots, [dots[x].get_center() for x in anchors_idx])
        vertical_line = axes.get_vertical_line(dots[CHOSEN_SAMPLE].target.get_center(), line_func=Line).set_opacity(0.5)
        horizontal_line = axes.get_horizontal_line(dots[CHOSEN_SAMPLE].target.get_center(), line_func=Line).set_opacity(
            0.5
        )

        return (
            distances,
            [num_a, num_b],
            axes,
            vertical_line,
            horizontal_line,
        )

    def construct(self):
        slide_title = SectionTitle(section_title="Universal Space")
        reference = Reference(
            text="Moschella*, Maiorca*, et al. “Relative representations enable zero-shot latent space communication”, ICLR 2023 (oral)",
            font_size=24,
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

        left_run_opt = get_run_opt(LEFT_RUN_ID)
        sample_ids = left_sample_ids = list(left_run_opt[left_run_opt["step"] == 0]["sample_id"])

        right_run_opt = get_run_opt(RIGHT_RUN_ID)

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

        left_dots = self.resume_optimization(
            axes=left_axis, run_opt=left_run_opt, sample_ids=sample_ids, max_lim=POINTS
        )
        right_dots = self.resume_optimization(
            axes=right_axis, run_opt=right_run_opt, sample_ids=sample_ids, max_lim=POINTS
        )

        self.play(
            Create(left_axis),
            Create(right_axis),
        )

        self.play(
            AnimationGroup(
                *(FadeIn(dot) for dot in itertools.chain(left_dots)),
                lag_ratio=0.01,
            ),
            AnimationGroup(
                *(FadeIn(dot) for dot in itertools.chain(right_dots)),
                lag_ratio=0.01,
            ),
            run_time=1.5,
        )

        self.wait(0.1)
        self.next_slide()

        opacity_anim = []
        for dot in itertools.chain(left_dots, right_dots, left_axis, right_axis):
            opacity_anim.append(dot.animate.set_opacity(0.15))
        self.play(
            AnimationGroup(
                AnimationGroup(*opacity_anim),
                lag_ratio=0.25,
                run_time=1,
            ),
        )

        anchors_transform = []
        for anchors_idx in ANCHORS_IDX:
            for dots in (left_dots, right_dots):
                anchor_dot = dots[anchors_idx]
                anchors_transform.append(
                    Transform(
                        anchor_dot,
                        Star(
                            fill_opacity=0.5,
                            outer_radius=0.1,
                            color=anchor_dot.color,
                        ).move_to(anchor_dot.get_center()),
                    )
                )
        self.play(*anchors_transform)

        self.wait()
        self.next_slide()

        self.play(
            *(dot.animate.scale(1.25).set_opacity(1) for dot in [left_dots[CHOSEN_SAMPLE], right_dots[CHOSEN_SAMPLE]])
        )

        self.wait()
        self.next_slide()

        self.play(
            Uncreate(left_axis),
            Uncreate(right_axis),
        )

        left_distances, left_nums, left_axis, left_vertical_line, left_horizontal_line = self.build_relative_trasnform(
            left_dots, anchors_idx=ANCHORS_IDX, alignement=LEFT
        )
        (
            right_distances,
            right_nums,
            right_axis,
            right_vertical_line,
            right_horizontal_line,
        ) = self.build_relative_trasnform(right_dots, anchors_idx=ANCHORS_IDX, alignement=RIGHT)
        for n in itertools.chain(left_nums, right_nums):
            n.update(0)
            self.add(n)

        self.play(
            *(Create(l, run_time=4) for l in itertools.chain(left_distances, right_distances)),
        )

        for n in itertools.chain(left_nums, right_nums):
            n.clear_updaters()

        self.wait()
        self.next_slide()

        relative_anims = []
        for dots, ax, dist, num, vline, hline in zip(
            (left_dots, right_dots),
            (left_axis, right_axis),
            (left_distances, right_distances),
            (left_nums, right_nums),
            (left_vertical_line, right_vertical_line),
            (left_horizontal_line, right_horizontal_line),
        ):
            relative_anims.extend(MoveToTarget(x) for x in dots)
            relative_anims.extend(
                ReplacementTransform(dots[anch], x.set_color(dots[anch].get_color()))
                for anch, x in zip(ANCHORS_IDX, [ax.x_axis, ax.y_axis])
            )

            relative_anims.extend(x.animate.become(y.set_color(x.get_color())) for x, y in zip(dist, [hline, vline]))
            relative_anims.append(num[0].animate.next_to(hline, LEFT))
            relative_anims.append(num[1].animate.next_to(vline, DOWN))

        self.play(*relative_anims, run_time=5)

        self.wait()
        self.next_slide()

        opacity_anim = []
        for dot in itertools.chain(left_dots, right_dots):
            opacity_anim.append(dot.animate.set_opacity(0.75))
        for ax in itertools.chain(left_axis, right_axis):
            opacity_anim.append(ax.animate.set_opacity(1))
        self.play(
            *opacity_anim,
            *(Uncreate(x) for x in itertools.chain(left_distances, right_distances, left_nums, right_nums)),
        )

        self.wait()
        self.next_slide(auto_next=True)

        self.play(
            AnimationGroup(*(Uncreate(x) for x in left_dots), lag_ratio=0.2),
            AnimationGroup(*(Uncreate(x) for x in right_dots), lag_ratio=0.2),
            Uncreate(left_axis),
            Uncreate(right_axis),
            # Uncreate(midline),
            run_time=2,
        )

        self.wait(0.1)
