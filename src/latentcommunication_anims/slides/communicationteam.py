from manim import *
from manim_slides import Slide

from nn_core.common import PROJECT_ROOT


# Barbiero
# Cannistraci
# Ciccone
# Crisostomi
# Fumero
# Lio
# Locatello
# Maiorca
# Norelli
# Ricciardi
# Rodolà

TEAMS_PHOTO = PROJECT_ROOT / "assets" / "team"

ORDER = [
    "fumero",
    "locatello",
    "cannistraci",
    "rodola",
    "crisostomi",
    "norelli",
    "ricciardi",
    "maiorca",
]


class CommunicationTeam(Slide):
    def construct(self):
        team = Tex("Latent Communication Team").to_edge(UP)

        order = Tex("...in random order").set_opacity(0.8).scale(0.75)
        order.to_corner(DR)
        photos = list(TEAMS_PHOTO.iterdir())

        filterout = set(("ciccone", "lio", "barbiero"))
        photos = [x for x in photos if x.stem not in filterout]
        photos = sorted(photos, key=lambda x: ORDER.index(x.stem))
        photos = [ImageMobject(x) for x in photos]

        ref_photo = photos[0].scale(0.9)
        for photo in photos:
            photo.scale_to_fit_height(ref_photo.get_height())

        first_row_nelements = 4
        buff = 0.75
        first_row = Group(*photos[:first_row_nelements]).arrange(RIGHT, buff=buff)
        second_row = Group(*photos[first_row_nelements:]).arrange(RIGHT, buff=buff)
        second_row.next_to(first_row, DOWN, buff=buff)
        images = Group(first_row, second_row).move_to(ORIGIN).shift(DOWN * 0.25)

        self.play(
            AnimationGroup(
                FadeIn(team),
                AnimationGroup(
                    FadeIn(images),
                    Write(order),
                ),
                lag_ratio=0.5,
            )
        )

        self.wait(0.1)
        self.next_slide(auto_next=True)

        self.play(*(FadeOut(x) for x in (team, images, order)))
