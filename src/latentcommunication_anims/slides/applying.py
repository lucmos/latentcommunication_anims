from manim import *
from manim_slides import Slide
from powermanim.layouts.arrangedbullets import Bullet
from powermanim.templates.bulletlist import BulletList

from nn_core.common import PROJECT_ROOT

from latentcommunication_anims.utils import section_slide


class Applying(Slide):
    def construct(self) -> None:
        section_slide(self, section_title=r"Applying\\Latent Communication")
