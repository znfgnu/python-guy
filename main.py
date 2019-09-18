import zx
from player import Player


class Game(zx.Game):
    display_size = (320, 240)
    prescaler = 3
    fps_on = True

    palette = zx.palettes['awsm219']
    background_color = palette[3]

    objects = [
        Player(160, 120)
    ]


Game().run()
