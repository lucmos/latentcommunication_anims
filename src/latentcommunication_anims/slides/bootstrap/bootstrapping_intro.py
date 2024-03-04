import itertools
import random
from pathlib import Path
from typing import *

import pandas as pd
from altair import Self
from manim import *
from manim.mobject.geometry.line import Arrow
from manim.mobject.geometry.polygram import Polygon
from manim_slides import Slide
from powermanim.layouts.arrangedbullets import Bullet, MathBullet
from powermanim.templates.bulletlist import BulletList
from powermanim.templates.reference import Reference
from powermanim.templates.sectiontitle import SectionTitle
from torchvision.datasets import MNIST

from nn_core.common import PROJECT_ROOT

from latentcommunication_anims.slides.parallel_opt import ANCHORS_IDX, CHOSEN_SAMPLE, LEFT_RUN_ID, POINTS, RIGHT_RUN_ID
from latentcommunication_anims.utils import TARGET_COLORS, get_run_opt, section_slide, seed_everything

folder_path: Path = PROJECT_ROOT / "data" / "bootstrapping" / "csv"
IDS = [13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29]
STEPS = [1, 2, 3, 77, 78, 79, 80, 81, 82, 83, 84, 85, 87, 88, 89, 90]

DOMAIN_X_COLOR = GREEN
DOMAIN_Y_COLOR = BLUE
SEED_COLOR = ORANGE
PERMUTATION_COLOR = PURPLE


class BoostrappingIntro(Slide):
    def construct(self) -> None:
        slide_title = SectionTitle(section_title="Limited Semantic Correspondence")
        reference = Reference(
            text="Cannistraci, Moschella, et al. “Bootstrapping Parallel Anchors for Relative Representations”, Tiny Papers at ICLR 2023",
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

        fix_words_g = VGroup()
        fix_words = pd.read_csv(folder_path / "anchors_fix_words.csv")
        fix_words = fix_words[fix_words["anchor_id"].isin(IDS)]
        fix_words = list(fix_words["anchor"])

        for word in fix_words:
            fix_words_g += Text(word, weight=MEDIUM)

        fix_words_g[0].set_color(SEED_COLOR)
        fix_words_g[1].set_color(SEED_COLOR)

        fix_words_g.arrange(DOWN, buff=MED_SMALL_BUFF * 1.3).to_edge(LEFT, buff=LARGE_BUFF * 2).scale(0.5)
        box = SurroundingRectangle(fix_words_g, corner_radius=0.5, buff=0.45, stroke_color=DOMAIN_X_COLOR)

        # moving words
        opt_words = pd.read_csv(folder_path / "anchors_optim_words_custom.csv")

        step_0_df = opt_words[opt_words.step == 0]
        transform_words = [Text(x.anchor, weight=MEDIUM) for _, x in step_0_df.iterrows()]

        init = VGroup(Text("exome", color=SEED_COLOR), Text("garrisoning", color=SEED_COLOR), *transform_words)
        init.arrange(DOWN, buff=MED_SMALL_BUFF * 1.3).to_edge(RIGHT, buff=LARGE_BUFF * 2).scale(0.5)

        box2 = SurroundingRectangle(init, corner_radius=0.5, buff=0.45, stroke_color=DOMAIN_Y_COLOR)

        arrow = DoubleArrow(buff=0, tip_length=0.2, color=WHITE)

        left = VGroup(fix_words_g, box)
        fasttex = Tex("FastText").next_to(left, UP)
        left = VGroup(left, fasttex)

        right = VGroup(init, box2)
        w2c = Tex("Word2Vec").next_to(right, UP)
        right = VGroup(right, w2c)

        VGroup(left, arrow, right).arrange(RIGHT, buff=1.5).scale(0.8).move_to(ORIGIN).to_edge(DOWN)

        self.play(
            *(Create(x) for x in (fix_words_g, box, fasttex, init, box2, w2c)),
            GrowFromPoint(arrow, point=arrow.get_critical_point(ORIGIN)),
        )

        self.wait(0.1)
        self.next_slide()

        displayed_words = [x for x in transform_words]
        for step in STEPS:
            current_df = opt_words[opt_words.step == step]
            current_words = list(current_df.anchor)

            step_anim = []
            for i, word in enumerate(current_words):
                if word != displayed_words[i]:
                    displayed_words[i] = word
                    step_anim.append(
                        AnimationGroup(
                            Transform(
                                transform_words[i],
                                x := Text(word, weight=MEDIUM).scale(0.4).move_to(transform_words[i]),
                            ),
                            ShowPassingFlash(Underline(x, color=SEED_COLOR)),
                        )
                    )

            if step_anim:
                self.play(*step_anim)

        self.wait(0.1)
        self.next_slide(auto_next=True)
        self.play(
            FadeOut(fasttex),
            FadeOut(w2c),
            FadeOut(init),
            FadeOut(fix_words_g),
            FadeOut(box),
            FadeOut(box2),
            FadeOut(arrow),
        )
