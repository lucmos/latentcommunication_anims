from manim import *
from manim_slides import Slide

from nn_core.common import PROJECT_ROOT

from latentcommunication_anims.utils import TARGET_COLORS, get_run_opt, section_slide

MNIST_DIGIT_IN = PROJECT_ROOT / "data" / "assets" / "mnist" / "8_sample_94.png"
# MNIST_DIGIT_OUT = PROJECT_ROOT / "data" / "assets" / "mnist" / "blurred_8_sample_94.png"

LATENT_SPACE_SHAPE_TEXT = "The shape of the latent space"

TOY_RUN_ID = "optpcpnm"

N_POINTS = 100

EVIDENCE_POINT = 3


class ShapeLatentSpace(Slide):
    def absolute_difference_interleave(self):
        slide_title = Tex(r"Latent Space Contributing Factors").to_edge(UP)

        # contributing_factors = Tex(r"\emph{Contributing factors...}", font_size=38)
        # contributing_factors.next_to(slide_title, DOWN, buff=MED_LARGE_BUFF)

        section_font_size = 42

        ideally_title = (
            Tex("Ideally", font_size=section_font_size).next_to(slide_title, DOWN, buff=LARGE_BUFF).shift(LEFT * 4)
        )

        practice_title = (
            Tex(r"In practice", font_size=section_font_size)
            .next_to(slide_title, DOWN, buff=LARGE_BUFF)
            .to_edge(RIGHT * 4)
        )

        font_size = 38
        ideally = [
            r"\textbullet~Data Distribution",
            r"\textbullet~The task",
            r"\textbullet~Additional constraints (implicit or explicit)",
            r"\textbullet~Data Semantics",
        ]
        ideally_list = (
            VGroup(*(Tex(x, font_size=font_size) for x in ideally))
            .arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)
            .to_edge(LEFT)
        )

        practice = [
            r"\textbullet~Parameter initialization",
            r"\textbullet~Data shuffling",
            r"\textbullet~Training seed",
            r"\textbullet~Hyperparameters",
            r"\textbullet~Data Modality",
            r"\textbullet~...",
        ]
        practice_list = (
            VGroup(*(Tex(x, font_size=font_size) for x in practice))
            .arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)
            .to_edge(RIGHT)
        )

        ideally_list.next_to(ideally_title, DOWN, buff=MED_LARGE_BUFF).to_edge(LEFT)
        practice_list.next_to(practice_title, DOWN, buff=MED_LARGE_BUFF).to_edge(RIGHT)

        self.play(FadeIn(slide_title, run_time=0.75, shift=DOWN))

        # self.play(
        #     Create(contributing_factors),
        #     # ShowPassingFlashWithThinningStrokeWidth(contributing_factors),
        # )

        self.wait(0.1)
        self.next_slide()

        self.play(
            AnimationGroup(
                FadeIn(ideally_title),
                Create(
                    ideally_list,
                    lag_ratio=1,
                    run_time=2,
                ),
                lag_ratio=0.5,
            )
        )

        self.wait(0.1)
        self.next_slide()

        self.play(
            AnimationGroup(
                FadeIn(practice_title),
                Create(
                    practice_list,
                    lag_ratio=1,
                    run_time=2,
                ),
                lag_ratio=0.5,
            )
        )

        self.wait(0.1)
        self.next_slide()

        self.play(Create(cross := Cross(VGroup(practice_title, practice_list))))

        self.wait(0.1)
        self.next_slide()

        self.play(
            FadeOut(slide_title, shift=UP),
            # FadeOut(contributing_factors, shift=UP),
            FadeOut(ideally_title, shift=UP),
            FadeOut(practice_title, shift=UP),
            FadeOut(ideally_list, shift=UP),
            FadeOut(practice_list, shift=UP),
            FadeOut(cross, shift=UP),
        )

    def construct(self):
        df = get_run_opt(TOY_RUN_ID)
        max_step = df["step"].max()
        df = df[df["step"] == max_step]

        sample_ids = list(df["sample_id"])[:N_POINTS]
        evidence_point_df = df[df.sample_id == sample_ids[EVIDENCE_POINT]]
        del sample_ids[EVIDENCE_POINT]

        x_range = [df.dim_0.min(), df.dim_0.max()]
        y_range = [df.dim_1.min(), df.dim_1.max()]
        min_range = min(x_range[0], y_range[0], -x_range[1], -y_range[1])
        max_range = -min_range

        section_slide(self, LATENT_SPACE_SHAPE_TEXT, auto_next=True)

        self.absolute_difference_interleave()

        self.wait(0.1)
        self.next_slide(auto_next=True)

        embedding = Rectangle(height=2, width=0.5, fill_opacity=0.5)
        encoder = Polygon(2 * UP + LEFT, RIGHT + UP, RIGHT + DOWN, 2 * DOWN + LEFT, fill_opacity=0.5).next_to(
            embedding, LEFT
        )
        decoder = Polygon(RIGHT + 2 * UP, RIGHT + 2 * DOWN, DOWN + LEFT, UP + LEFT, fill_opacity=0.5).next_to(
            embedding, RIGHT
        )
        arrowl = Arrow(LEFT / 2, RIGHT / 2).next_to(encoder, LEFT)
        data_in = Tex("Data").next_to(arrowl, LEFT)
        encoder_label = Tex("Encoder").next_to(encoder, UP)
        decoder_label = Tex("Decoder").next_to(decoder, UP)
        tasks = VGroup(Tex("Generation"), Tex("Classification"), Tex("Reconstruction"), Tex(f"\dots")).arrange(
            direction=DOWN,
            buff=MED_LARGE_BUFF,
            aligned_edge=LEFT,
        )
        brace = Brace(tasks, LEFT).next_to(decoder, RIGHT)
        tasks.next_to(brace, RIGHT)

        model = VGroup(encoder, decoder, embedding, encoder_label, decoder_label, data_in, arrowl, brace, tasks).shift(
            DOWN * 0.5
        )

        toy_model1 = Tex("Bidimensional")
        toy_model2 = Tex("AutoEncoder")
        toy_model = VGroup(toy_model1, toy_model2).arrange(RIGHT, buff=0.2).to_edge(UP)

        self.play(
            AnimationGroup(Create(toy_model), FadeIn(model, shift=DOWN * 0.5)),
            AnimationGroup(
                *(tasks.submobjects[i].animate.set_opacity(0.4) for i in (0, 1, 3)),
            ),
            lag_ratio=0.9,
        )

        self.wait(0.1)
        self.next_slide()

        digit = ImageMobject(MNIST_DIGIT_IN)
        digit.rescale_to_fit(length=decoder.height * 0.75, dim=1).next_to(arrowl, LEFT)

        self.play(GrowFromCenter(digit), FadeOut(data_in))

        self.wait(0.1)
        self.next_slide()

        latent_y = Rectangle(height=1, width=0.5, fill_opacity=0.5, color=TEAL).align_to(embedding, UP)
        latent_x = Rectangle(height=1, width=0.5, fill_opacity=0.5, color=PURPLE).align_to(embedding, DOWN)

        bilatent = VGroup(latent_y, latent_x)
        number_y = (
            DecimalNumber(
                float(evidence_point_df.dim_1),
                fill_opacity=0.75,
            )
            .scale(0.8)
            .next_to(latent_y, UP)
        )
        number_x = (
            DecimalNumber(
                float(evidence_point_df.dim_0),
                fill_opacity=0.75,
            )
            .scale(0.8)
            .next_to(latent_x, DOWN)
        )

        self.play(
            FadeOut(embedding),
            FadeIn(bilatent),
            ShowPassingFlash(Underline(toy_model1, color=YELLOW)),
            Create(number_y),
            Create(number_x),
        )

        self.wait(0.1)
        self.next_slide()

        arrowr = Arrow(LEFT / 2, RIGHT / 2)
        arrowr.add_updater(lambda x: x.next_to(decoder, RIGHT))
        arrowr.update(0)

        # out_digit = Image.open(MNIST_DIGIT_OUT)
        # out_digit = out_digit.filter(ImageFilter.GaussianBlur(1))
        out_digit = ImageMobject(MNIST_DIGIT_IN)
        out_digit.rescale_to_fit(length=decoder.height * 0.75, dim=1).next_to(arrowr, RIGHT)

        self.play(GrowFromCenter(out_digit), FadeOut(tasks), Transform(brace, arrowr))

        self.wait(0.1)
        self.next_slide()

        self.play(
            Uncreate(encoder),
            Uncreate(decoder),
            Uncreate(encoder_label),
            Uncreate(decoder_label),
            FadeOut(digit),
            FadeOut(out_digit),
            Uncreate(arrowl),
            Uncreate(brace),
        )

        axes = Axes(
            x_range=(min_range, max_range, -1),
            y_range=(min_range, max_range, -1),
        ).shift(DOWN * 0.25)
        axes.y_axis.set_color(latent_y.get_color())
        axes.x_axis.set_color(latent_x.get_color())

        self.wait(0.1)
        self.next_slide()

        self.play(
            AnimationGroup(
                AnimationGroup(
                    ReplacementTransform(latent_y, axes.y_axis),
                    number_y.animate.next_to(axes.y_axis.number_to_point(number_y.get_value()), LEFT),
                ),
                AnimationGroup(
                    ReplacementTransform(latent_x, axes.x_axis),
                    number_x.animate.next_to(axes.x_axis.number_to_point(number_x.get_value()), DOWN),
                ),
                lag_ratio=0.25,
                run_time=4,
            ),
        )

        data_point = [
            axes.x_axis.number_to_point(number_x.get_value())[0],
            axes.y_axis.number_to_point(number_y.get_value())[1],
            0,
        ]
        data = Dot(
            data_point,
            stroke_width=1,
            fill_opacity=1,
            color=TARGET_COLORS[int(evidence_point_df.target)],
            radius=0.075,
        )

        mini_digit = digit.copy().scale(0.2).next_to(data, UR, buff=SMALL_BUFF)

        vertical_line = axes.get_vertical_line(data_point, color=YELLOW)
        horizontal_line = axes.get_horizontal_line(data_point, color=YELLOW)
        self.play(
            AnimationGroup(
                AnimationGroup(
                    Create(vertical_line),
                    Create(horizontal_line),
                ),
                Create(data),
                FadeIn(mini_digit),
                lag_ratio=0.9,
            )
        )

        dots = []

        for sample_id in sample_ids:
            point_df = df[df["sample_id"] == sample_id].iloc[0]
            point_target = int(point_df.target)

            dots.append(
                Dot(
                    axes.c2p(*[float(point_df.dim_0), float(point_df.dim_1), 0]),
                    stroke_width=1,
                    fill_opacity=0.75,
                    color=TARGET_COLORS[point_target],
                    radius=0.05,
                ),
            )

        self.wait(0.1)
        self.next_slide()

        self.play(
            axes.animate.set_color(WHITE),
            Transform(
                data,
                Dot(
                    data_point,
                    stroke_width=1,
                    fill_opacity=1,
                    color=TARGET_COLORS[int(evidence_point_df.target)],
                    radius=0.05,
                ),
            ),
            AnimationGroup(
                AnimationGroup(
                    AnimationGroup(FadeOut(number_x), FadeOut(number_y)),
                    AnimationGroup(FadeOut(vertical_line), FadeOut(horizontal_line)),
                    FadeOut(mini_digit),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    *[Create(x) for x in dots],
                    lag_ratio=0.1,
                ),
                lag_ratio=0.5,
            ),
            run_time=2,
        )

        self.wait(0.1)
        self.next_slide(auto_next=True)

        self.play(
            AnimationGroup(
                FadeOut(toy_model),
                FadeOut(axes),
                AnimationGroup(
                    *[FadeOut(x) for x in dots],
                    FadeOut(data),
                ),
                lag_ratio=0.25,
            ),
            run_time=1.5,
        )
