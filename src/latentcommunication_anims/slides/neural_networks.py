from manim import *
from manim_slides import Slide

from latentcommunication_anims.utils import section_slide


class NeuralNetworks(Slide):
    def construct(self):
        section_slide(self, "Neural Networks")

        encoder = Polygon(2 * UP + LEFT, RIGHT + UP, RIGHT + DOWN, 2 * DOWN + LEFT, fill_opacity=0.5)

        decoder = Polygon(RIGHT + 2 * UP, RIGHT + 2 * DOWN, DOWN + LEFT, UP + LEFT, fill_opacity=0.5)
        mini_decoder = Polygon(RIGHT + 0.5 * UP, RIGHT + 0.5 * DOWN, DOWN + LEFT, UP + LEFT, fill_opacity=0.5)
        mini_decoder.add_updater(lambda x: x.align_to(decoder, LEFT))

        encoder = encoder.next_to(ORIGIN, LEFT)
        decoder = decoder.next_to(ORIGIN, RIGHT)

        encoder_label = Tex("Encoder")
        encoder_label.next_to(encoder, UP)

        decoder_label = Tex("Decoder")
        decoder_label.next_to(decoder, UP)

        self.play(
            Create(encoder),
            Create(decoder),
            Create(encoder_label),
            Create(decoder_label),
        )

        self.wait(0.1)
        self.next_slide(auto_next=True)

        encoder_label.add_updater(lambda x: x.next_to(encoder, UP))
        decoder_label.add_updater(lambda x: x.next_to(decoder, UP))

        data_in = Tex("Data")
        arrowl = Arrow(
            LEFT / 2,
            RIGHT / 2,
        )
        arrowl.add_updater(lambda x: x.next_to(encoder, LEFT))
        data_in.add_updater(lambda x: x.next_to(arrowl, LEFT))

        self.play(Create(data_in), Create(arrowl), run_time=0.1)

        self.wait(0.1)
        self.next_slide(auto_next=True)

        embedding = Rectangle(height=2, width=0.5, fill_opacity=0.5)
        self.play(
            AnimationGroup(
                AnimationGroup(encoder.animate.next_to(embedding, LEFT), decoder.animate.next_to(embedding, RIGHT)),
                Create(embedding),
                lag_ratio=0.5,
            ),
        )

        self.wait(0.1)
        self.next_slide(auto_next=True)

        downtask = VGroup(Tex(r"Downstream\\ task")).arrange(direction=DOWN)
        arrowr = Arrow(LEFT / 2, RIGHT / 2)

        arrowr.add_updater(lambda x: x.next_to(decoder, RIGHT))
        downtask.add_updater(lambda x: x.next_to(arrowr, RIGHT))
        arrowr.update(0)
        downtask.update(0)
        self.play(
            AnimationGroup(Create(arrowr), Create(downtask), lag_ratio=0.25, run_time=0.75),
        )

        self.wait(0.1)
        self.next_slide()

        tasks = VGroup(Tex("Generation"), Tex("Classification"), Tex("Reconstruction"), Tex(f"\dots")).arrange(
            direction=DOWN,
            buff=MED_LARGE_BUFF,
            aligned_edge=LEFT,
        )
        brace = Brace(tasks, LEFT)

        brace.add_updater(lambda x: x.next_to(decoder, RIGHT))
        tasks.add_updater(lambda x: x.next_to(brace, RIGHT))
        brace.update(0)
        tasks.update(0)

        self.play(
            AnimationGroup(
                Transform(
                    decoder,
                    mini_decoder,
                    rate_func=rate_functions.there_and_back,
                ),
                run_time=2,
            ),
            AnimationGroup(
                Transform(arrowr, brace),
                Transform(downtask, tasks),
                run_time=1,
            ),
            lag_ratio=0.5,
        )

        self.wait(0.1)
        self.next_slide(auto_next=True)

        self.play(
            FadeOut(
                VGroup(encoder, decoder, embedding, encoder_label, decoder_label, data_in, arrowl, arrowr, downtask),
                shift=UP,
            )
        )
