import itertools
from typing import *

import numpy as np
import pandas as pd
import torch
from manim import *
from manim_slides import Slide
from powermanim.templates.reference import Reference
from powermanim.templates.sectiontitle import SectionTitle
from scipy.stats import ortho_group

from latentcommunication_anims.slides.parallel_opt import LEFT_RUN_ID, POINTS, RIGHT_RUN_ID
from latentcommunication_anims.utils import TARGET_COLORS, get_run_opt, seed_everything

dtype = torch.float32


DOT_RADIUS: float = 0.08


def build_space(random: bool = False, N: int = 2):
    x = torch.linspace(-1, 1, 7, dtype=dtype)
    y = torch.linspace(-1, 1, 7, dtype=dtype)

    xx, yy = torch.meshgrid(x, y, indexing="ij")

    x_grid = torch.stack([xx, yy], dim=-1).reshape(-1, N)
    if random:
        x_grid *= torch.randn_like(x_grid)

    return x_grid


def svd_translation(A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
    # """Compute the translation vector that aligns A to B using SVD."""
    assert A.size(1) == B.size(1)
    u, s, vt = torch.svd((B.T @ A).T)
    R = u @ vt.T
    return R, s


def iso_transform(x, seed: int = 42, dtype: torch.dtype = torch.float32, return_transform: bool = False):
    opt_isometry: np.ndarray = ortho_group.rvs(x.shape[-1], random_state=seed)
    opt_isometry: torch.Tensor = torch.as_tensor(opt_isometry, dtype=dtype)
    out = x @ opt_isometry

    if return_transform:
        return out, opt_isometry

    return out


def transform_latents(
    x: torch.Tensor,
    norm_mode: Optional[str],
    seed: int,
    isometry_first: bool = True,
    scale: float = 1,
    translation: Optional[torch.Tensor] = None,
    noise: bool = False,
    N: int = 2,
) -> torch.Tensor:
    x = x.clone() * scale
    if translation is not None:
        x += translation.unsqueeze(0)

    norm = torch.tensor([1], dtype=dtype)

    if norm_mode == "independent":
        seed_everything(seed=seed)
        norm = torch.abs((torch.randn(x.size(0), dtype=dtype) + 0.001) * 100)
    elif norm_mode == "consistent":
        grid_side: int = int(x.size(0) ** (1 / 2))
        norm = x.reshape(grid_side, grid_side, N).sum(dim=-1)
        norm = (norm**2).flatten()
        norm = (norm - norm.min()) / (norm.max() - norm.min()) + 1
    elif norm_mode == "smooth":
        grid_side: int = int(x.size(0) ** (1 / 2))
        norm = x.reshape(grid_side, grid_side, N).sum(dim=-1)
        norm = (norm**3).flatten()
        norm = (norm - norm.min()) / (norm.max() - norm.min()) + 1
    elif norm_mode == "fixed":
        x = x * 10

    if noise:
        x = x + torch.abs(torch.randn_like(x) * 0.04)

    if isometry_first:
        out = iso_transform(x, seed=seed) * norm.unsqueeze(-1)
    else:
        out = iso_transform(x * norm.unsqueeze(-1), seed=seed)

    return out


def random_transform(x: torch.Tensor, seed: int) -> torch.Tensor:
    seed_everything(seed=seed)
    random_matrix = torch.randn((x.size(1), x.size(1)), dtype=dtype)
    return x @ random_matrix


class Translation(Slide):
    def resume_optimization(self, axes, run_opt: pd.DataFrame, sample_ids: Sequence[int], max_lim: int):
        dots = []
        coords = []
        for sample_id in sample_ids[:max_lim]:
            point_df = run_opt[run_opt["sample_id"] == sample_id].iloc[-1]
            coords.append([point_df.dim_0, point_df.dim_1])
            point = np.asarray([point_df.dim_0, point_df.dim_1, 0])
            point = axes.coords_to_point([point])
            point_target = int(point_df.target)
            dot = Dot(point, stroke_width=1, fill_opacity=0.75, color=TARGET_COLORS[point_target], radius=0.05)
            dot.target = point_target
            dot.sample_id = point_df.sample_id
            dots.append(dot)
        return dots, np.asarray(coords)

    def build_pipeline(self, axis, original_dots, source_space, target_space):
        centered_source_space = source_space - source_space.mean(dim=0)
        centered_target_space = target_space - target_space.mean(dim=0)

        scaled_source_space = centered_source_space / source_space.std(dim=0)
        scaled_target_space = centered_target_space / target_space.std(dim=0)

        rotated_source_space = scaled_source_space @ svd_translation(scaled_source_space, scaled_target_space)[0]
        descaled_source_space = rotated_source_space * target_space.std(dim=0)
        decentered_source_space = descaled_source_space + target_space.mean(dim=0)

        previous_step = torch.cat([source_space, torch.zeros((source_space.size(0), 1), dtype=dtype)], dim=1)
        previous_step = original_dots
        dots = []
        anims = []
        label = None
        for next_step, next_step_name in (
            (centered_source_space, "Centering"),
            (scaled_source_space, "Scaling"),
            (rotated_source_space, r"$\mathcal{T}$ estimation and application"),
            (descaled_source_space, "Descaling"),
            (decentered_source_space, "Decentering"),
        ):
            step_dots = []
            step_anims = []
            next_step = torch.cat([next_step, torch.zeros((next_step.size(0), 1), dtype=dtype)], dim=1).numpy()
            next_points = axis.coords_to_point(next_step)

            for previous_dot, next_point in zip(previous_step, next_points):
                previous_dot.generate_target()
                previous_dot.target.move_to(next_point)
                step_anims.append(MoveToTarget(previous_dot, rate_func=rate_functions.smooth))
                step_dots.append(previous_dot)

            next_label = Tex(next_step_name, font_size=34).next_to(axis, DOWN)

            labelanim = Create(next_label) if label is None else ReplacementTransform(label, next_label)
            anims.append(
                AnimationGroup(
                    AnimationGroup(labelanim, run_time=0.5),
                    AnimationGroup(*step_anims, lag_ratio=0),
                    lag_ratio=0.8,
                    run_time=2.5,
                ),
            )

            label = next_label

            dots.append(step_dots)

        anims.append(AnimationGroup(Unwrite(label), run_time=0.5))

        return dots, anims

    def construct(self):
        slide_title = SectionTitle(section_title="Direct Translation")
        # TODO: decidi che fare
        reference = Reference(
            text="Maiorca*, Moschella*, et al. “Latent Space Translation via Semantic Alignment”, NeurIPS 2023",
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
        left_axis_label = Tex(r"Source space").next_to(left_axis, UP)
        left_axis_block = VGroup(left_axis_label, left_axis)

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
        right_axis_label = Tex(r"Target space").next_to(right_axis, UP)
        right_axis_block = VGroup(right_axis_label, right_axis)

        left_dots, x = self.resume_optimization(
            axes=left_axis, run_opt=left_run_opt, sample_ids=sample_ids, max_lim=POINTS
        )
        right_dots, y = self.resume_optimization(
            axes=right_axis, run_opt=right_run_opt, sample_ids=sample_ids, max_lim=POINTS
        )
        original_dots = left_dots

        self.play(
            Create(left_axis_block),
            Create(right_axis_block),
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

        self.next_slide()

        left_dots, pipeline_anims = self.build_pipeline(
            axis=left_axis,
            original_dots=left_dots,
            source_space=torch.as_tensor(x),
            target_space=torch.as_tensor(y),
        )

        for pipeline_step in pipeline_anims:
            self.play(pipeline_step)
            self.wait(0.1)
            self.next_slide()

        approx_symbol = Tex(r"$\approx$", font_size=54).shift(UP * 0.25)

        self.play(Write(approx_symbol))
        #
        self.next_slide(auto_next=True)
        #
        self.play(
            AnimationGroup(FadeOut(approx_symbol)),
            AnimationGroup(
                *(AnimationGroup(FadeOut(x), FadeOut(y)) for x, y in zip(original_dots, right_dots)), lag_ratio=0.1
            ),
            AnimationGroup(
                Uncreate(left_axis_block),
                Uncreate(right_axis_block),
            ),
            run_time=1.5,
        )
