import itertools
from typing import Dict, List

import torch
from datasets import load_from_disk
from manim import *
from manim.mobject.geometry.line import Arrow
from manim.mobject.geometry.polygram import Polygon, Rectangle
from manim_slides import Slide

from nn_core.common import PROJECT_ROOT

from latentcommunication_anims.utils import section_slide

MNIST_DATASET = load_from_disk(PROJECT_ROOT / "data" / "stitching" / "mnist")
FMNIST_DATASET = load_from_disk(PROJECT_ROOT / "data" / "stitching" / "fashion_mnist")

MNIST_DATASET.set_format(type="torch")
FMNIST_DATASET.set_format(type="torch")


START_MODULE_OPACITY: float = 0.5

OBJ_OPACITY = 0.5


def build_stitching_ae(model_id: str, color: str, label_pos):
    scale: float = 0.6
    encoder = (
        Polygon(2 * UP + LEFT, RIGHT + UP, RIGHT + DOWN, 2 * DOWN + LEFT, fill_opacity=0.5, color=color)
        # .set_opacity(START_MODULE_OPACITY)
        .scale(scale)
    )

    decoder = (
        Polygon(RIGHT + 2 * UP, RIGHT + 2 * DOWN, DOWN + LEFT, UP + LEFT, fill_opacity=0.5, color=color)
        # .set_opacity(START_MODULE_OPACITY)
        .scale(scale)
    )

    latent = Rectangle(height=2 * 0.6, width=0.5, fill_opacity=0.5, color=TEAL)

    encoded_arrow = Arrow(
        LEFT / 2,
        RIGHT / 2,
    )
    decoding_arrow = Arrow(
        LEFT / 2,
        RIGHT / 2,
    )

    encoded_arrow.next_to(latent, LEFT)
    decoding_arrow.next_to(latent, RIGHT)

    encoder.next_to(encoded_arrow, LEFT)
    decoder.next_to(decoding_arrow, RIGHT)

    encoder_label = Tex(f"Encoder {model_id}", z_index=2).next_to(encoder, label_pos)
    # .scale_to_fit_width(encoder.height * 2 / 3)
    # encoder_label.move_to(encoder.get_center()).rotate(PI / 2)

    decoder_label = Tex(f"Decoder {model_id}", z_index=2).next_to(decoder, label_pos)
    # .scale_to_fit_width(decoder.height * 2 / 3)
    # decoder_label.move_to(decoder.get_center()).rotate(PI / 2)

    return VDict(
        dict(
            encoder=encoder,
            decoder=decoder,
            encoder_label=encoder_label,
            encoded_arrow=encoded_arrow,
            decoding_arrow=decoding_arrow,
            decoder_label=decoder_label,
        )
    )


def build_stitched_ae(model_id: str, encoder_color: str, decoder_color: str, rescale_length: float = 1):
    scale: float = 1.2

    encoder = (
        Polygon(2 * UP + LEFT, RIGHT + UP, RIGHT + DOWN, 2 * DOWN + LEFT, fill_opacity=0.5, color=encoder_color)
        .set_opacity(START_MODULE_OPACITY)
        .scale(scale)
    )

    decoder = (
        Polygon(RIGHT + 2 * UP, RIGHT + 2 * DOWN, DOWN + LEFT, UP + LEFT, fill_opacity=0.5, color=decoder_color)
        .set_opacity(START_MODULE_OPACITY)
        .scale(scale)
    )

    if model_id == "Identity":
        encoder = (
            Rectangle(width=2, height=4, fill_opacity=0.5, color=encoder_color)
            .set_opacity(START_MODULE_OPACITY)
            .scale(scale)
        )

        decoder = (
            Rectangle(width=2, height=4, fill_opacity=0.5, color=encoder_color)
            .set_opacity(START_MODULE_OPACITY)
            .scale(scale)
        )

    encoder.next_to(decoder, LEFT, buff=0)
    decoder.next_to(encoder, RIGHT, buff=0)

    ae = Group(encoder, decoder)

    label = Tex(model_id).scale_to_fit_height(ae.height * (2 / 5))  # .rotate(PI / 2)
    label.next_to(ae.get_top(), UP, buff=LARGE_BUFF)

    return VDict(dict(encoder=encoder, decoder=decoder, label=label)).rescale_to_fit(length=rescale_length, dim=1)


def build_identity(model_id: str, arrow_color: str, rescale_length: float = 1):
    scale: float = 1.2

    identity_arrow = Arrow(LEFT / 2, RIGHT / 2, color=arrow_color)

    label = Tex(model_id).scale_to_fit_height(identity_arrow.height * (2 / 5))  # .rotate(PI / 2)
    label.next_to(identity_arrow.get_top(), UP, buff=LARGE_BUFF)

    return identity_arrow.rescale_to_fit(length=rescale_length, dim=1)


def fadein_and_move(mob: VMobject, alpha: float, t=0.5):
    mob.restore()
    if alpha <= t:
        opacity = interpolate(0, OBJ_OPACITY, alpha * 2)
        # fill_opacity = interpolate(0, OBJ_OPACITY, alpha * 2)
        mob.set_opacity(opacity)
        # mob.set_style(fill_opacity=fill_opacity)

    else:
        shift_x = interpolate(mob.get_center()[0], mob.target.get_center()[0], (alpha - 0.5) * 2)
        shift_y = interpolate(mob.get_center()[1], mob.target.get_center()[1], (alpha - 0.5) * 2)

        mob.move_to([shift_x, shift_y, 0])


def autoencode_anim(encoder, decoder, image_in, image_out, encoded_arrow: VMobject, decoding_arrow: VMobject):
    # Encoding
    encoding_arrow = Arrow(
        LEFT / 2,
        RIGHT / 2,
    )
    decoded_arrow = Arrow(
        LEFT / 2,
        RIGHT / 2,
    )
    image_in.rescale_to_fit(length=encoder.height, dim=1)
    image_out.rescale_to_fit(length=decoder.height, dim=1)

    encoding_arrow.next_to(encoder.get_left(), LEFT)
    decoded_arrow.next_to(decoder.get_right(), RIGHT)
    image_in.next_to(encoding_arrow.get_left(), LEFT)
    image_out.next_to(decoded_arrow.get_right(), RIGHT)

    latent = Rectangle(height=2 * 0.6, width=0.5, fill_opacity=0.5, color=TEAL)
    latent.next_to(encoded_arrow, RIGHT)
    latent.save_state()

    latent.generate_target()
    latent.target.next_to(decoding_arrow.get_left(), LEFT)

    start_anim = AnimationGroup(
        *[
            FadeIn(image_in, shift=RIGHT),
            GrowArrow(encoding_arrow, shift=RIGHT),
            Flash(encoder, flash_radius=encoder.height / 2, color=encoder.get_color()),
            GrowArrow(encoded_arrow, shift=RIGHT),
            # FadeIn(latent),
            # AnimationGroup(
            #     latent.animate.set_opacity(1),
            # latent.animate.next_to(decoding_arrow, LEFT),
            # ),
            UpdateFromAlphaFunc(mobject=latent, update_function=fadein_and_move),
            GrowArrow(decoding_arrow, shift=RIGHT),
            Flash(decoder, flash_radius=decoder.height / 2, color=decoder.get_color()),
            GrowArrow(decoded_arrow, shift=RIGHT),
            FadeIn(image_out, shift=RIGHT),
        ],
        # rate_func=rate_functions.smooth,
        lag_ratio=0.5,
        run_time=1.5,
    )

    end_anim = AnimationGroup(
        *[
            FadeOut(image_out, shift=LEFT),
            FadeOut(decoded_arrow),
            FadeOut(decoding_arrow),
            FadeOut(latent),
            FadeOut(encoded_arrow),
            FadeOut(encoding_arrow),
            FadeOut(image_in, shift=UP),
        ],
        rate_func=rate_functions.smooth,
        lag_ratio=0.75,
        run_time=0.75,
    )

    return start_anim, end_anim


def autoencode_anim_big_stiching(
    encoder, decoder, image_in, image_out, encoded_arrow: VMobject, decoding_arrow: VMobject
):
    # Encoding
    encoding_arrow = Arrow(
        LEFT / 2,
        RIGHT / 2,
    )
    decoded_arrow = Arrow(
        LEFT / 2,
        RIGHT / 2,
    )
    image_in.rescale_to_fit(length=encoder.height, dim=1)
    image_out.rescale_to_fit(length=decoder.height, dim=1)

    encoding_arrow.next_to(encoder.get_left(), LEFT)
    decoded_arrow.next_to(decoder.get_right(), RIGHT)
    image_in.next_to(encoding_arrow.get_left(), LEFT)
    image_out.next_to(decoded_arrow.get_right(), RIGHT)

    latent = Rectangle(height=2 * 0.6, width=0.5, fill_opacity=0.5, color=TEAL)
    latent.next_to(encoded_arrow, RIGHT)
    latent.save_state()

    latent.generate_target()
    latent.target.next_to(decoding_arrow.get_left(), LEFT)

    first_half_start = [
        FadeIn(image_in, shift=RIGHT),
        GrowArrow(encoding_arrow, shift=RIGHT),
        Flash(encoder, flash_radius=encoder.height / 2, color=encoder.get_color()),
        GrowArrow(encoded_arrow, shift=RIGHT),
        FadeIn(latent),
    ]
    move_latent_start = [latent.animate.next_to(decoding_arrow.get_left(), LEFT)]
    second_half_start = [
        GrowArrow(decoding_arrow, shift=RIGHT),
        Flash(decoder, flash_radius=decoder.height / 2, color=decoder.get_color()),
        GrowArrow(decoded_arrow, shift=RIGHT),
        FadeIn(image_out, shift=RIGHT),
    ]

    end_anim = AnimationGroup(
        *[
            FadeOut(image_out, shift=LEFT),
            FadeOut(decoded_arrow),
            FadeOut(decoding_arrow),
            FadeOut(latent),
            FadeOut(encoded_arrow),
            FadeOut(encoding_arrow),
            FadeOut(image_in, shift=UP),
        ],
        rate_func=rate_functions.smooth,
        lag_ratio=0.75,
        run_time=1.5,
    )

    return first_half_start, move_latent_start, second_half_start, end_anim


def autoencode_anim2(ae: Mobject, image_in: Mobject, image_out: Mobject, image_list: List):
    # ae = ae.copy()
    image_in = image_in.copy()
    image_out = image_out.copy()

    encoder: Mobject = ae["encoder"]
    decoder: Mobject = ae["decoder"]

    # Encoding
    encoding_arrow = Arrow(
        LEFT / 2,
        RIGHT / 2,
    )

    decoded_arrow = Arrow(
        LEFT / 2,
        RIGHT / 2,
    )
    image_in.rescale_to_fit(length=ae.height * 3 / 4, dim=1)
    image_out.rescale_to_fit(length=ae.height * 3 / 4, dim=1)

    encoding_arrow.next_to(encoder.get_left(), LEFT)
    decoded_arrow.next_to(decoder.get_right(), RIGHT)
    image_in.next_to(encoding_arrow.get_left(), LEFT)
    image_out.next_to(decoded_arrow.get_right(), RIGHT)

    encoder_x, encoder_y, _ = encoder.get_center()
    decoder_x, decoder_y, _ = encoder.get_center()

    image_out.save_state()

    image_out.generate_target()
    image_out.target.next_to(image_list[0], buff=SMALL_BUFF, direction=LEFT)

    start_anim = AnimationGroup(
        *[
            FadeIn(image_in, shift=RIGHT),
            FadeIn(encoding_arrow, shift=RIGHT),
            # Flash(ae, flash_radius=ae.height, color=ae.get_color()),
            FadeIn(decoded_arrow, shift=RIGHT),
            UpdateFromAlphaFunc(
                mobject=image_out,
                update_function=fadein_and_move,
                run_time=4,
            ),
        ],
        rate_func=rate_functions.smooth,
        lag_ratio=0.2,
    )
    image_list.insert(0, image_out)

    end_anim = AnimationGroup(
        *[
            FadeOut(decoded_arrow),
            FadeOut(encoding_arrow),
            FadeOut(image_in, shift=LEFT),
        ],
        rate_func=rate_functions.smooth,
        lag_ratio=0.2,
    )

    return start_anim, end_anim


class RelRepStitching(Slide):
    def construct(self):
        section_slide(self, "Zero-shot Stitching")

        encoder_color: str = GREEN_D
        decoder_color: str = PURPLE_D
        ae1 = build_stitching_ae(model_id="1", color=encoder_color, label_pos=UP)
        ae2 = build_stitching_ae(model_id="2", color=decoder_color, label_pos=DOWN)

        VGroup(ae1, ae2).arrange(buff=1, direction=DOWN)
        self.play(
            *{Create(obj) for obj_name, obj in ae1.submob_dict.items() if "arrow" not in obj_name},
            *{Create(obj) for obj_name, obj in ae2.submob_dict.items() if "arrow" not in obj_name},
        )

        # Standard AE mechanism, two different models
        image_indices1 = [0, 1, 2][:2]
        image_indices2 = [3, 4, 5][:2]
        for i, (sample1, sample2) in enumerate(
            zip(MNIST_DATASET.select(image_indices1), MNIST_DATASET.select(image_indices2))
        ):
            image1_in = ImageMobject(((sample1["image"]) * 255).to(torch.uint8)[0])
            image1_out = ImageMobject(((sample1["ae_0_0"]) * 255).to(torch.uint8)[0])

            image2_in = ImageMobject(((sample2["image"]) * 255).to(torch.uint8)[0])
            image2_out = ImageMobject(((sample2["ae_1_1"]) * 255).to(torch.uint8)[0])

            image1_start_anim, image1_end_anim = autoencode_anim(
                encoder=ae1["encoder"],
                decoder=ae1["decoder"],
                encoded_arrow=ae1["encoded_arrow"],
                decoding_arrow=ae1["decoding_arrow"],
                image_in=image1_in,
                image_out=image1_out,
            )
            image2_start_anim, image2_end_anim = autoencode_anim(
                encoder=ae2["encoder"],
                decoder=ae2["decoder"],
                encoded_arrow=ae2["encoded_arrow"],
                decoding_arrow=ae2["decoding_arrow"],
                image_in=image2_in,
                image_out=image2_out,
            )
            self.play(
                Succession(
                    AnimationGroup(image1_start_anim, image2_start_anim),
                    AnimationGroup(image1_end_anim, image2_end_anim),
                ),
            )

        self.wait(0.1)
        self.next_slide()

        # Prepare for stitching
        self.play(
            ae1["decoder"].animate.set_opacity(0.1),
            ae2["encoder"].animate.set_opacity(0.1),
        )

        # Stitching animation
        stitching_indices = [8]
        for sample in MNIST_DATASET.select(stitching_indices):
            image_in = ImageMobject(((sample["image"]) * 255).to(torch.uint8)[0])
            image_out = Tex("?").scale_to_fit_height(image_in.height)

            first_half_start, move_latent_start, second_half_start, end_anim = autoencode_anim_big_stiching(
                encoder=ae1["encoder"],
                decoder=ae2["decoder"],
                encoded_arrow=ae1["encoded_arrow"],
                decoding_arrow=ae2["decoding_arrow"],
                image_in=image_in,
                image_out=image_out,
            )

        self.wait(0.1)
        self.next_slide()
        self.play(
            AnimationGroup(
                *first_half_start,
                lag_ratio=0.5,
                run_time=1,
            )
        )

        self.wait(0.1)
        self.next_slide()
        self.play(*move_latent_start)

        self.wait(0.1)
        self.next_slide()
        self.play(
            AnimationGroup(
                *second_half_start,
                lag_ratio=0.5,
                run_time=1,
            )
        )

        self.wait()
        self.next_slide()

        self.play(
            end_anim,
            *(Uncreate(ae1[x]) for x in ("encoder", "decoder", "encoder_label", "decoder_label")),
            *(Uncreate(ae2[x]) for x in ("encoder", "decoder", "encoder_label", "decoder_label")),
        )

        aes: VDict = VDict(
            dict(
                identity=build_stitched_ae(
                    model_id="Identity", encoder_color=YELLOW_D, decoder_color=YELLOW_D, rescale_length=1.1
                ),
                ae=build_stitched_ae(
                    model_id="AE", encoder_color=encoder_color, decoder_color=decoder_color, rescale_length=1.1
                ),
                vae_nocal=build_stitched_ae(
                    model_id="Variational AE",
                    encoder_color=encoder_color,
                    decoder_color=decoder_color,
                    rescale_length=1.1,
                ),
                rel_ae=build_stitched_ae(
                    model_id="Relative AE", encoder_color=encoder_color, decoder_color=decoder_color, rescale_length=1.1
                ),
            )
        )
        self.play(
            Create(
                aes.arrange(buff=MED_LARGE_BUFF, direction=DOWN)
                .to_edge(LEFT, buff=LARGE_BUFF * 4 / 3)
                .to_edge(DOWN, buff=MED_LARGE_BUFF)
            )
        )
        ae2images: Dict[str, List] = {
            ae_type: [Dot().move_to(ae["decoder"].get_center()).to_edge(RIGHT, buff=SMALL_BUFF / 2)]
            for ae_type, ae in aes.submob_dict.items()
        }

        mnist_images = [17, 18, 19, 20, 21]
        fmnist_images = [17, 18, 19, 20, 21]

        sample_end_anim = []
        for i, sample in enumerate(
            itertools.chain(MNIST_DATASET.select(mnist_images), FMNIST_DATASET.select(fmnist_images))
        ):
            sample_start_anim = []
            for ae_type, ae in aes.submob_dict.items():
                image_in = ImageMobject(((sample["image"]) * 255).to(torch.uint8)[0])
                if ae_type == "identity":
                    image_out = image_in.copy()
                else:
                    image_out = ImageMobject(((sample[f"{ae_type}_0_1"]) * 255).to(torch.uint8)[0])
                start_anim, end_anim = autoencode_anim2(
                    ae=ae, image_in=image_in, image_out=image_out, image_list=ae2images[ae_type]
                )
                sample_start_anim.append(start_anim)
                sample_end_anim.append(end_anim)
            self.play(*sample_start_anim, run_time=0.65)

        mnist_identity = Group(*ae2images["identity"][len(fmnist_images) : -1])
        fmnist_identity = Group(*ae2images["identity"][: len(fmnist_images)])

        mnist_brace = BraceLabel(mnist_identity, brace_direction=UP, text="MNIST").set_opacity(0.5)
        fmnist_brace = BraceLabel(fmnist_identity, brace_direction=UP, text="Fashion-MNIST").set_opacity(0.5)

        self.play(FadeIn(mnist_brace, shift=DOWN), FadeIn(fmnist_brace, shift=DOWN))

        self.next_slide(auto_next=True)
        self.play(
            *(FadeOut(x) for images in ae2images.values() for x in images[:-1]),
            *(Uncreate(x) for x in [mnist_brace, fmnist_brace, aes]),
            *sample_end_anim,
        )
        self.wait(0.1)


if __name__ == "__main__":
    Stitching().construct()
