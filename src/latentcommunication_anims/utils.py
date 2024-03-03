import pandas as pd
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


def section_slide(slide: Slide, section_title: str):
    slide_title = SectionTitle(section_title=section_title)
    slide_title.show(scene=slide)
    slide.wait(0.1)
    slide.next_slide()
    slide_title.hide(scene=slide)


def get_run_opt(run_id: str) -> pd.DataFrame:
    df = pd.read_csv(STORAGE_DIR / run_id / "val_latents.tsv", sep="\t")
    # df.dim_0 = (df.dim_0 - df.dim_0.min()) / (df.dim_0.max() - df.dim_0.min()) * 2 - 1
    # df.dim_1 = (df.dim_1 - df.dim_1.min()) / (df.dim_1.max() - df.dim_1.min()) * 2 - 1
    return df
