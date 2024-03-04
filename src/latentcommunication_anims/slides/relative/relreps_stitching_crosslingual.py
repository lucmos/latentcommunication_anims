import numpy as np
from manim import *
from manim_slides import Slide


class RelRepStitchingCrossLingual(Slide):
    def construct(self):
        text = Tex(
            r"Given a classifier trained on \textbf{English data}...\\[1.5ex]",
            r"...stitch it as-is on latent spaces of \textbf{different languages}!",
        )

        self.play(
            Create(text),
            run_time=1,
        )

        self.wait()
        self.next_slide()

        self.play(
            Uncreate(text),
        )
        slide_title = Tex("Cross-lingual Stitching").to_edge(UP)
        self.play(Create(slide_title), run_time=0.5)

        # Data for the bar chart
        encoders = ["English", "Spanish", "French", "Japanese"]
        abs_fscores = [91.54, 43.67, 54.41, 48.72]
        rel_translated_fscores = [90.06, 82.78, 78.49, 65.72]
        rel_wikipedia_fscores = [90.45, 78.53, 70.41, 66.31]

        data = list(zip(abs_fscores, rel_translated_fscores, rel_wikipedia_fscores))

        # Labels for the x-axis
        x_labels = encoders

        # Colors for the bars
        bar_colors = [BLUE, GREEN, RED]

        # Category names for the legend
        category_names = ["Absolute", "Relative - Translated", "Relative - Wikipedia"]

        # Create the bar chart
        bar_charts, x_labels_group, legend, x_axis, y_axis = self.create_grouped_bar_chart(
            data, x_labels, bar_colors, category_names
        )

        encoding_languages = Tex("Encoding languages", font_size=30).to_edge(DOWN)
        bar_labels = [bc.get_bar_labels(font_size=24, label_constructor=MathTex) for bc in bar_charts]
        # Add the bar chart, x-axis labels, the legend, and the axes to the scene
        self.play(
            *[Create(bc) for bc in bar_charts],
            *[Create(bl) for bl in bar_labels],
            Create(x_labels_group),
            Create(legend),
            Create(x_axis),
            Create(y_axis),
            Create(encoding_languages),
        )

        self.wait()
        self.next_slide(auto_next=True)

        self.play(
            *[Uncreate(bc) for bc in bar_charts],
            *[Uncreate(bl) for bl in bar_labels],
            Uncreate(x_labels_group),
            Uncreate(legend),
            Uncreate(x_axis),
            Uncreate(y_axis),
            Uncreate(encoding_languages),
            Uncreate(slide_title),
        )
        self.wait(0.1)

    def create_grouped_bar_chart(self, data, x_labels, bar_colors, category_names):
        num_groups = len(data)
        num_bars_per_group = len(data[0])

        # Calculate the width of each bar and the gap between bars
        bar_width = 0.4
        gap_between_bars = 0.2
        gap_between_groups = 0.2

        bars = []
        for group_index in range(num_groups):
            bar_chart = BarChart(
                values=data[group_index],
                y_range=(0, 100),
                x_length=5
                / num_groups
                * (bar_width * num_bars_per_group + gap_between_bars * (num_bars_per_group - 1)),
                bar_colors=bar_colors,
                bar_fill_opacity=0.8,
                bar_stroke_width=0.5,
                bar_width=bar_width,
            )
            bar_chart.x_axis.set_opacity(0)
            bar_chart.y_axis.set_opacity(0)
            bars.append(bar_chart)

        bar_charts = VGroup(*bars).arrange_in_grid(rows=1, cols=len(bars), buff=gap_between_groups)

        # Create a single x-axis for all bar charts
        x_axis_start = bars[0].x_axis.get_start()
        x_axis_end = bars[-1].x_axis.get_end()
        x_axis = (
            Line(start=x_axis_start + LEFT, end=x_axis_end)
            .move_to(
                ORIGIN,
            )
            .align_to(bar_charts, DOWN)
            .shift(UP * 0.02)
        )

        # Create a single y-axis for all bar charts
        y_axis_start = x_axis.get_start() + DOWN * 0.5
        y_axis_end = y_axis_start + 5.5 * UP
        y_axis = Arrow(start=y_axis_start, end=y_axis_end, stroke_width=5).align_to(x_axis, LEFT).shift(UP * 0.03)
        y_axis_label = Tex(r"\textbf{F-score}", font_size=30).next_to(y_axis, LEFT, buff=-0.25).rotate(PI / 2)

        # Create x-axis labels
        x_labels_group = self.create_x_labels(bar_charts, x_labels)

        # Create the legend
        legend = self.create_legend(bar_colors, category_names)
        legend.to_corner(UP + RIGHT, buff=MED_LARGE_BUFF)

        return bar_charts, x_labels_group, legend, x_axis, VGroup(y_axis, y_axis_label)

    def create_x_labels(self, bar_charts, x_labels):
        x_labels_group = VGroup()

        for i, label in enumerate(x_labels):
            text = Tex(f"\\textbf{{{label}}}", font_size=28)
            text.next_to(bar_charts[i].x_axis.get_bottom(), DOWN, buff=0.4)
            x_labels_group.add(text)

        return x_labels_group

    def create_legend(self, bar_colors, category_names):
        legend_items = VGroup()

        for i, (color, name) in enumerate(zip(bar_colors, category_names)):
            item = VGroup(
                Rectangle(height=0.3, width=0.3, fill_color=color, fill_opacity=0.8, stroke_width=0.5),
                Text(name)
                .scale(0.5)
                .next_to(
                    Rectangle(height=0.3, width=0.3, fill_color=color, fill_opacity=0.8, stroke_width=0.5),
                    RIGHT,
                    buff=0.2,
                ),
            )
            legend_items.add(item)

        legend_items.arrange_submobjects(DOWN, aligned_edge=LEFT, buff=0.3)
        legend = VGroup(
            RoundedRectangle(
                corner_radius=0.2,
                height=legend_items.height + 0.5,
                width=legend_items.width + 1.2,
                stroke_width=1,
                fill_opacity=0.1,
            ),
            legend_items,
        )
        legend_items.move_to(legend.get_center())

        return legend.scale(0.7)
