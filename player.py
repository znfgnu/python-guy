import zx


class Player(zx.Object):
    def __init__(self, x: int = 50, y: int = 50):
        super().__init__(x, y)

    def draw(self):
        palette = zx.Game.data.palette

        zx.Graphics.draw_striped_background(palette)
        zx.Graphics.draw_wobbly_stripes(palette, self.position)
        zx.Graphics.draw_diamond(palette, self.position)
