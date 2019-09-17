import zx
from my_guy import MyGuy


class Game(zx.Game):
    display_size = (320, 240)
    prescaler = 5
    fps_on = True

    objects = [
        MyGuy(160, 120)
    ]


Game().run()
