import itertools

from altair import Self
from manim import *
from manim_slides import Slide
from powermanim.layouts.arrangedbullets import Bullet, MathBullet
from powermanim.templates.bulletlist import BulletList
from powermanim.templates.sectiontitle import SectionTitle
from torchvision.datasets import MNIST

from nn_core.common import PROJECT_ROOT

from latentcommunication_anims.components import Reference
from latentcommunication_anims.utils import section_slide


class RelReps(Slide):
    def construct(self):
        slide_title = SectionTitle(section_title="Universal Space")
        reference = Reference(
            text="Moschella et al. “Relative representations enable zero-shot latent space communication”, ICLR 2023 (oral)"
        )
        self.play(
            slide_title.show(),
            FadeIn(reference),
        )

        self.wait(0.1)
        self.next_slide(auto_next=False)
        slide_title.hide()
