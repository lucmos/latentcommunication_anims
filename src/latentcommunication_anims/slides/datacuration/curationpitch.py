from manim import *
from manim_slides.slide import Slide
from powermanim import Bullet, BulletList

FONT_SIZE = 44


class CurationPitch(Slide):
    def construct(self):
        slide_title = Tex("tldr.").to_edge(UP)

        description = (
            Tex(r"Leverage multiple (pretrained) models\\[1.5ex]to curate data")
            .scale(1.25)
            .shift(UP * 0.5)
        )

        intuition = (
            BulletList(
                Bullet("Do not base decisions on a single arbitrary latent space"),
                Bullet("Tackle multi-modal data by construction"),
                inactive_opacity=0.1,
            )
            .scale(0.75)
            .to_corner(DL)
        )
        self.play(
            AnimationGroup(
                FadeIn(slide_title),
                FadeIn(description),
                FadeIn(intuition),
                lag_ratio=0.5,
            )
        )
        for _ in range(intuition.ngroups):
            self.wait(0.1)
            self.next_slide()
            self.play(intuition.also_next())

        self.next_slide(auto_next=True)
        self.play(
            AnimationGroup(
                *(FadeOut(x) for x in (slide_title, description, intuition)),
                lag_ratio=0.1,
            ),
        )

        # title = Tex(
        #     r"Possible Research Directions",
        # )
        # title.to_edge(UP)

        # bulletlist = (
        #     BulletList(
        #         Bullet(
        #             "Analyze Multimodal Data: discover semantic correspondences (e.g. DNA \& RNA)",
        #             force_inline=True,
        #             font_size=FONT_SIZE,
        #             level=0,
        #         ),
        #         Bullet("Modular Neural Components: reusable decoders", font_size=FONT_SIZE, level=0),
        #         Bullet(
        #             "Relative Representations Interpretability: each dimension has a meaning",
        #             font_size=FONT_SIZE,
        #             level=0,
        #         ),
        #         Bullet(
        #             "Learnable Similarity Functions to infuse a data-driven invariance",
        #             font_size=FONT_SIZE,
        #             level=0,
        #         ),
        #         Bullet(
        #             "Geodesic Relative Representations to better describe the data manifold",
        #             font_size=FONT_SIZE,
        #             level=0,
        #         ),
        #         Bullet(
        #             r"Automatic Data Curation: exploit \emph{multiple good models} to curate the data",
        #             font_size=FONT_SIZE,
        #             level=0,
        #         ),
        #         line_spacing=LARGE_BUFF * 0.8,
        #         scale_active=1.025,
        #         inactive_opacity=0.35,
        #     )
        #     .scale(0.75)
        #     .to_edge(LEFT)
        #     .shift(DOWN * 0.5)
        # )

        # self.play(
        #     AnimationGroup(
        #         Create(title),
        #         FadeIn(bulletlist),
        #         lag_ratio=0.5,
        #     ),
        #     run_time=1.25,
        # )

        # self.wait()

        # for _ in range(bulletlist.ngroups):
        #     self.wait(0.1)
        #     self.next_slide()
        #     self.play(bulletlist.also_next())

        # self.wait(0.1)
        # self.next_slide(auto_next=True)
        # self.play(
        #     FadeOut(bulletlist),
        #     Uncreate(title),
