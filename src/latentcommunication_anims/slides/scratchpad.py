from manim import *

from nn_core.common import PROJECT_ROOT


class ScratchPad(Scene):
    def construct(self):
        self.add(NumberPlane())
        self.wait()
