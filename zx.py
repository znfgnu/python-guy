from __future__ import annotations

import pyglet


class Game:
    # Set up a window
    fps_on = True
    display_size = (100, 100)
    game_window = None
    counter = None

    main_batch = pyglet.graphics.Batch()
    data = None
    prescaler = 1

    @staticmethod
    def on_draw():
        Game.data.game_window.clear()

        # The following two lines will change how textures are scaled.
        # pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
        # pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST)
        # Game.label.draw()  # blits the label to the screen

        if Game.data.counter is not None:
            Game.data.counter.draw()
        Game.data.main_batch.draw()

        for object_ in Game.data.objects:
            object_.draw()

    @classmethod
    def loop(cls, dt):
        if cls.game_window:
            cls.game_window.dispatch_event('on_draw')

    @classmethod
    def run(cls):
        print(cls.data.objects)
        pyglet.clock.schedule_interval(Game.loop, 1/30)
        pyglet.app.run()

    def __init__(self):
        # Can access `self`.
        self.__class__.mro()[1].data = self
        self.__class__.display_size = (
            self.__class__.display_size[0]*self.__class__.prescaler,
            self.__class__.display_size[1]*self.__class__.prescaler,
        )
        self.__class__.game_window = pyglet.window.Window(*self.__class__.display_size)
        # self.__class__.klasa = self.__class__
        print(f"Prescaler: {self.__class__.prescaler}")
        pyglet.gl.glScalef(self.__class__.prescaler, self.__class__.prescaler, self.__class__.prescaler)

        print(f"FPS on: {self.__class__.fps_on}")
        if self.__class__.fps_on:
            self.__class__.counter = pyglet.window.FPSDisplay(window=self.__class__.game_window)

        self.__class__.game_window.on_draw = self.__class__.on_draw


class Object:
    def __init__(self, x: int, y: int):
        self.position = (x, y)
