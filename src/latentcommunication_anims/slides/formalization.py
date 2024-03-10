import typing as tp
from math import copysign

from manim import *
from manim_slides import Slide
from powermanim.components.directionalarrow import DirectionalArrow
from powermanim.layouts.arrangedbullets import Bullet
from powermanim.templates.bulletlist import BulletList

from latentcommunication_anims.utils import section_slide

X_COLOR = RED
Y_COLOR = GREEN

MANIFOLD_EMBEDDING_Y_SHIFT = 0.325

MANIFOLD_BUFF = 1.75
AMBIENTS_HORIZ_BUFF = 1.5
AMBIENTS_VERT_BUFF = 1.25

LABEL_SCALE = 0.8

LABEL_BUFF = 0.075


class Formalization(Slide):

    def build_ambient_space(
        self,
        label: str,
        inner_manifold: VMobject,
        manifold_embedding_y_shift,
        color,
        size=2.5,
    ):
        if isinstance(label, str):
            label = (label,)

        shift_direction = UP * copysign(1, manifold_embedding_y_shift)
        ambient_space = Square(side_length=size, stroke_color=LIGHTER_GREY)
        inner_manifold = inner_manifold.set_color(color=WHITE)

        inner_manifold.scale_to_fit_height(ambient_space.get_height() * 0.4)

        inner_manifold.move_to(ambient_space.get_critical_point(LEFT))
        inner_manifold.shift(
            UP * manifold_embedding_y_shift,
        )
        inner_manifold.shift(
            [
                (inner_manifold.get_width() / 2)
                + abs(
                    ambient_space.get_critical_point(direction=shift_direction)[1]
                    - inner_manifold.get_critical_point(direction=shift_direction)[1]
                ),
                0,
                0,
            ]
        )

        label = MathTex(*label)
        if len(label) == 1:
            label.set_color(color)
        else:
            label[1].set_color(color)

        midpoint = (
            ambient_space.get_critical_point(-shift_direction) + inner_manifold.get_critical_point(-shift_direction)
        ) / 2
        label.move_to((ambient_space.get_center()[0], midpoint[1], 0))

        return VDict({"label": label, "space": ambient_space, "embedding": inner_manifold})

    def construct(self) -> None:
        # section_slide(self, section_title=r"The Latent Communication\\Problem")

        input_space_x = self.build_ambient_space(
            label="X",
            inner_manifold=RegularPolygon(5),
            manifold_embedding_y_shift=MANIFOLD_EMBEDDING_Y_SHIFT,
            color=X_COLOR,
        )

        input_space_y = self.build_ambient_space(
            label="Y",
            inner_manifold=DashedVMobject(RegularPolygon(5)),
            manifold_embedding_y_shift=-MANIFOLD_EMBEDDING_Y_SHIFT,
            color=Y_COLOR,
        )

        latent_space_x = self.build_ambient_space(
            label="\widetilde{X}",
            inner_manifold=(RegularPolygon(7)),
            manifold_embedding_y_shift=MANIFOLD_EMBEDDING_Y_SHIFT,
            color=X_COLOR,
        )

        latent_space_y = self.build_ambient_space(
            label="\widetilde{Y}",
            inner_manifold=DashedVMobject(RegularPolygon(7)),
            manifold_embedding_y_shift=-MANIFOLD_EMBEDDING_Y_SHIFT,
            color=Y_COLOR,
        )

        universal_space_x = self.build_ambient_space(
            label=("U_", "{X}"),
            inner_manifold=(RegularPolygon(16)),
            manifold_embedding_y_shift=MANIFOLD_EMBEDDING_Y_SHIFT,
            color=X_COLOR,
        )

        universal_space_y = self.build_ambient_space(
            label=("U_", "{Y}"),
            inner_manifold=DashedVMobject(RegularPolygon(16)),
            manifold_embedding_y_shift=-MANIFOLD_EMBEDDING_Y_SHIFT,
            color=Y_COLOR,
        )

        x_pipeline = VDict({"input": input_space_x, "latent": latent_space_x, "universal": universal_space_x})
        y_pipeline = VDict({"input": input_space_y, "latent": latent_space_y, "universal": universal_space_y})

        x_pipeline.arrange(RIGHT, buff=AMBIENTS_HORIZ_BUFF)
        y_pipeline.arrange(RIGHT, buff=AMBIENTS_HORIZ_BUFF)
        y_pipeline.next_to(x_pipeline, DOWN, buff=AMBIENTS_VERT_BUFF)

        formalization = VGroup(x_pipeline, y_pipeline)
        formalization.to_edge(DOWN, buff=0.75)
        formalization.to_edge(RIGHT, buff=1.25)

        manifold_x = MathTex(r"\mathcal{M}_", "{X}")
        manifold_x[1].set_color(X_COLOR)
        manifold_x.next_to(input_space_x["embedding"], LEFT, buff=MANIFOLD_BUFF)

        manifold_y = MathTex(r"\mathcal{M}_", "{Y}")
        manifold_y[1].set_color(Y_COLOR)
        manifold_y.next_to(input_space_y["embedding"], LEFT, buff=MANIFOLD_BUFF)

        phix = DirectionalArrow(
            manifold_x,
            input_space_x["embedding"].get_critical_point(LEFT),
            buff=0.1,
            direction=RIGHT,
            color=WHITE,
        )
        phix = VDict(
            {"phi": phix, "label": MathTex(r"\varphi_", "{X}").scale(LABEL_SCALE).next_to(phix, UP, buff=LABEL_BUFF)}
        )
        phix["label"][1].set_color(X_COLOR)

        phiy = DirectionalArrow(
            manifold_y,
            input_space_y["embedding"].get_critical_point(LEFT),
            buff=0.1,
            direction=RIGHT,
            color=WHITE,
        )
        phiy = VDict(
            {"phi": phiy, "label": MathTex(r"\varphi_", "{Y}").scale(LABEL_SCALE).next_to(phiy, UP, buff=LABEL_BUFF)}
        )
        phiy["label"][1].set_color(Y_COLOR)

        encoder_x = DirectionalArrow(
            input_space_x.get_critical_point(RIGHT),
            latent_space_x.get_critical_point(LEFT),
            buff=0.1,
            direction=RIGHT,
            color=WHITE,
        )
        encoder_x = VDict(
            {
                "arrow": encoder_x,
                "label": MathTex(r"E_", "{X}").scale(LABEL_SCALE).next_to(encoder_x, UP, buff=LABEL_BUFF),
            }
        )
        encoder_x["label"][1].set_color(X_COLOR)

        encoder_y = DirectionalArrow(
            input_space_y.get_critical_point(RIGHT),
            latent_space_y.get_critical_point(LEFT),
            buff=0.1,
            direction=RIGHT,
            color=WHITE,
        )
        encoder_y = VDict(
            {
                "arrow": encoder_y,
                "label": MathTex(r"E_", "{Y}").scale(LABEL_SCALE).next_to(encoder_y, UP, buff=LABEL_BUFF),
            }
        )
        encoder_y["label"][1].set_color(Y_COLOR)

        t_x = DirectionalArrow(
            latent_space_x.get_critical_point(RIGHT),
            universal_space_x.get_critical_point(LEFT),
            buff=0.1,
            direction=RIGHT,
            color=WHITE,
        )
        t_x = VDict(
            {
                "arrow": t_x,
                "label": MathTex(r"T_", r"{X}").scale(LABEL_SCALE).next_to(t_x, UP, buff=LABEL_BUFF),
            }
        )
        t_x["label"][1].set_color(X_COLOR)

        t_y = DirectionalArrow(
            latent_space_y.get_critical_point(RIGHT),
            universal_space_y.get_critical_point(LEFT),
            buff=0.1,
            direction=RIGHT,
            color=WHITE,
        )
        t_y = VDict(
            {
                "arrow": t_y,
                "label": MathTex(r"T_", r"{Y}").scale(LABEL_SCALE).next_to(t_y, UP, buff=LABEL_BUFF),
            }
        )
        t_y["label"][1].set_color(Y_COLOR)

        inputspaces_label = Tex("Input Spaces").next_to(input_space_x, UP)
        latentspaces_label = Tex("Latent Spaces").next_to(latent_space_x, UP)
        universalspaces_label = Tex("Universal Spaces").next_to(universal_space_x, UP)

        abstract_correspondence = DashedLine(
            manifold_x.get_critical_point(DOWN),
            manifold_y.get_critical_point(UP),
            color=WHITE,
            buff=0.1,
        )
        abstract_correspondence = VDict(
            {
                "arrow": abstract_correspondence,
                "label": MathTex(r"C").next_to(abstract_correspondence, RIGHT, buff=LABEL_BUFF * 2),
            }
        )

        pi_correspondence = DashedLine(
            input_space_x.get_critical_point(DOWN),
            input_space_y.get_critical_point(UP),
            color=WHITE,
            buff=0.1,
        )
        pi_correspondence = VDict(
            {
                "arrow": pi_correspondence,
                "label": MathTex(r"\pi").next_to(pi_correspondence, RIGHT, buff=LABEL_BUFF * 2),
            }
        )

        transformation = DashedLine(
            latent_space_x["embedding"].get_critical_point(DOWN),
            latent_space_y["embedding"].get_critical_point(UP),
            color=WHITE,
            buff=0.1,
        )
        transformation = VDict(
            {
                "arrow": transformation,
                "label": MathTex(r"\mathcal{T}").next_to(transformation, RIGHT, buff=LABEL_BUFF * 2),
            }
        )

        aligned = DashedVMobject(
            ArcBetweenPoints(
                universal_space_x["embedding"].get_critical_point(RIGHT) + RIGHT * 0.1 + DOWN * 0.1,
                universal_space_y["embedding"].get_critical_point(RIGHT) + RIGHT * 0.1 + UP * 0.1,
                angle=-1.5707963267948966 * 1.5,
            ),
            num_dashes=60,
            dashed_ratio=0.5,
        )
        aligned = VDict(
            {
                "arrow": aligned,
                "label": VGroup(
                    x := Circle(
                        radius=0.3,
                        color=BLACK,
                        fill_color=BLACK,
                        fill_opacity=1,
                    ).move_to(aligned.get_critical_point(RIGHT)),
                    MathTex(r"\approx").move_to(x.get_center()),
                ),
            }
        )

        fake_rec = SurroundingRectangle(
            VGroup(
                universal_space_x["embedding"],
                universal_space_y["embedding"],
                aligned,
            ),
            buff=0.25,
        )
        universal_space = DashedVMobject(
            RoundedRectangle(
                width=fake_rec.get_width(),
                height=fake_rec.get_height(),
                # fill_color=BLUE,
                # fill_opacity=0.2,
                stroke_color=BLUE,
                stroke_opacity=1,
            ),
            num_dashes=30,
        ).move_to(fake_rec.get_center())
        universal_space = VDict(
            {
                "rec": universal_space,
                "label": MathTex(r"U").next_to(universal_space, UR, buff=-0.65),
            }
        )

        all_elements = VGroup(
            formalization,
            manifold_x,
            manifold_y,
            phix,
            phiy,
            inputspaces_label,
            latentspaces_label,
            universalspaces_label,
            encoder_x,
            encoder_y,
            t_x,
            t_y,
            abstract_correspondence,
            pi_correspondence,
            transformation,
            aligned,
            universal_space,
        ).move_to(ORIGIN)

        self.add(all_elements)
        self.wait()
