from manim_slides import Slide

from latentcommunication_anims.utils import section_slide


class Applying(Slide):
    def construct(self) -> None:
        section_slide(self, section_title=r"Applying\\Latent Communication", auto_next=True)
