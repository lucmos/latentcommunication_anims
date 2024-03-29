import typing as tp
from functools import partial
from math import copysign

from manim import *
from manim_slides.slide import Slide
from powermanim import Bullet, BulletList, DirectionalArrow, GroupActivable, VAutoActivable
from powermanim.templates.sectiontitle import Color

from latentcommunication_anims.utils import section_slide

X_COLOR = RED
Y_COLOR = GREEN

MANIFOLD_EMBEDDING_Y_SHIFT = 0.325

MANIFOLD_BUFF = 1.75
AMBIENTS_HORIZ_BUFF = 1.5
AMBIENTS_VERT_BUFF = 1.25

LABEL_SCALE = 0.8

LABEL_BUFF = 0.075

FONT_SIZE = 38


def _set_tex_colors(texobj: MathTex, indices: tp.Sequence[int], color: Color):
    for i in indices:
        texobj[i].set_color(color)


# class Formalization(Scene):
class Formalization(Slide):
    def build_ambient_space(
        self,
        label_text: tp.Sequence[str],
        inner_manifold: VMobject,
        manifold_embedding_y_shift,
        color,
        size=2.5,
    ):
        if isinstance(label_text, str):
            label_text = (label_text,)

        shift_direction = UP * copysign(1, manifold_embedding_y_shift)
        ambient_space = Square(side_length=size, stroke_color=LIGHTER_GREY)
        inner_manifold = inner_manifold.set_color(color=WHITE)

        inner_manifold.scale_to_fit_height(ambient_space.get_height() * 0.4)

        inner_manifold.move_to(ambient_space.get_critical_point(LEFT))
        inner_manifold.shift(
            UP * manifold_embedding_y_shift,
        )
        inner_manifold.shift(
            np.asarray(
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
        )

        label = MathTex(*label_text)
        if len(label) == 1:
            label.set_color(color)
        else:
            label[1].set_color(color)

        midpoint = (
            ambient_space.get_critical_point(-shift_direction) + inner_manifold.get_critical_point(-shift_direction)
        ) / np.asarray(2)
        label.move_to((ambient_space.get_center()[0], midpoint[1], 0))

        return VDict({"label": label, "space": ambient_space, "embedding": inner_manifold})

    def construct(self) -> None:
        input_space_x = self.build_ambient_space(
            label_text="X",
            inner_manifold=RegularPolygon(5),
            manifold_embedding_y_shift=MANIFOLD_EMBEDDING_Y_SHIFT,
            color=X_COLOR,
        )

        input_space_y = self.build_ambient_space(
            label_text="Y",
            inner_manifold=DashedVMobject(RegularPolygon(5)),
            manifold_embedding_y_shift=-MANIFOLD_EMBEDDING_Y_SHIFT,
            color=Y_COLOR,
        )

        latent_space_x = self.build_ambient_space(
            label_text=r"\widetilde{X}",
            inner_manifold=(RegularPolygon(7)),
            manifold_embedding_y_shift=MANIFOLD_EMBEDDING_Y_SHIFT,
            color=X_COLOR,
        )

        latent_space_y = self.build_ambient_space(
            label_text=r"\widetilde{Y}",
            inner_manifold=DashedVMobject(RegularPolygon(7)),
            manifold_embedding_y_shift=-MANIFOLD_EMBEDDING_Y_SHIFT,
            color=Y_COLOR,
        )

        universal_space_x = self.build_ambient_space(
            label_text=("U_", "{X}"),
            inner_manifold=(RegularPolygon(16)),
            manifold_embedding_y_shift=MANIFOLD_EMBEDDING_Y_SHIFT,
            color=X_COLOR,
        )

        universal_space_y = self.build_ambient_space(
            label_text=("U_", "{Y}"),
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

        INACTIVE = 0

        shape_highlightable = partial(
            VAutoActivable,
            scale_active=None,
            active_fill_opacity=None,
            inactive_fill_opacity=None,
            active_stroke_opacity=1.0,
            inactive_stroke_opacity=INACTIVE,
        )
        label_highlightable = partial(
            VAutoActivable,
            scale_active=None,
            active_fill_opacity=1.0,
            inactive_fill_opacity=INACTIVE,
            active_stroke_opacity=1.0,
            inactive_stroke_opacity=INACTIVE,
        )

        all_elements = GroupActivable(
            label_highlightable(inputspaces_label, group=0),
            label_highlightable(x_pipeline["input"]["label"], group=0),
            shape_highlightable(x_pipeline["input"]["space"], group=0),
            label_highlightable(y_pipeline["input"]["label"], group=0),
            shape_highlightable(y_pipeline["input"]["space"], group=0),
            #
            label_highlightable(manifold_x, group=1),
            label_highlightable(manifold_y, group=1),
            #
            label_highlightable(phix, group=2),
            label_highlightable(phiy, group=2),
            shape_highlightable(x_pipeline["input"]["embedding"], group=2),
            shape_highlightable(y_pipeline["input"]["embedding"], group=2),
            #
            label_highlightable(abstract_correspondence, group=3),
            label_highlightable(pi_correspondence, group=4),
            #
            #
            label_highlightable(encoder_x, group=5),
            label_highlightable(encoder_y, group=5),
            #
            label_highlightable(latentspaces_label, group=6),
            label_highlightable(x_pipeline["latent"]["label"], group=6),
            shape_highlightable(x_pipeline["latent"]["space"], group=6),
            label_highlightable(y_pipeline["latent"]["label"], group=6),
            shape_highlightable(y_pipeline["latent"]["space"], group=6),
            #
            shape_highlightable(x_pipeline["latent"]["embedding"], group=7),
            shape_highlightable(y_pipeline["latent"]["embedding"], group=7),
            #
            label_highlightable(transformation, group=8),
            #
            label_highlightable(t_x, group=9),
            label_highlightable(t_y, group=9),
            #
            label_highlightable(universalspaces_label, group=10),
            label_highlightable(y_pipeline["universal"]["label"], group=10),
            label_highlightable(x_pipeline["universal"]["label"], group=10),
            shape_highlightable(x_pipeline["universal"]["space"], group=10),
            shape_highlightable(y_pipeline["universal"]["space"], group=10),
            #
            shape_highlightable(x_pipeline["universal"]["embedding"], group=11),
            shape_highlightable(y_pipeline["universal"]["embedding"], group=11),
            #
            label_highlightable(aligned, group=12),
            #
            shape_highlightable(universal_space["rec"], group=13),
            label_highlightable(universal_space["label"], group=13),
            anim_lag_ratio=0.25,
        ).move_to(ORIGIN)

        a = VGroup(
            inputspaces_label,
            x_pipeline["input"]["label"],
            x_pipeline["input"]["space"],
            y_pipeline["input"]["label"],
            y_pipeline["input"]["space"],
            manifold_x,
            manifold_y,
            phix,
            phiy,
            x_pipeline["input"]["embedding"],
            y_pipeline["input"]["embedding"],
            abstract_correspondence,
            pi_correspondence,
            encoder_x,
            encoder_y,
            latentspaces_label,
            x_pipeline["latent"]["label"],
            x_pipeline["latent"]["space"],
            y_pipeline["latent"]["label"],
            y_pipeline["latent"]["space"],
            x_pipeline["latent"]["embedding"],
            y_pipeline["latent"]["embedding"],
            transformation,
        ).move_to(ORIGIN)

        # ----------- START ANIMATIONS

        section_slide(self, section_title=r"The Latent Communication\\Problem")

        general_problem = Tex(r"Searching for a Universal Space or a Direct Translation")
        general_problem2 = Tex(r"are instances of the same \textbf{general} problem!").next_to(
            general_problem, DOWN, buff=MED_LARGE_BUFF * 2
        )
        VGroup(general_problem, general_problem2).move_to(ORIGIN)
        self.play(AnimationGroup(FadeIn(general_problem), FadeIn(general_problem2), lag_ratio=0.5))
        self.wait(0.1)
        self.next_slide()

        framework_intro = Tex("Consider the following setting")
        self.play(FadeOut(general_problem, general_problem2))
        self.play(Create(framework_intro))
        self.wait(0.1)
        self.next_slide()

        self.play(
            FadeOut(framework_intro),
            FadeIn(all_elements.align_to(a, LEFT)),
        )
        for _ in range(9):
            self.play(all_elements.also_next())
            self.wait(0.1)
            self.next_slide()

        self.play(all_elements.animate.move_to(ORIGIN))

        for _ in range(all_elements.ngroups - 8 - 1):
            self.play(all_elements.also_next())
            self.wait(0.1)
            self.next_slide()

        formalization_title = Tex("Latent Communication Problem").to_edge(UP)

        self.play(FadeOut(all_elements))

        problemfind = MathTex(
            r"\text{Search} \quad T_{",  # 0
            r"X",  # 1
            r"}: ",  # 2
            r"\widetilde{X}",  # 3
            r"\to",  # 4
            r"U_{",  # 5
            r"X",  # 6
            r"}",  # 7
            r" \quad \text{ and } \quad ",  # 8
            r"T_{",  # 9
            r"Y",  # 10
            r"}:",  # 11
            r"\widetilde{Y}",  # 12
            r"\to",  # 13
            r"U_{",  # 14
            r"Y",  # 15
            r"}",  # 16
        )
        _set_tex_colors(texobj=problemfind, indices=(1, 3, 6), color=X_COLOR)
        _set_tex_colors(texobj=problemfind, indices=(10, 12, 15), color=Y_COLOR)

        problemloss = MathTex(
            r"\forall (",  # 0
            r"x",  # 1
            r", ",  # 2
            r"y",  # 3
            r") \in C, ",  # 4
            r"\quad ",  # 5
            r"T_{",  # 6
            r"X",  # 7
            r"}(E_",  # 8
            r"X",  # 9
            r"(\varphi_{",  # 10
            r"X",  # 11
            r"}(",  # 12
            r"x",  # 13
            r")))",  # 14
            r" = ",  # 15
            r"T_{",  # 16
            r"Y",  # 17
            r"}(E_",  # 18
            r"Y",  # 19
            r"(\varphi_{",  # 20
            r"Y",  # 21
            r"}(",  # 22
            r"y",  # 23
            r")))",  # 24
            r" \subseteq{U}",  # 25
        )
        _set_tex_colors(texobj=problemloss, indices=(1, 7, 9, 11, 13), color=X_COLOR)
        _set_tex_colors(texobj=problemloss, indices=(3, 17, 19, 21, 23), color=Y_COLOR)
        st = Tex("such that")
        constraint = MathTex(
            r"\mathcal{L}(",  # 0
            r"\widetilde{X}",  # 1
            r")",  # 2
            " = ",  # 3
            r"\mathcal{L}(U_{",  # 4
            r"X",  # 5
            r"})",  # 6
            r" \quad\text{ and }\quad ",  # 7
            r"\mathcal{L}(",  # 8
            r"\widetilde{Y}",  # 9
            r")",  # 10
            " = ",  # 11
            r"\mathcal{L}(U_{",  # 12
            r"Y",  # 13
            r"})",  # 14
        )
        _set_tex_colors(texobj=constraint, indices=(1, 5), color=X_COLOR)
        _set_tex_colors(texobj=constraint, indices=(9, 13), color=Y_COLOR)
        clarification = Tex(r"where $\mathcal{L}$ is the minimum achievable loss, by any model")
        statement = (
            VGroup(problemfind, problemloss, st, constraint, clarification).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        )
        clarification.shift(DOWN)
        self.play(
            AnimationGroup(
                FadeIn(formalization_title),
                FadeIn(statement),
                lag_ratio=0.5,
            ),
        )
        self.wait()
        self.next_slide()

        intuitiontitle = Tex("Essentially").to_edge(UP)
        intuition = Tex("Searching for transformations of the latent ambient spaces")
        intuition2 = Tex("that implicitly align the manifolds embedded in them")
        intutiongroup = VGroup(intuition, intuition2).arrange(DOWN, buff=1).move_to(ORIGIN)
        self.play(
            AnimationGroup(
                AnimationGroup(
                    AnimationGroup(FadeOut(statement), FadeOut(formalization_title)),
                    FadeIn(intuitiontitle),
                    lag_ratio=0.5,
                ),
                FadeIn(intuition),
                FadeIn(intuition2),
                lag_ratio=0.5,
            )
        )

        self.wait(0.5)
        self.next_slide()

        corollaryproblems = Tex("Corollary Problems").to_edge(UP)

        bulletlist = (
            BulletList(
                Bullet("Zero-Shot Stitching", font_size=FONT_SIZE, level=0),
                Bullet("Reuse neural components without finetuning", font_size=FONT_SIZE, level=1, symbol=""),
                Bullet("Latent Model Evaluation", font_size=FONT_SIZE, level=0),
                Bullet(
                    "Measure models performance implicitly in the latent space",
                    font_size=FONT_SIZE,
                    level=1,
                    symbol="",
                ),
                Bullet(r"Retrieval", font_size=FONT_SIZE, level=0),
                Bullet(
                    "Retrieve data points from one space using queries from another",
                    font_size=FONT_SIZE,
                    level=1,
                    symbol="",
                ),
                line_spacing=MED_LARGE_BUFF,
                scale_active=1.025,
                inactive_opacity=0.35,
            )
            .move_to(ORIGIN)
            .to_edge(LEFT)
            .shift(DOWN * 0.25)
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    AnimationGroup(FadeOut(intutiongroup), FadeOut(intuitiontitle)),
                    FadeIn(corollaryproblems),
                    lag_ratio=0.5,
                ),
                FadeIn(bulletlist),
                lag_ratio=0.5,
            )
        )
        self.wait(0.5)
        self.next_slide()

        for i in range(bulletlist.ngroups):
            self.play(bulletlist.also_next())
            self.wait(0.1)
            self.next_slide(auto_next=i == bulletlist.ngroups - 1)

        self.play(FadeOut(bulletlist), FadeOut(corollaryproblems))
        self.wait(0.1)
