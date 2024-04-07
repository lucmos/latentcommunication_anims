import itertools

from manim import *
from manim_slides import Slide
from powermanim.layouts.arrangedbullets import Bullet, MathBullet
from powermanim.templates.bulletlist import BulletList
from torchvision.datasets import MNIST

from nn_core.common import PROJECT_ROOT

from latentcommunication_anims.utils import section_slide

DISABLED_OPACITY = 0.4
FONT_SIZE = 28
SCALE_ACTIVE = 1.25
DATASET = MNIST(root=PROJECT_ROOT / "data", train=True, download=True)

ANCHORS_COLOR = RED
ANCHORS_POINT_COLORS = [RED_A, RED_C, RED_E]
SAMPLE_COLOR = GREEN
SIM_COLOR = BLUE


class RelRepsAlgo(Slide):
    def construct(self):
        section_slide(self, "Relative Representations")

        slide_title = Tex("Algorithm").to_edge(UP)

        self.play(Create(slide_title))

        algo = (
            Bullet(
                r"Select a subset",
                " $\mathbb{A}$ ",
                "of the training set $\mathbb{X}$, denoted ",
                r"\textbf{anchors}",
                font_size=FONT_SIZE,
                group=0,
            ),
            Bullet(
                r"Consider each ",
                r"\textbf{sample} $x$",
                font_size=FONT_SIZE,
                group=1,
            ),
            Bullet(
                r"Consider an encoding function $E$",
                font_size=FONT_SIZE,
                group=2,
            ),
            Bullet(
                r"Choose a similarity function ",
                "$sim$",
                font_size=FONT_SIZE,
                group=3,
            ),
            Bullet(
                r"The \textbf{relative representation} of ",
                "$x$",
                " is:",
                font_size=FONT_SIZE,
                group=4,
            ),
            MathBullet(
                r"\mathbf{r}_{",
                r"\mathbf{x}^{(i)}",
                r"} = (",
                "sim",
                "(",
                "\mathbf{e}_{\mathbf{x}^{(i)}}",
                ", ",
                "\mathbf{e}_{\mathbf{a}^{(1)}}",
                "),",
                "sim",
                "(",
                "\mathbf{e}_{\mathbf{x}^{(i)}}",
                ", ",
                "\mathbf{e}_{\mathbf{a}^{(2)}}",
                "),\dots,",
                "sim",
                "(",
                "\mathbf{e}_{\mathbf{x}^{(i)}}",
                ", ",
                "\mathbf{e}_{\mathbf{a}^{(|\mathbb{A}|)}}",
                "))",
                font_size=FONT_SIZE + 5,
                symbol=None,
                level=1,
                group=4,
                adjustment=UP * MED_LARGE_BUFF * 1.25 * 0.25,
            ),
        )
        algo[0][1].set_color(ANCHORS_COLOR)
        algo[0][3].set_color(ANCHORS_COLOR)
        algo[1][1].set_color(SAMPLE_COLOR)
        algo[-2][1].set_color(SAMPLE_COLOR)
        algo[3][1].set_color(SIM_COLOR)
        for color, entity_idxs in (
            (SIM_COLOR, [3, 9, 15]),
            (SAMPLE_COLOR, [1, 5, 11, 17]),
        ):
            for entity_idx in entity_idxs:
                algo[-1][entity_idx].set_color(color)
        for color, entity_idx in zip(ANCHORS_POINT_COLORS, [7, 13, 19]):
            algo[-1][entity_idx].set_color(color)

        bulletlist = BulletList(
            *algo,
            line_spacing=MED_LARGE_BUFF * 1.3,
            indent_buff=MED_LARGE_BUFF * 1.25,
            left_buff=MED_LARGE_BUFF,
            scale_active=1.25,
        ).shift(DOWN * 0.275)
        self.play(FadeIn(bulletlist), run_time=0.5)

        self.wait(0.5)
        self.next_slide()
        anchor_images = (
            Group(*[ImageMobject(DATASET[sample_idx][0], image_mode="RGB") for sample_idx in [0, 1, 3]])
            .scale(2)
            .arrange(RIGHT, buff=MED_LARGE_BUFF * 2)
            .to_edge(RIGHT)
            .shift(UP)
        )
        anchors_brace = BraceText(
            anchor_images,
            text=r"\textbf{anchors}",
            brace_direction=UP,
            font_size=38,
        )
        anchors_brace.label.set_color(ANCHORS_COLOR)
        self.play(
            AnimationGroup(
                bulletlist.only_next(),
                run_time=1,
            ),
            FadeIn(anchor_images),
            Create(anchors_brace),
        )

        self.wait(0.5)
        self.next_slide()
        sample_image = (
            ImageMobject(DATASET[4][0], image_mode="RGB")
            .scale(2)
            .align_to(anchor_images.submobjects[1], RIGHT)
            .shift(DOWN)
        )
        sample_brace = Tex(r"\textbf{sample}", color=SAMPLE_COLOR, font_size=38).next_to(sample_image, DOWN)
        self.play(
            AnimationGroup(
                bulletlist.only_next(),
                run_time=1,
            ),
            FadeIn(sample_image),
            Create(sample_brace),
        )

        self.wait(0.5)
        self.next_slide()
        anims = []
        dots = []
        for image, color in zip(
            itertools.chain(anchor_images.submobjects, [sample_image]),
            [*ANCHORS_POINT_COLORS, SAMPLE_COLOR],
        ):
            anims.append(
                AnimationGroup(
                    FadeOut(image),
                    FadeIn(
                        d := Dot(
                            point=image.get_center(),
                            radius=0.15,
                            color=color,
                            fill_opacity=1,
                            z_index=1,
                        )
                    ),
                    lag_ratio=0.5,
                )
            )
            dots.append(d)
        *anchors_dots, sample_dot = dots
        self.play(
            AnimationGroup(
                AnimationGroup(
                    bulletlist.only_next(),
                    run_time=1,
                ),
                AnimationGroup(
                    *anims,
                    lag_ratio=0.5,
                    run_time=2.5,
                ),
                lag_ratio=0.5,
            ),
        )

        self.wait(0.5)
        self.next_slide()
        self.play(
            AnimationGroup(
                bulletlist.only_next(),
                run_time=1,
            )
        )

        self.wait(0.5)
        self.next_slide()
        lines_anim = []
        lines = []
        for anchor in anchors_dots:
            lines_anim.append(
                Create(l := Line(anchor.get_center(), sample_dot.get_center(), color=SIM_COLOR).set_opacity(0.5))
            )
            lines.append(l)
        self.play(
            AnimationGroup(
                bulletlist.only_next(),
                run_time=1,
            ),
            AnimationGroup(*lines_anim, lag_ratio=0.5, run_time=3),
        )

        self.wait(0.5)
        self.next_slide()
        rendered_code = (
            Code(
                code="""import torch
import torch.nn.functional as F

def relative_projection(x, anchors):
\tx = F.normalize(x, p=2, dim=-1)
\tanchors = F.normalize(anchors, p=2, dim=-1)
\treturn torch.einsum("nd, ad -> na", x, anchors)""",
                tab_width=3,
                language="Python",
                style="monokai",
                insert_line_no=False,
                font_size=18,
            )
            .to_edge(LEFT, buff=LARGE_BUFF)
            .align_to(
                VGroup(*dots),
                direction=UP,
            )
        )

        cosine_label = Tex("$sim$", " $=$ ", "cosine similarity", font_size=38).next_to(rendered_code, UP)
        cosine_label[0].set_color(SIM_COLOR)

        self.play(
            AnimationGroup(
                FadeOut(bulletlist, shift=LEFT),
                AnimationGroup(
                    FadeIn(cosine_label, shift=RIGHT),
                    FadeIn(rendered_code, shift=RIGHT),
                    lag_ratio=0.5,
                ),
                lag_ratio=0.75,
                run_time=1.5,
            )
        )

        differentiable = Tex("(differentiable!)").next_to(rendered_code, DOWN, buff=LARGE_BUFF).set_opacity(0.5)
        self.play(FadeIn(differentiable))

        self.wait()
        self.next_slide()

        title = Tex(f"Properties").to_edge(UP)

        properties = (
            MathBullet(
                r"\mathbf{r}_{",
                r"\mathbf{x}^{(i)}",
                r"} \text{ is a universal representation computed \emph{independently} for each space }",
                font_size=FONT_SIZE,
            ),
            MathBullet(
                r"\text{The size of } \mathbf{r}_{",
                r"\mathbf{x}^{(i)}",
                r"} \text{ depends on the number of }",
                r"\text{anchors }",
                r"|",
                r"\mathbb{A}",
                r"|",
                font_size=FONT_SIZE,
            ),
            Bullet(
                r"The ",
                r"anchors",
                r" and ",
                r"similarity",
                r" function choices determine the representation \emph{properties}",
                font_size=FONT_SIZE,
                force_inline=True,
            ),
        )
        properties[0][1].set_color(SAMPLE_COLOR)

        properties[1][1].set_color(SAMPLE_COLOR)
        properties[1][3].set_color(ANCHORS_COLOR)
        properties[1][5].set_color(ANCHORS_COLOR)

        properties[2][1].set_color(ANCHORS_COLOR)
        properties[2][3].set_color(SIM_COLOR)

        properties_list = BulletList(
            *properties,
            left_buff=MED_LARGE_BUFF * 1.5,
            scale_active=1.15,
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    *(
                        Uncreate(x)
                        for x in [
                            differentiable,
                            cosine_label,
                            rendered_code,
                            *lines,
                            *anchors_dots,
                            sample_dot,
                            anchors_brace,
                            sample_brace,
                        ]
                    )
                ),
                ReplacementTransform(slide_title, title),
                FadeIn(properties_list),
                lag_ratio=0.5,
            )
        )

        self.wait()
        self.next_slide()
        self.play(properties_list.also_next())

        self.wait()
        self.next_slide()
        self.play(properties_list.also_next())

        self.wait()
        self.next_slide()
        self.play(properties_list.also_next())

        self.wait()
        self.next_slide()

        cosine = Tex("$\mathbf{sim}$", " $=$ ", "cosine similarity", font_size=34).shift(DOWN)
        cosine[0].set_color(SIM_COLOR)

        arrow = Arrow(0.5 * UP, 0.5 * DOWN).next_to(cosine, DOWN, buff=MED_LARGE_BUFF)
        invariance = Tex(
            r"invariant to \textbf{angle-norm preserving transformations} of the latent space",
            font_size=34,
        ).next_to(arrow, DOWN, buff=MED_LARGE_BUFF)

        self.play(
            AnimationGroup(
                properties_list.animate.shift(UP * 1.2),
                AnimationGroup(
                    AnimationGroup(FadeIn(cosine)),
                    GrowArrow(arrow),
                    Create(invariance),
                    lag_ratio=0.75,
                ),
                lag_ratio=0.15,
            ),
            run_time=3,
        )
        self.play(
            AnimationGroup(
                ShowPassingFlash(Underline(cosine, color=YELLOW)),
                ShowPassingFlash(Underline(invariance, color=YELLOW)),
                lag_ratio=0.5,
                run_time=2,
            )
        )

        self.wait()
        self.next_slide(auto_next=True)
        self.play(*(FadeOut(x) for x in (title, properties_list, cosine, arrow, invariance)))

        self.wait(0.1)
