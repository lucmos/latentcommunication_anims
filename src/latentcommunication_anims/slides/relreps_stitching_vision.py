from manim import *
from manim_slides import Slide

# Create a custom TeX template with necessary packages
custom_tex_template = TexTemplate()
custom_tex_template.add_to_preamble(r"\usepackage{booktabs,multirow}")

# Define the LaTeX code for the table
latex_table_vision = r"""
\begin{tabular}{llrrrr}
\toprule
                      &                       & \multicolumn{2}{c}{\texttt{CIFAR-100}} & \multicolumn{2}{c}{\texttt{ImageNet}} \\\cmidrule(lr){3-4}\cmidrule(lr){5-6}
\textbf{Decoder} &  \textbf{Encoder} &      \multicolumn{1}{c}{\textbf{Absolute}}      &           \multicolumn{1}{c}{\textbf{Relative}}  &           \multicolumn{1}{c}{\textbf{Absolute}}  &           \multicolumn{1}{c}{\textbf{Relative}}  \\
\midrule
\multirow{4}{*}{RexNet} & RexNet &  $82.06$ &  $80.22$ &  $73.78$ &  $72.61$ \\
                      & ViT-base & \multicolumn{1}{r}{-}  &  $54.98$ &  \multicolumn{1}{r}{-} &  $37.39$ \\
                      & ViT-ResNet & \multicolumn{1}{r}{-} &  $53.33$ &  \multicolumn{1}{r}{-} &  $42.36$ \\
                      & ViT-small & \multicolumn{1}{r}{-} &  $59.82$ &  \multicolumn{1}{r}{-} &  $43.75$ \\
\cmidrule{1-6}
\multirow{4}{*}{ViT-base} & RexNet &  \multicolumn{1}{r}{-} &  $76.81$ &  \multicolumn{1}{r}{-} &  $30.78$ \\
                      & ViT-base &  $93.15$ &  $91.94$ &  $80.91$ &  $78.86$ \\
                      & ViT-ResNet &   $6.21$ &  $81.42$ &   $0.07$ &  $44.72$ \\
                      & ViT-small & \multicolumn{1}{r}{-} &  $84.29$ & \multicolumn{1}{r}{-} &  $48.31$ \\
\cmidrule{1-6}
\multirow{4}{*}{ViT-ResNet} & RexNet & \multicolumn{1}{r}{-} &  $79.79$ & \multicolumn{1}{r}{-} &  $53.46$ \\
                      & ViT-base &   $4.69$ &  $84.46$ &   $0.08$ &  $62.21$ \\
                      & ViT-ResNet &  $91.41$ &  $90.77$ &  $82.55$ &  $81.88$ \\
                      & ViT-small & \multicolumn{1}{r}{-} &  $84.66$ & \multicolumn{1}{r}{-} &  $61.32$ \\
\cmidrule{1-6}
\multirow{4}{*}{ViT-small} & RexNet & \multicolumn{1}{r}{-} &  $75.35$ & \multicolumn{1}{r}{-} &  $37.58$ \\
                      & ViT-base & \multicolumn{1}{r}{-} &  $81.23$ & \multicolumn{1}{r}{-} &  $50.08$ \\
                      & ViT-ResNet & \multicolumn{1}{r}{-} &  $78.35$ & \multicolumn{1}{r}{-} &  $45.45$ \\
                      & ViT-small &  $90.07$ &  $88.85$ &  $77.73$ &  $76.36$ \\
\bottomrule
\end{tabular}
"""


class RelRepStitchingVision(Slide):
    def construct(self):
        #
        # slide_title = Tex("Out-Of-Domain Anchors").to_edge(UP)
        # self.play(Write(slide_title), run_time=0.5)
        slide_title = Tex("Cross-architecture Stitching").to_edge(UP)

        # Render the table using the custom TeX template
        table = Tex(latex_table_vision, tex_template=custom_tex_template)
        table.scale(0.5).to_edge(DOWN)

        self.play(
            AnimationGroup(
                Create(slide_title),
                Create(table),
            ),
            lag_ratio=0.5,
            run_time=1,
        )

        self.wait(1)
        self.next_slide(auto_next=True)
        self.play(Uncreate(table), Uncreate(slide_title))
        self.wait(0.1)
