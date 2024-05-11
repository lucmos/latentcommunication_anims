import random
from typing import Dict, Optional, Tuple

import networkx as nx
import numpy as np
import pandas as pd
from manim import *
from manim_slides import Slide

from nn_core.common import PROJECT_ROOT

from latentcommunication_anims.utils import section_slide

EXP_POINTS = PROJECT_ROOT / "data" / "latent_metric" / "Cora_data_manifold_points.tsv"
EXP_STATS = PROJECT_ROOT / "data" / "latent_metric" / "Cora_data_manifold_stats.tsv"

PARAM_FONT_SIZE = 34

seed = 3
random.seed(seed)
np.random.seed(seed)

COLORS = [YELLOW, BLUE, PURPLE, YELLOW, RED, BLUE, RED]

COLUMN2NAME = (
    ("seed", "Seed"),
    ("num_epochs", "Epochs"),
    ("num_layers", "Layers"),
    ("dropout", "Dropout"),
    ("hidden_fn", "Hidden act."),
    ("conv_fn", "Conv. act."),
    ("optimizer", "Optimizer"),
    ("lr", "Learning rate"),
    ("encoder", "Encoder"),
)

PERF_COLOR = BLUE
SIM_COLOR = YELLOW


def parallel_plot(df, exp_id, val_kwargs, sim_kwargs, **kwargs):
    exp_df = df.loc[df["experiment"] == exp_id]

    axes = Axes(
        x_range=[0, exp_df.epoch.max(), 5],
        y_range=[0, 1, exp_df.val_acc.max() * 2],
        axis_config={"color": WHITE},
        # x_axis_config={
        #     "numbers_to_include": np.arange(0, 1.1, 0.2),
        #     "numbers_with_elongated_ticks": np.arange(0, 1.1, 0.2),
        # },
        # y_axis_config={
        #     "numbers_to_include": np.arange(0, 1.1, 0.2),
        #     "numbers_with_elongated_ticks": np.arange(0, 1.1, 0.2),
        # },
        **kwargs,
        tips=True,
    ).scale(0.9)

    # SET UPDATERS

    acc_graph = axes.plot_line_graph(
        exp_df.epoch,
        exp_df.val_acc,
        **val_kwargs,
    )
    sim_graph = axes.plot_line_graph(
        exp_df.epoch,
        exp_df.reference_distance,
        **sim_kwargs,
    )

    correlation = exp_df.val_acc.corr(exp_df.reference_distance)
    return (
        axes,
        acc_graph,
        sim_graph,
        VGroup(axes, acc_graph, sim_graph),
        [
            AnimationGroup(Create(acc_graph), Create(sim_graph)),
        ],
        exp_df,
        MathTex(f"\\rho= {{{correlation:.2f}}}").scale(0.8).next_to(axes.x_axis, UP),
    )


def update_values(
    axes: Axes,
    rows_refs: Dict[str, VMobject],
    points_df: pd.DataFrame,
    reference: bool,
    exp_id: int,
    previous_values: Optional[Dict[str, str]] = None,
    only_dot: bool = False,
    dot_radius: float = DEFAULT_DOT_RADIUS,
) -> Tuple[Dot, Dict[str, VMobject], Dict[str, str]]:
    sample_df = points_df[points_df["reference"] == reference].loc[exp_id]

    dot = Dot(
        point=axes.coords_to_point(sample_df.similarity, sample_df.score),
        radius=dot_radius,
    )

    if reference:
        dot.set_color(color=GOLD)
    else:
        dot.set_color(color=BLUE_D)
        dot.set_style(fill_opacity=0.8)

    hypervalues = {}
    hyper_raw_texts = {}
    if not only_dot:
        for key_name, hyper_pos in rows_refs.items():
            sample_text = str(sample_df[key_name])
            if previous_values is None or sample_text != previous_values[key_name]:
                v = Tex(sample_text, font_size=PARAM_FONT_SIZE)
                v.next_to(hyper_pos, RIGHT, buff=MED_LARGE_BUFF)
                hypervalues[key_name] = v
            hyper_raw_texts[key_name] = sample_text
    return dot, hypervalues, hyper_raw_texts


class LatentMetricShort(Slide):
    def animate_a_dot(self, dot, reference_values, new_values, run_time=1.5):
        self.play(
            Create(dot, run_time=0.1),
            Flash(dot, line_length=0.15, line_stroke_width=2, run_time=1),
            AnimationGroup(
                *(
                    ShowPassingFlash(Underline(x, color=YELLOW))
                    for x in new_values.values()
                ),
                *(
                    Transform(reference_values[key], target_tex)
                    for key, target_tex in new_values.items()
                ),
            ),
            run_time=run_time,
        )

    def construct(self):
        section_slide(self, r"Latent Performance Metric")

        slide_title = Tex("Consider a node classification task...")
        self.play(FadeIn(slide_title))

        self.next_slide(auto_next=True)
        self.play(FadeOut(slide_title))

        n = 7  # 10 nodes
        m = 10  # 20 edges
        G = nx.gnm_random_graph(n, m, seed=seed)

        Line()
        g = Graph(
            list(G.nodes),
            list(G.edges),
            layout="spring",
            layout_scale=4,
            vertex_type=Circle,
            vertex_config={
                "radius": 0.20,
                "fill_opacity": 1,
                "fill_color": BLACK,
                "stroke_color": WHITE,
            },
            edge_config={
                "color": LIGHT_GRAY,
            },
        )

        cora_dataset = Tex(r"Cora dataset").to_edge(DL)
        self.play(Create(cora_dataset), Create(g))

        self.next_slide(auto_next=True)
        node_style_anim = []
        for x, c in zip(g, COLORS):
            node_style_anim.append(
                x.animate.set_style(stroke_color=c, stroke_opacity=0.5)
            )

        self.play(AnimationGroup(*node_style_anim, lag_ratio=0.25), run_time=2)

        self.next_slide()
        given_model = Tex(r"given a good")
        ref_model = Tex("reference model $\mathcal{M}$")
        good_model = (
            VGroup(
                given_model, ref_model.next_to(given_model, DOWN, buff=MED_LARGE_BUFF)
            )
            .move_to(ORIGIN)
            .to_edge(LEFT, buff=LARGE_BUFF)
        )
        self.play(
            Create(good_model), Uncreate(cora_dataset), g.animate.shift(RIGHT * 2)
        )

        # self.wait()
        node_colors_anim = []
        for x, c in zip(g, COLORS):
            node_colors_anim.append(x.animate.set_style(fill_color=c))
        self.play(
            AnimationGroup(
                ShowPassingFlash(Underline(ref_model, color=YELLOW), run_time=2),
                AnimationGroup(
                    *node_colors_anim,
                    lag_ratio=0.5,
                    run_time=3,
                ),
                lag_ratio=0.25,
            )
        )

        self.wait()
        self.next_slide()
        self.play(Uncreate(g), FadeOut(good_model))
        other_models = Tex("We train other models...")
        self.play(Create(other_models))

        self.wait()
        self.next_slide(auto_next=True)
        self.play(FadeOut(other_models))

        ####

        # compare_models = Tex("...and compare their relative space to the reference one").next_to(
        #     other_models, DOWN, buff=LARGE_BUFF
        # )

        exp_points = pd.read_csv(EXP_POINTS, sep="\t", index_col=0)

        hyperparms = {
            key: Tex(name, font_size=PARAM_FONT_SIZE) for key, name in COLUMN2NAME
        }
        params = (
            VGroup(*hyperparms.values())
            .arrange(DOWN, aligned_edge=RIGHT, buff=0.3)
            .move_to(ORIGIN)
            .shift(RIGHT * 3)
        )

        axes = Axes(
            x_range=[0, 1.15, 0.1],
            y_range=[0, 1.15, 0.1],
            x_length=6,
            axis_config={"color": WHITE},
            x_axis_config={
                "numbers_to_include": np.arange(0, 1.1, 0.2),
                "numbers_with_elongated_ticks": np.arange(0, 1.1, 0.2),
            },
            y_axis_config={
                "numbers_to_include": np.arange(0, 1.1, 0.2),
                "numbers_with_elongated_ticks": np.arange(0, 1.1, 0.2),
            },
            tips=True,
        )
        x_label = Tex(
            "Relative latent similarity to ", "$\mathcal{M}$", font_size=54
        ).next_to(axes.x_axis, DOWN, buff=MED_LARGE_BUFF)
        y_label = (
            Tex("Performance", font_size=54)
            .rotate(PI / 2)
            .next_to(axes.y_axis, LEFT, buff=MED_LARGE_BUFF)
        )
        VGroup(axes, x_label, y_label).scale(0.9).move_to(ORIGIN).to_edge(
            LEFT, buff=MED_LARGE_BUFF
        )

        reference_dot, hypervalues, hypertexts = update_values(
            axes=axes,
            rows_refs=hyperparms,
            points_df=exp_points,
            reference=True,
            exp_id=0,
        )

        self.play(*(Create(x) for x in [axes, x_label, y_label]))

        self.next_slide()
        self.play(
            *(Create(x) for x in [reference_dot, params, *hypervalues.values()]),
            ShowPassingFlash(Underline(x_label[1], color=YELLOW)),
            Circumscribe(reference_dot, shape=Circle, color=YELLOW),
            *(
                ShowPassingFlash(Underline(x, color=YELLOW))
                for x in hypervalues.values()
            ),
        )

        exp_ids = list(range(1, len(exp_points)))
        random.seed(0)
        np.random.seed(0)
        random.shuffle(exp_ids)

        self.wait()
        self.next_slide(auto_next=True)
        taken_idxs = {71}
        new_dot, new_hypervalues, hypertexts = update_values(
            axes=axes,
            rows_refs=hyperparms,
            points_df=exp_points,
            reference=False,
            exp_id=71,
            previous_values=hypertexts,
        )
        added_dots = [reference_dot, new_dot]
        self.animate_a_dot(
            dot=new_dot,
            reference_values=hypervalues,
            new_values=new_hypervalues,
            run_time=2,
        )

        self.next_slide(auto_next=True)
        chosen_idxs = [132, 1118, 171, 423, 1094]
        for i in chosen_idxs:
            taken_idxs.add(i)
            new_dot, new_hypervalues, hypertexts = update_values(
                axes=axes,
                rows_refs=hyperparms,
                points_df=exp_points,
                reference=False,
                exp_id=i,
                previous_values=hypertexts,
            )
            added_dots.append(new_dot)
            self.animate_a_dot(
                dot=new_dot,
                reference_values=hypervalues,
                new_values=new_hypervalues,
                run_time=1.5,
            )

        self.next_slide()

        left_objects = VGroup(*added_dots, y_label, x_label, axes)
        right_objects = VGroup(*hyperparms.values(), *hypervalues.values())
        self.play(
            AnimationGroup(
                FadeOut(right_objects, shift=RIGHT),
                left_objects.animate.move_to(ORIGIN),
                lag_ratio=0.25,
            ),
            run_time=2,
        )

        dots_size_anim = []
        for x in added_dots:
            dots_size_anim.append(
                Transform(
                    x,
                    Dot(
                        x.get_center(),
                        color=x.color,
                        radius=0.05,
                        fill_opacity=x.fill_opacity,
                    ),
                )
            )

        added_dots = []
        other_dots_anim = []
        for i in exp_ids:
            if i in taken_idxs:
                continue
            new_dot, _, _ = update_values(
                axes=axes,
                rows_refs=hyperparms,
                points_df=exp_points,
                reference=False,
                exp_id=i,
                previous_values=hypertexts,
                only_dot=True,
                dot_radius=0.05,
            )
            added_dots.append(new_dot)
            other_dots_anim.append(Create(new_dot))

        z = np.polyfit(exp_points.similarity, exp_points.score, 1)
        trend_line = np.poly1d(z)
        min_point = (min_sim := exp_points.similarity.min()), trend_line(min_sim)
        max_point = (max_sim := exp_points.similarity.max()), trend_line(max_sim)

        dashed_trendline = DashedLine(
            axes.coords_to_point(*min_point),
            axes.coords_to_point(*max_point),
            color=RED,
            dash_length=0.25,
            stroke_width=8,
        )
        corr_trendline = (
            MathTex(f"\\rho= {{{exp_points.similarity.corr(exp_points.score):.2f}}}")
            .next_to(dashed_trendline.get_corner(UP + RIGHT), UP + RIGHT)
            .set_color(RED)
            .scale(0.8)
        )

        self.play(
            *dots_size_anim,
            AnimationGroup(
                AnimationGroup(
                    *other_dots_anim,
                    run_time=3.5,
                    lag_ratio=0.1,
                ),
                Create(dashed_trendline),
                Create(corr_trendline),
                lag_ratio=0.85,
            ),
        )

        self.wait()
        self.next_slide()
        self.play(
            *(
                Uncreate(x)
                for x in [
                    dashed_trendline,
                    *added_dots,
                    x_label,
                    y_label,
                    axes,
                    left_objects,
                    corr_trendline,
                ]
            )
        )

        # correlation_over_time = Tex(r"...zooming into\\[1.5ex]a single model training")
        # self.play(Create(correlation_over_time))

        performance_label = VGroup(
            (d := Dot()), Tex("Performance", font_size=38).next_to(d)
        )
        performance_label.set_color(PERF_COLOR)
        similarity_label = VGroup(
            (d := Dot()), Tex("Similarity", font_size=38).next_to(d)
        )
        similarity_label.set_color(SIM_COLOR)
        VGroup(performance_label, similarity_label).arrange(
            RIGHT, aligned_edge=UP, buff=LARGE_BUFF
        ).to_edge(UP)

        epoch_tracker = ValueTracker(0)
        x_label = Tex("Epoch:", font_size=38)
        epoch_num = Integer(0, font_size=38).next_to(x_label)
        epoch_num.add_updater(lambda x: x.set_value(epoch_tracker.get_value()))

        VGroup(x_label, epoch_num).to_edge(DOWN)

        # self.wait()
        # self.play(
        #     FadeOut(correlation_over_time),
        # )

        exp_stats = pd.read_csv(EXP_STATS, sep="\t", index_col=0)

        # Filter experiments that reach at least 0.7 acc.
        VAL_ACC_LOWER_BOUND = 0.9
        df_max_acc = exp_stats.groupby(["experiment"]).agg([np.max])["val_acc"]
        best_experiments = df_max_acc.loc[df_max_acc["max"] > VAL_ACC_LOWER_BOUND]
        best_experiments = best_experiments.reset_index().experiment
        df = exp_stats[exp_stats["experiment"].isin(best_experiments)]
        available_experiments = sorted(set(df.experiment))

        val_kwargs = {
            "line_color": PERF_COLOR,
            "add_vertex_dots": False,
            "stroke_width": 8,
        }
        sim_kwargs = {
            "line_color": SIM_COLOR,
            "add_vertex_dots": False,
            "stroke_width": 8,
        }

        axes, acc_graph, sim_graph, objs, anims, exp_df, corr = parallel_plot(
            df, available_experiments[5], val_kwargs=val_kwargs, sim_kwargs=sim_kwargs
        )
        self.play(
            FadeIn(axes),
            Create(performance_label, run_time=1),
            Create(similarity_label, run_time=1),
            FadeIn(x_label),
            FadeIn(epoch_num),
        )
        self.play(
            *anims,
            epoch_tracker.animate.set_value(exp_df.epoch.max()),
            run_time=10,
        )
        self.play(
            FadeIn(corr),
        )

        self.wait()

        self.next_slide()
        self.play(
            FadeOut(performance_label),
            FadeOut(similarity_label),
            Uncreate(epoch_num),
            Uncreate(x_label),
            *(FadeOut(x) for x in [axes, acc_graph, sim_graph, corr]),
        )

        implication = Arrow(UP, DOWN, stroke_width=3)
        not_implication = Arrow(DOWN, UP, stroke_width=3).shift(RIGHT)

        similar_model = Tex("relative space similar to the reference model").align_to(
            implication.get_critical_point(UP) + UP * MED_LARGE_BUFF,
            DOWN,
        )
        performing = Tex("good performance").align_to(
            implication.get_critical_point(DOWN) + DOWN * MED_LARGE_BUFF,
            UP,
        )
        cross = Cross().scale(0.25).move_to(not_implication.get_center() + DOWN * 0.1)

        self.play(
            AnimationGroup(
                FadeIn(similar_model),
                GrowArrow(implication),
                FadeIn(performing),
                lag_ratio=0.8,
                run_time=2,
            )
        )

        self.wait()
        self.next_slide()
        self.play(
            implication.animate.shift(LEFT), GrowArrow(not_implication, shift=RIGHT)
        )
        self.play(Create(cross))

        self.wait()
        self.next_slide()
        self.play(
            *(
                Uncreate(x)
                for x in [
                    implication,
                    not_implication,
                    similar_model,
                    performing,
                    cross,
                ]
            )
        )


if __name__ == "__main__":
    LatentMetricShort().construct()
