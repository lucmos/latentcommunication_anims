import itertools

import torch
from manim import *
from manim_slides import Slide
from sklearn.decomposition import PCA

from nn_core.common import PROJECT_ROOT

from latentcommunication_anims.utils import section_slide

EMBEDDING_SPACES = (
    "local_fasttext",
    "word2vec-google-news-300",
)
ABSOLUTE_LATENTS = PROJECT_ROOT / "data" / "word_latents" / "absolute_latents.pt"
RELATIVE_LATENTS = PROJECT_ROOT / "data" / "word_latents" / "relative_latents.pt"
TARGETS = PROJECT_ROOT / "data" / "word_latents" / "latents_targets.pt"

COLORS = [RED, BLUE, GREEN, PURPLE]


def reduce_dimensionality(latents):
    return PCA(n_components=2).fit_transform(latents.cpu())


class SemanticSpace(Slide):
    def construct(self):
        section_slide(self, "Semantic Invariance")

        self.next_slide()
        consider = Tex(r"Given some \emph{words}...").shift(UP * 0.5)
        consider2 = Tex(r"...consider their \emph{embeddings} in different spaces").next_to(
            consider, DOWN, buff=LARGE_BUFF
        )
        self.play(
            AnimationGroup(FadeIn(consider), FadeIn(consider2), lag_ratio=0.5, run_time=1.5),
        )

        self.wait()
        self.next_slide()
        self.play(FadeOut(consider), FadeOut(consider2))
        abs_latents = torch.load(ABSOLUTE_LATENTS, map_location="cpu")
        rel_latents = torch.load(RELATIVE_LATENTS, map_location="cpu")
        targets = torch.load(TARGETS)
        left_axis = Axes(
            x_range=[-3.8, 3.8, 1],
            y_range=[-3.8, 3.8, 1],
            x_length=5,
            y_length=5,
            tips=True,
        ).to_edge(LEFT, buff=LARGE_BUFF)
        right_axis = Axes(
            x_range=[-3.8, 3.8, 1],
            y_range=[-3.8, 3.8, 1],
            x_length=5,
            y_length=5,
            tips=True,
        ).to_edge(RIGHT, buff=LARGE_BUFF)
        fasttex = Tex("FastText").next_to(left_axis, UP, buff=MED_LARGE_BUFF)
        w2c = Tex("Word2Vec").next_to(right_axis, UP, buff=MED_LARGE_BUFF)
        absolute_spaces = Tex("Absolute", " Spaces").to_edge(DOWN, buff=LARGE_BUFF)

        abs_dots = {x: [] for x in EMBEDDING_SPACES}
        for ax, embed_name in zip([left_axis, right_axis], EMBEDDING_SPACES):
            latents = abs_latents[embed_name]
            points = reduce_dimensionality(latents)

            for point, target in zip(points, targets):
                dot = Dot(
                    point=ax.coords_to_point(*point),
                    color=COLORS[target - 1],
                    radius=DEFAULT_DOT_RADIUS / 2,
                    fill_opacity=0.5,
                )
                abs_dots[embed_name].append(dot)

        self.play(
            Create(fasttex),
            Create(w2c),
            Create(left_axis),
            Create(right_axis),
        )
        self.play(
            AnimationGroup(
                *(
                    AnimationGroup(
                        Create(left_dot),
                        Create(right_dot),
                        lag_ratio=0,
                    )
                    for left_dot, right_dot in zip(abs_dots[EMBEDDING_SPACES[0]], abs_dots[EMBEDDING_SPACES[1]])
                ),
                lag_ratio=0.2,
                run_time=2.5,
            ),
        )
        self.play(Create(absolute_spaces))

        self.wait()
        self.next_slide()
        rel_dots_anims = []
        for ax, embed_name in zip([left_axis, right_axis], EMBEDDING_SPACES):
            latents = rel_latents[embed_name]
            points = reduce_dimensionality(latents)
            for dot, point in zip(abs_dots[embed_name], points):
                rel_dots_anims.append(dot.animate.move_to(ax.coords_to_point(*point)))
        relative_spaces = Tex("Relative", " Spaces").to_edge(DOWN, buff=LARGE_BUFF)
        self.play(
            ReplacementTransform(absolute_spaces[0], relative_spaces[0]),
            *rel_dots_anims,
            run_time=6,
        )
        self.play(
            Circumscribe(
                relative_spaces[0],
                color=YELLOW,
            )
        )

        self.wait()
        self.next_slide()
        self.play(
            *(
                Uncreate(x)
                for x in itertools.chain(
                    [relative_spaces[0], absolute_spaces[1], left_axis, fasttex, right_axis, w2c],
                    *(abs_dots[embed_name] for embed_name in EMBEDDING_SPACES),
                )
            )
        )

        semantic = Tex("latent spaces with the same semantics").shift(UP * 1.25)
        unique_representation = Tex(r"represented \textbf{similarly} in the relative space").shift(DOWN * 1.25)
        arrow = Arrow(semantic.get_critical_point(DOWN), unique_representation.get_critical_point(UP)).scale(0.9)
        VGroup(semantic, unique_representation, arrow).move_to(ORIGIN)
        self.play(
            AnimationGroup(Create(semantic), Create(arrow), Create(unique_representation), lag_ratio=0.9),
            run_tim=2,
        )

        self.wait()
        self.next_slide(auto_next=True)
        self.play(
            AnimationGroup(
                *(Uncreate(x) for x in [semantic, arrow, unique_representation]),
                lag_ratio=0.5,
            ),
            run_time=0.5,
        )


if __name__ == "__main__":
    SemanticSpace().construct()
