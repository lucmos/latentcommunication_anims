from latentcommunication_anims.slides.formalization import X_COLOR, Y_COLOR
from manim import *
from manim_slides import Slide
from powermanim.layouts.arrangedbullets import Bullet, MathBullet
from powermanim.templates.bulletlist import BulletList
from torchvision.datasets import CIFAR100
from torchvision.transforms import transforms

from nn_core.common import PROJECT_ROOT

DISABLED_OPACITY = 0.4
FONT_SIZE = 28
SCALE_ACTIVE = 1.25
DATASET1 = CIFAR100(root=PROJECT_ROOT / "data", train=True, download=True)
# same as Dataset1 but with grayscale conversion
DATASET2 = CIFAR100(
    root=PROJECT_ROOT / "data",
    train=True,
    download=True,
    transform=transforms.Grayscale(),
)

ANCHORS_POINT_COLORS = [RED_D, GRAY_C, YELLOW_D]
SAMPLE_COLOR = GREEN


class TranslationAlgorithm(Slide):
    def construct(self):
        slide_title = Tex("Algorithm").to_edge(UP)

        self.play(Create(slide_title))

        algo = (
            MathBullet(
                r"\text{Given a subset } \mathbb{A}_",
                r"{X}",
                r"\text{ of the training set }",
                r"{X}",
                font_size=FONT_SIZE,
                group=0,
            ),
            MathBullet(
                r"\text{A subset }",
                r"{\mathbb{A}_",
                r"{Y}",
                r"}",
                r"\text{of the training set }",
                r"{Y}",
                font_size=FONT_SIZE,
                group=1,
            ),
            Bullet(
                r"And a \textbf{correspondence} between them",
                font_size=FONT_SIZE,
                group=2,
            ),
            MathBullet(
                r"\text{Apply the respective encoders }",
                r"E_",
                "X",
                r"\text{ and }",
                r"E_",
                "Y",
                font_size=FONT_SIZE,
                group=3,
            ),
            Bullet(
                r"Normalize the encodings",
                font_size=FONT_SIZE,
                group=4,
            ),
            Bullet(
                r"The \textbf{latent translation} operator $\mathcal{T}$ ",
                " is obtained via solving:",
                font_size=FONT_SIZE,
                group=5,
            ),
            MathBullet(
                r"\mathcal{T}(",
                r"\mathbf{x}",
                r") = \mathbf{R} \mathbb{A}_",
                r"{X}",
                r"+ \mathbf{b}",
                font_size=FONT_SIZE + 5,
                symbol=None,
                level=1,
                group=5,
                adjustment=UP * MED_LARGE_BUFF * 1.25 * 0.25,
            ),
        )
        for bullet_idx, element_idx, color in (
            (0, 1, X_COLOR),
            (0, 3, X_COLOR),
            (1, 2, Y_COLOR),
            (1, 5, Y_COLOR),
            (3, 2, X_COLOR),
            (3, 5, Y_COLOR),
            (6, 1, X_COLOR),
            (6, 3, X_COLOR),
        ):
            algo[bullet_idx][element_idx].set_color(color)

        bulletlist = BulletList(
            *algo,
            line_spacing=MED_LARGE_BUFF * 1.3,
            indent_buff=MED_LARGE_BUFF * 1.25,
            left_buff=MED_LARGE_BUFF,
            scale_active=1.25,
        ).shift(DOWN * 0.275)
        self.play(FadeIn(bulletlist), run_time=0.5)

        samples = [42, 7, 33]
        anchor_images1 = (
            Group(
                *[
                    ImageMobject(DATASET1[sample_idx][0], image_mode="RGB")
                    for sample_idx in samples
                ]
            )
            .scale(3.5)
            .arrange(RIGHT, buff=MED_LARGE_BUFF * 2)
            .to_edge(RIGHT)
            .shift(UP)
        )
        anchor_images2 = (
            Group(
                *[
                    ImageMobject(DATASET2[sample_idx][0], image_mode="RGB")
                    for sample_idx in samples
                ]
            )
            .scale(3.5)
            .arrange(RIGHT, buff=MED_LARGE_BUFF * 2)
            .to_edge(RIGHT)
            .next_to(anchor_images1, DOWN, buff=MED_LARGE_BUFF * 2)
        )

        correspondence = []
        for anchor_image1, anchor_image2 in zip(
            anchor_images1.submobjects, anchor_images2.submobjects
        ):
            correspondence.append(
                Line(
                    anchor_image1.get_bottom() + DOWN * 0.25,
                    anchor_image2.get_top() + UP * 0.25,
                    color=TEAL_D,
                    stroke_width=5,
                ),
            )

        semantic_alignment = SurroundingRectangle(
            Group(anchor_images1, anchor_images2, *correspondence),
            color=TEAL_D,
            stroke_width=5,
        )
        semantic_alignment_label = Tex(
            r"\textbf{Semantic Alignment!}", font_size=38
        ).next_to(semantic_alignment, UP)
        semantic_alignment = Group(semantic_alignment, semantic_alignment_label)

        self.wait(0.1)
        self.next_slide()
        # anchor1
        self.play(
            AnimationGroup(
                bulletlist.only_next(),
                run_time=1,
            ),
            FadeIn(anchor_images1),
        )

        self.wait(0.1)
        self.next_slide()
        # anchor2
        self.play(
            AnimationGroup(
                bulletlist.only_next(),
                run_time=1,
            ),
            FadeIn(anchor_images2),
        )

        self.wait(0.1)
        self.next_slide()
        # correspondence
        self.play(
            AnimationGroup(
                bulletlist.only_next(),
                AnimationGroup(*[FadeIn(c) for c in correspondence], lag_ratio=0.5),
                run_time=1.5,
            )
        )
        self.play(FadeIn(semantic_alignment))

        anims = []
        polygons = []
        regularized_anims = []

        np.random.seed(42)
        min_displacement = 0.05
        displacement_factor: float = 0.3
        for image, color in zip(anchor_images1.submobjects, ANCHORS_POINT_COLORS):
            polygon = Polygon(
                image.get_center()
                + UL
                * np.random.uniform(
                    min_displacement, image.width * displacement_factor
                ),
                image.get_center()
                + UR
                * np.random.uniform(
                    min_displacement, image.width * displacement_factor
                ),
                image.get_center()
                + DR
                * np.random.uniform(
                    min_displacement, image.width * displacement_factor
                ),
                image.get_center()
                + DL
                * np.random.uniform(
                    min_displacement, image.width * displacement_factor
                ),
                color=color,
                fill_opacity=1,
                z_index=1,
            )
            anims.append(
                AnimationGroup(
                    FadeOut(image),
                    FadeIn(polygon),
                    lag_ratio=0.5,
                )
            )
            polygons.append(polygon)

            polygon.target = Polygon(
                image.get_center() + UL * image.width * displacement_factor,
                image.get_center() + UR * image.width * displacement_factor,
                image.get_center() + DR * image.width * displacement_factor,
                image.get_center() + DL * image.width * displacement_factor,
                color=color,
                fill_opacity=1,
                z_index=1,
            )
            regularized_anims.append(MoveToTarget(polygon))

        np.random.seed(42)
        for image, color in zip(anchor_images2.submobjects, ANCHORS_POINT_COLORS):
            polygon = Polygon(
                image.get_center()
                + UP
                * np.random.uniform(
                    min_displacement, image.width * displacement_factor
                ),
                image.get_center()
                + LEFT
                * np.random.uniform(
                    min_displacement, image.width * displacement_factor
                ),
                image.get_center()
                + RIGHT
                * np.random.uniform(
                    min_displacement, image.width * displacement_factor
                ),
                color=color,
                fill_opacity=1,
                z_index=1,
            )
            anims.append(
                AnimationGroup(
                    FadeOut(image),
                    FadeIn(polygon),
                    lag_ratio=0.5,
                )
            )
            polygons.append(polygon)

            polygon.target = Polygon(
                image.get_center() + UP * 2 * image.width * displacement_factor,
                image.get_center() + LEFT * image.width * displacement_factor,
                image.get_center() + RIGHT * image.width * displacement_factor,
                color=color,
                fill_opacity=1,
                z_index=1,
            )
            regularized_anims.append(MoveToTarget(polygon))

        self.wait(0.1)
        self.next_slide()
        # encoding
        self.play(
            AnimationGroup(
                AnimationGroup(
                    bulletlist.only_next(),
                    run_time=1,
                ),
                AnimationGroup(
                    AnimationGroup(
                        *anims[: len(anims) // 2],
                        lag_ratio=0.5,
                        run_time=1,
                    ),
                    AnimationGroup(
                        *anims[len(anims) // 2 :],
                        lag_ratio=0.5,
                        run_time=1,
                    ),
                ),
                lag_ratio=0.5,
            ),
        )

        self.wait(0.1)
        self.next_slide()

        # regularization
        self.play(
            AnimationGroup(
                bulletlist.only_next(),
                AnimationGroup(
                    AnimationGroup(
                        *regularized_anims[: len(regularized_anims) // 2],
                        lag_ratio=0.5,
                        run_time=1.5,
                    ),
                    AnimationGroup(
                        *regularized_anims[len(regularized_anims) // 2 :],
                        lag_ratio=0.5,
                        run_time=1.5,
                    ),
                ),
                lag_ratio=0.5,
            ),
        )

        self.wait(0.1)
        self.next_slide()
        self.play(bulletlist.only_next())

        arrow = Arrow(0.2 * RIGHT, 0.2 * LEFT).next_to(
            bulletlist[-1][-1], RIGHT, buff=MED_LARGE_BUFF * 2
        )
        arrow_label = Tex(r"\textbf{Mostly orthogonal!}", font_size=38).next_to(
            arrow, RIGHT
        )

        self.wait(0.1)
        self.next_slide()
        self.play(
            AnimationGroup(
                AnimationGroup(
                    GrowArrow(arrow),
                    FadeIn(arrow_label),
                ),
                ShowPassingFlash(Underline(arrow_label, color=YELLOW)),
                lag_ratio=0.5,
            )
        )

        self.wait(0.1)
        self.next_slide(auto_next=True)
        self.play(
            FadeOut(arrow),
            FadeOut(arrow_label),
            FadeOut(bulletlist),
            FadeOut(slide_title),
            FadeOut(semantic_alignment),
            *(
                FadeOut(x, shift=DOWN, run_time=1.5)
                for x in (*correspondence, *polygons)
            ),
        )

    # TODO: Clarify assumption!
