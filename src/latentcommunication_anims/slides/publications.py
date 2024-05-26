from manim import *
from manim_slides import Slide
from powermanim.layouts.arrangedbullets import Bullet
from powermanim.templates.bulletlist import BulletList

from latentcommunication_anims.utils import section_slide

FONT_SIZE_HEADER = 28
FONT_SIZE_PUBS = 18

AUTHOR_COLOR = TEAL
CONFERENCE_COLOR = GREEN
HIGHTLIGHT_COLOR = ORANGE


class Publications(Slide):
    def construct(self):
        title = Tex(
            r"Authored Publications",
        )
        title.to_edge(UP)

        bullets = (
            Bullet(
                "Latent Communication:",
                force_inline=False,
                font_size=FONT_SIZE_HEADER,
                level=0,
                symbol="",
            ),
            Bullet(
                r"Cannistraci, I., ",
                r"Moschella, L.",
                ", et. al. ``From Bricks to Bridges: Product of Invariances to Enhance Latent Space Communication''. ",
                r"In: ",
                r"ICLR 2024 ",
                r"(Spotlight, Top 5\%)",
                force_inline=True,
                font_size=FONT_SIZE_PUBS,
                level=1,
                symbol="[1]",
            ),
            Bullet(
                r"Crisostomi, D., Cannistraci, I., ",
                r"Moschella, L.",
                ", et. al. ``From Charts to Atlas: Merging Latent Spaces into One''. ",
                "In: ",
                r"NeurReps at ",
                r"NeurIPS 2023",
                force_inline=True,
                font_size=FONT_SIZE_PUBS,
                level=1,
                symbol="[2]",
            ),
            Bullet(
                r"Cannistraci, I., ",
                r"Moschella, L.",
                ", et. al. ``Bootstrapping Parallel Anchors for Relative Representations''. ",
                r"In: Tiny Papers Track at ",
                r"ICLR 2023",
                force_inline=True,
                font_size=FONT_SIZE_PUBS,
                level=1,
                symbol="[3]",
            ),
            Bullet(
                r"Maiorca*, V., ",
                r"Moschella*, L.",
                ", et. al. ``Latent Space Translation via Semantic Alignment''. ",
                r"In: ",
                r"NeurIPS 2023",
                force_inline=True,
                font_size=FONT_SIZE_PUBS,
                level=1,
                symbol="[4]",
            ),
            Bullet(
                r"Moschella*, L.",
                ", Maiorca*, V., et. al. ``Relative representations enable zero-shot latent space communication''. ",
                r"In: ",
                r"ICLR 2023 ",
                r"(Oral, Notable Top 5\%)",
                force_inline=True,
                font_size=FONT_SIZE_PUBS,
                level=1,
                symbol="[5]",
            ),
            Bullet(
                r"Norelli, A., Fumero, M., Maiorca, V., ",
                r"Moschella, L.",
                ", et. al. ``ASIF: Coupled Data Turns Unimodal Models to Multimodal without Training''. ",
                r"In: ",
                r"NeurIPS 2023",
                force_inline=True,
                font_size=FONT_SIZE_PUBS,
                level=1,
                symbol="[6]",
            ),
            Bullet(
                r"Ricciardi, A. P., Maiorca, V., ",
                r"Moschella, L.",
                ", et. al. ``Latent Communication for Zero-shot Stitching in Reinforcement Learning''. ",
                r"Under review, 2024",
                force_inline=True,
                font_size=FONT_SIZE_PUBS,
                level=1,
                symbol="[7]",
            ),
            Bullet(
                "Other Research Directions:",
                force_inline=True,
                font_size=FONT_SIZE_HEADER,
                level=0,
                symbol="",
            ),
            Bullet(
                r"Frascaroli, E., Benaglia, R., Boschini, M., ",
                r"Moschella, L.",
                ", et. al. ``CaSpeR: Latent Spectral Regularization for Continual Learning''. Preprint, 2023",
                force_inline=True,
                font_size=FONT_SIZE_PUBS,
                level=1,
                symbol="[8]",
            ),
            Bullet(
                r"Srivastava, A., et. al. ``Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models''. In: ",
                r"TMLR 2023",
                force_inline=True,
                font_size=FONT_SIZE_PUBS,
                level=1,
                symbol="[9]",
            ),
            Bullet(
                r"Crisostomi, D., Antonelli, S., Maiorca, V., ",
                r"Moschella, L.",
                ", et. al. ``Metric Based Few-Shot Graph Classification''. In: ",
                r"LoG 2022",
                force_inline=True,
                font_size=FONT_SIZE_PUBS,
                level=1,
                symbol="[10]",
            ),
            Bullet(
                r"Moschella, L.",
                ", et al. ``Learning Spectral Unions of Partial Deformable 3D Shapes''. In: ",
                r"Computer Graphics Forum 2022",
                force_inline=True,
                font_size=FONT_SIZE_PUBS,
                level=1,
                symbol="[11]",
            ),
            Bullet(
                r"Norelli, A., Mariani, G., ",
                r"Moschella, L.",
                ", et. al. ``Explanatory Learning: Beyond Empiricism in Neural Networks''. Preprint, 2022",
                force_inline=True,
                font_size=FONT_SIZE_PUBS,
                level=1,
                symbol="[12]",
            ),
            Bullet(
                r"Trappolini, G., Cosmo, L., ",
                r"Moschella, L.",
                ", et. al. ``Shape Registration in the Time of Transformers''. In: ",
                r"NeurIPS 2021",
                force_inline=True,
                font_size=FONT_SIZE_PUBS,
                level=1,
                symbol="[13]",
            ),
        )

        bullet_idx2author_name_idx = [
            None,
            1,
            1,
            1,
            1,
            0,
            1,
            1,
            None,
            1,
            None,
            1,
            0,
            1,
            1,
        ]
        for bullet_idx, author_idx in enumerate(bullet_idx2author_name_idx):
            if author_idx is None:
                continue
            bullets[bullet_idx][author_idx].set_color(AUTHOR_COLOR)

        bullet_idx2conference = [
            None,
            4,
            5,
            4,
            4,
            3,
            4,
            None,
            None,
            None,
            1,
            3,
            2,
            None,
            3,
        ]
        for bullet_idx, conference_idx in enumerate(bullet_idx2conference):
            if conference_idx is None:
                continue
            bullets[bullet_idx][conference_idx].set_color(CONFERENCE_COLOR)

        bullet_idx2hightlight = [
            (1, 5),
            (5, 4),
        ]
        for bullet_idx, hightlight_idx in bullet_idx2hightlight:
            bullets[bullet_idx][hightlight_idx].set_color(HIGHTLIGHT_COLOR)

        bulletlist = (
            BulletList(
                *bullets,
                line_spacing=MED_LARGE_BUFF * 1.1,
                line_spacing_decay=0.45,
                indent_buff=SMALL_BUFF,
                scale_active=1,
                inactive_opacity=0.35,
                active_opacity=1,
            )
            .to_edge(LEFT, buff=SMALL_BUFF * 1.5)
            .shift(DOWN * 0.5)
        )

        self.play(
            AnimationGroup(
                Create(title),
                FadeIn(bulletlist),
                lag_ratio=0.5,
            ),
            run_time=1,
        )

        self.play(
            AnimationGroup(
                *(bulletlist.also_next() for _ in range(bulletlist.ngroups)),
                lag_ratio=0.5,
                run_time=2,
            )
        )
        self.wait(0.1)
        self.next_slide(auto_next=True)
        self.play(
            FadeOut(bulletlist),
            FadeOut(title),
        )
