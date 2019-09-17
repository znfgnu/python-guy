import pyglet

import zx


def addsome(t, x, y):
    return t[0] + x, t[1] + y


class MyGuy(zx.Object):
    def __init__(self, x: int = 50, y: int = 10):
        super().__init__(x, y)

    def draw(self):
        pyglet.graphics.draw(
            4, pyglet.gl.GL_POLYGON,
            (
                'v2f',
                addsome(self.position, 0, 10) + \
                addsome(self.position, 10, 0) + \
                addsome(self.position, 0, -10) + \
                addsome(self.position, -10, 0)
            ),
            (
                'c3B', (
                    0, 0, 0,
                    0, 100, 0,
                    0, 0, 0,
                    0, 100, 0
                )
            )
        )
