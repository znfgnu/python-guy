import zx
from player import Player


class Game(zx.Game):
    objects = [
        Player()
    ]


Game().run()
