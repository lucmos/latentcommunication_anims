from manim import *
from manim_slides import Slide
from powermanim.templates.reference import Reference

# Create a custom TeX template with necessary packages
custom_tex_template = TexTemplate()
custom_tex_template.add_to_preamble(r"\usepackage{booktabs,multirow}")

# Define the LaTeX code for the table
latex_table_vision = r"""
\begin{tabular}{lccccc}
    \toprule
    {Method}                   & {Dataset size} & {ImageNet} & {CIFAR100} & {Pets} & {ImageNet v2} \\
    \midrule
    CLIP                   & 400M (private)        & 68.6              & 68.7              & 88.9          & -                    \\
    CLIP                   & 15M (public)          & 31.3              & -                 & -             & -                    \\
    LiT                     & 10M (public)          & 66.9              & -                 & -             & -                    \\
    CLIP~(lit) & 901M (private)        & 50.6              & 47.9              & 70.3          & 43.3                 \\
    LiT                     & 901M (private)        & 70.1              & 70.9              & 88.1          & 61.7                 \\
    \midrule
    % ASIF (sup vis. encoder)                    & 1.6M (public)                  & 55.4$^*$                      & 63.3                       & 71.5                   & 45.6  \\
    ASIF (sup vis. encoder)           & 1.6M (public)         & 60.9              & 50.2              & 81.5          & 52.2                 \\
    ASIF (unsup vis. encoder)         & 1.6M (public)         & 53.0              & 46.5              & 74.7          & 45.9                 \\
    \bottomrule
\end{tabular}
"""


class Asif(Slide):
    def construct(self):
        #
        # slide_title = Tex("Out-Of-Domain Anchors").to_edge(UP)
        # self.play(Write(slide_title), run_time=0.5)
        slide_title = Tex("ASIF: Unimodal Models to Multimodal").to_edge(UP)
        reference = Reference(
            text="Norelli, et al. “ASIF: Coupled Data Turns Unimodal Models to Multimodal without Training”, NeurIPS 2023",
            font_size=24,
        )
        # Render the table using the custom TeX template
        table = Tex(latex_table_vision, tex_template=custom_tex_template)
        table.scale(0.6).move_to(ORIGIN)

        self.play(
            AnimationGroup(
                Create(slide_title),
                Create(reference),
                Create(table),
            ),
            lag_ratio=0.5,
            run_time=1,
        )

        self.wait(0.1)
        self.next_slide(auto_next=True)
        self.play(FadeOut(table), FadeOut(reference), FadeOut(slide_title))
        self.wait(0.1)
