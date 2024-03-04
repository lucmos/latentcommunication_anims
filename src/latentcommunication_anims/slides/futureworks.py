from manim import *
from manim_slides import Slide
from powermanim.layouts.arrangedbullets import Bullet
from powermanim.templates.bulletlist import BulletList

from latentcommunication_anims.utils import section_slide

FONT_SIZE = 44


class FutureWorks(Slide):
    def construct(self):
        section_slide(self, "Future Works")
        self.next_slide()

        title = Tex(
            r"Possible Research Directions",
        )
        title.to_edge(UP)

        bulletlist = (
            BulletList(
                Bullet(
                    "Analyze Multimodal Data: discover semantic correspondences (e.g. DNA \& RNA)",
                    force_inline=True,
                    font_size=FONT_SIZE,
                    level=0,
                ),
                Bullet("Modular Neural Components: reusable decoders", font_size=FONT_SIZE, level=0),
                Bullet(
                    "Relative Representations Interpretability: each dimension has a meaning",
                    font_size=FONT_SIZE,
                    level=0,
                ),
                Bullet(
                    "Learnable Similarity Functions to infuse a data-driven invariance",
                    font_size=FONT_SIZE,
                    level=0,
                ),
                Bullet(
                    "Geodesic Relative Representations to better describe the data manifold",
                    font_size=FONT_SIZE,
                    level=0,
                ),
                Bullet(
                    r"Automatic Data Curation: exploit \emph{good models} to curate the data",
                    font_size=FONT_SIZE,
                    level=0,
                ),
                line_spacing=LARGE_BUFF * 0.8,
                scale_active=1.025,
                inactive_opacity=0.35,
            )
            .scale(0.75)
            .to_edge(LEFT)
            .shift(DOWN * 0.5)
        )

        self.play(
            AnimationGroup(
                Create(title),
                FadeIn(bulletlist),
                lag_ratio=0.5,
            ),
            run_time=1.25,
        )

        self.wait()

        for _ in range(bulletlist.ngroups):
            self.wait(0.1)
            self.next_slide()
            self.play(bulletlist.also_next())

        self.wait(0.1)
        self.next_slide(auto_next=True)
        self.play(
            FadeOut(bulletlist),
            Uncreate(title),
        )
