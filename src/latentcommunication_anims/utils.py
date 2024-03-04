import random

import pandas as pd
import torch
from manim import *
from manim_slides import Slide
from powermanim.templates.sectiontitle import SectionTitle

from nn_core.common import PROJECT_ROOT

STORAGE_DIR: Path = PROJECT_ROOT / "data" / "anim_latents"
TARGET_COLORS = [
    ORANGE,
    BLUE,
    TEAL,
    GREEN,
    YELLOW,
    GOLD,
    RED,
    MAROON,
    PURPLE,
    PINK,
]


def section_slide(slide: Slide, section_title: str, auto_next: bool = False) -> SectionTitle:
    slide_title = SectionTitle(section_title=section_title)
    slide.play(slide_title.show())
    slide.wait(0.1)
    slide.next_slide(auto_next=auto_next)
    slide.play(slide_title.hide())
    return slide_title


def get_run_opt(run_id: str) -> pd.DataFrame:
    df = pd.read_csv(STORAGE_DIR / run_id / "val_latents.tsv", sep="\t")
    # df.dim_0 = (df.dim_0 - df.dim_0.min()) / (df.dim_0.max() - df.dim_0.min()) * 2 - 1
    # df.dim_1 = (df.dim_1 - df.dim_1.min()) / (df.dim_1.max() - df.dim_1.min()) * 2 - 1
    return df


def seed_everything(seed) -> int:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    return seed
