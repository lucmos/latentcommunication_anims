from manim import *
from manim_slides import Slide

from nn_core.common import PROJECT_ROOT

FONT_SIZE = 38

from powermanim.components.powermanim import PowerManim


class Thanks(Slide):
    def construct(self):
        thankyou = Tex("Thank you!", font_size=84)

        # Sponsor
        erc = ImageMobject(PROJECT_ROOT / "data" / "assets" / "erc.jpg").scale(0.35).to_corner(UR)

        banner = ManimBanner().scale(0.125).to_edge(LEFT, buff=LARGE_BUFF * 1.15)

        manimslides = ImageMobject(PROJECT_ROOT / "data" / "assets" / "manimslides.png")
        manimslides.scale_to_fit_height(banner.get_height()).scale(1.5).align_to(banner, DOWN).align_to(
            banner.get_critical_point(RIGHT), LEFT
        )

        powermanim_banner = PowerManim(font_color=WHITE, logo_black=WHITE, gap=0.5).build_banner()
        powermanim_banner.scale_to_fit_height(banner.get_height() * 1.6)
        powermanim_banner.next_to(banner, DOWN).align_to(banner, LEFT)

        Group(banner, manimslides, powermanim_banner).to_corner(DL).shift(RIGHT * 0.5)

        # # Slides by...
        # cc = Tex(r"\emph{...slides by \textbf{Luca Moschella} \& \textbf{Valentino Maiorca}}", font_size=28).to_corner(
        #     DR
        # )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    DrawBorderThenFill(thankyou, run_time=0.75),
                    Circumscribe(
                        thankyou,
                        color=BLUE,
                        buff=MED_LARGE_BUFF,
                    ),
                    lag_ratio=0.5,
                ),
                # AnimationGroup(
                #     Create(poster),
                #     ShowPassingFlash(Underline(poster, color=YELLOW)),
                #     lag_ratio=0.5,
                # ),
                lag_ratio=0.5,
            )
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeIn(erc),
                    AnimationGroup(
                        banner.create(),
                        FadeIn(manimslides),
                        FadeIn(powermanim_banner),
                        lag_ratio=0.1,
                    ),
                ),
                # Create(cc),
                lag_ratio=0.5,
            ),
            run_time=2,
        )

        # Expand banner
        manimslides.add_updater(lambda m: m.align_to(banner.get_critical_point(RIGHT), LEFT))
        powermanim_banner.add_updater(lambda m: m.align_to(banner, LEFT))
        self.play(banner.expand(), run_time=1)
        self.wait(2)
