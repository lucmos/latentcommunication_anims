from manim import *
from manim_slides import Slide

from nn_core.common import PROJECT_ROOT


class TitleAnimation(Slide):
    def construct(self):
        paper_title = Tex("Latent Communication", font_size=72)
        paper_title_sub = Tex("in", font_size=52)
        paper_title_sub2 = Tex("Artificial Neural Networks", font_size=52)
        title = VGroup(paper_title, paper_title_sub, paper_title_sub2).arrange(DOWN, buff=0.5)
        title.move_to(point_or_mobject=ORIGIN)

        top_authors = (
            VGroup(*[Tex(x, font_size=40) for x in (r"\textit{Luca Moschella}",)]).to_corner(DL).set_opacity(0.5)
        )

        # other_authors = VGroup(
        #     *[
        #         Tex(x, font_size=40)
        #         for x in ("Marco Fumero", "Antonio Norelli", "Francesco Locatello", "Emanuele Rodolà")
        #     ]
        # )

        # top_authors.arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.5).shift(DOWN * 0.25)
        # other_authors.arrange(RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 1.5).next_to(top_authors, DOWN, buff=0.5)

        sapienzalogo = ImageMobject(PROJECT_ROOT / "data" / "logos" / "sapienza_logo.png").scale(0.055)
        gladialogo = ImageMobject(PROJECT_ROOT / "data" / "logos" / "logo_gladia_white.png").rescale_to_fit(
            length=sapienzalogo.height, dim=1
        )
        ista_logo = ImageMobject(PROJECT_ROOT / "data" / "logos" / "ista_logo.png").rescale_to_fit(
            length=sapienzalogo.height, dim=1
        )
        iclr_logo = ImageMobject(PROJECT_ROOT / "data" / "logos" / "iclr_logo.png").rescale_to_fit(
            length=sapienzalogo.height, dim=1
        )
        neurips_logo: ImageMobject = ImageMobject(PROJECT_ROOT / "data" / "logos" / "neurips_logo.png").rescale_to_fit(
            length=sapienzalogo.height, dim=1
        )
        logos = Group(gladialogo, sapienzalogo, ista_logo, iclr_logo, neurips_logo).arrange(RIGHT, buff=0.4)
        logos = logos.to_corner(DR)

        logos = Group(logos, SurroundingRectangle(logos, buff=0.1, color=BLACK, stroke_width=1).set_opacity(0.5))
        # authors_group = Group(top_authors, other_authors, Group(sapienzalogo, iclr_logo, gladialogo))

        self.play(
            AnimationGroup(
                *(FadeIn(x, shift=UP, run_time=1.5) for x in (paper_title, paper_title_sub, paper_title_sub2)),
                run_time=2,
                lag_ratio=0.2,
            ),
            Write(top_authors, run_time=1),
            FadeIn(logos, run_time=1),
        )

        self.wait(0.1)
        self.next_slide(auto_next=True)

        self.play(
            AnimationGroup(
                *(
                    FadeOut(x, shift=DOWN, run_time=1.5)
                    for x in (Group(top_authors, logos), paper_title_sub2, paper_title_sub, paper_title)
                ),
                run_time=2,
                lag_ratio=0.2,
            ),
        )
