from __future__ import annotations

import random
from collections import namedtuple
from itertools import cycle
from typing import Tuple, List

import pyglet


Color = Tuple[int, int, int]
Palette = List[Color]
Position = namedtuple('Position', ['x', 'y'])


def addsome(t, x, y):
    return t[0] + x, t[1] + y


class BaseColorPalette:
    @classmethod
    def from_hex(cls, hex_string: str):
        if hex_string.startswith("#"):
            hex_string = hex_string[1:]
        return int(hex_string[:2], 16), int(hex_string[2:4], 16), int(hex_string[4:], 16)


palettes = {
    'default': [
        BaseColorPalette.from_hex("aa2447"),
        BaseColorPalette.from_hex("ff6f5e"),
        BaseColorPalette.from_hex("f5f0e3"),
        BaseColorPalette.from_hex("40bfc1"),
    ],
    'default2': [
        BaseColorPalette.from_hex("c0d154"),
        BaseColorPalette.from_hex("faf3e3"),
        BaseColorPalette.from_hex("de1b85"),
        BaseColorPalette.from_hex("6c1460"),
    ],
    'default3': [
        BaseColorPalette.from_hex("4b2637"),
        BaseColorPalette.from_hex("7d2941"),
        BaseColorPalette.from_hex("e9e3e3"),
        BaseColorPalette.from_hex("b3a2a2"),
    ],
    'gb': [
        BaseColorPalette.from_hex("0f380f"),
        BaseColorPalette.from_hex("306230"),
        BaseColorPalette.from_hex("8bac0f"),
        BaseColorPalette.from_hex("9bbc0f"),
    ],
    'icecream': [
        BaseColorPalette.from_hex("7c3f58"),
        BaseColorPalette.from_hex("eb6b6f"),
        BaseColorPalette.from_hex("f9a875"),
        BaseColorPalette.from_hex("fff6d3"),
    ],
    'kamikaze': [
        BaseColorPalette.from_hex("332c50"),
        BaseColorPalette.from_hex("46878f"),
        BaseColorPalette.from_hex("94e344"),
        BaseColorPalette.from_hex("e2f3e4"),
    ],
    'rustic': [
        BaseColorPalette.from_hex("2c2137"),
        BaseColorPalette.from_hex("764462"),
        BaseColorPalette.from_hex("edb4a1"),
        BaseColorPalette.from_hex("a96868"),
    ],
    'dirtyboy': [
        BaseColorPalette.from_hex("c4cfa1"),
        BaseColorPalette.from_hex("8b956d"),
        BaseColorPalette.from_hex("4d533c"),
        BaseColorPalette.from_hex("1f1f1f"),
    ],
    'awakening': [
        BaseColorPalette.from_hex("5a3921"),
        BaseColorPalette.from_hex("6b8c42"),
        BaseColorPalette.from_hex("7bc67b"),
        BaseColorPalette.from_hex("ffffb5"),
    ],
    'pokemon': [
        BaseColorPalette.from_hex("181010"),
        BaseColorPalette.from_hex("84739c"),
        BaseColorPalette.from_hex("f7b58c"),
        BaseColorPalette.from_hex("ffefff"),
    ],
    'grayscale': [
        BaseColorPalette.from_hex("000000"),
        BaseColorPalette.from_hex("676767"),
        BaseColorPalette.from_hex("b6b6b6"),
        BaseColorPalette.from_hex("ffffff"),
    ],
}


class Game:
    # Set up a window
    fps_on = True
    display_size = (100, 100)
    game_window = None
    counter = None

    palette = palettes['default']
    background_color = None

    main_batch = pyglet.graphics.Batch()
    data = None
    prescaler = 1

    key_state = {}

    @staticmethod
    def on_draw():
        Game.data.game_window.clear()

        # The following two lines will change how textures are scaled.
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
        pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST)
        # Game.label.draw()  # blits the label to the screen

        Game.data.main_batch.draw()

        for object_ in Game.data.objects:
            object_.draw()

        if Game.data.counter is not None:
            Game.data.counter.draw()

    @staticmethod
    def on_key_press(key, mod):
        Game.data.game_window.on_key_press_old(key, mod)

        map_ = {
            pyglet.window.key.UP: 'on_up_pressed',
            pyglet.window.key.DOWN: 'on_down_pressed',
            pyglet.window.key.LEFT: 'on_left_pressed',
            pyglet.window.key.RIGHT: 'on_right_pressed',
        }
        Game.data.key_state[key] = True

        for object_ in Game.data.objects:
            try:
                func = getattr(object_, map_[key])
            except KeyError:
                continue
            func()

    @staticmethod
    def on_key_release(key, mod):
        map_ = {
            pyglet.window.key.UP: 'on_up_released',
            pyglet.window.key.DOWN: 'on_down_released',
            pyglet.window.key.LEFT: 'on_left_released',
            pyglet.window.key.RIGHT: 'on_right_released',
        }
        Game.data.key_state[key] = False

        for object_ in Game.data.objects:
            getattr(object_, map_[key])()

    @classmethod
    def loop(cls, dt):
        if cls.game_window:
            cls.game_window.dispatch_event('on_draw')

    @classmethod
    def run(cls):
        print(cls.data.objects)
        pyglet.clock.schedule_interval(Game.loop, 1 / 30)
        pyglet.app.run()

    def __init__(self):
        # Can access `self`.
        self.__class__.mro()[1].data = self

        display_size = (
            self.__class__.display_size[0] * self.__class__.prescaler,
            self.__class__.display_size[1] * self.__class__.prescaler,
        )

        self.__class__.game_window = pyglet.window.Window(*display_size)
        self.__class__.game_window.on_draw = self.__class__.on_draw

        self.__class__.game_window.on_key_press_old = self.__class__.game_window.on_key_press
        self.__class__.game_window.on_key_press = self.__class__.on_key_press
        self.__class__.game_window.on_key_release = self.__class__.on_key_release

        if self.__class__.background_color is None:
            self.__class__.background_color = self.__class__.palette[3]

        pyglet.gl.glClearColor(
            self.background_color[0] / 256,
            self.background_color[1] / 256,
            self.background_color[2] / 256,
            1
        )

        # self.__class__.klasa = self.__class__
        print(f"Prescaler: {self.__class__.prescaler}")
        pyglet.gl.glScalef(self.__class__.prescaler, self.__class__.prescaler, self.__class__.prescaler)

        print(f"FPS on: {self.__class__.fps_on}")
        if self.__class__.fps_on:
            self.__class__.counter = pyglet.window.FPSDisplay(window=self.__class__.game_window)
            self.__class__.counter.color = self.__class__.data.palette[2]


class Object:
    relative_object = None

    def __init__(self, x: int, y: int, speed: int = 5):
        self.position = (x, y)
        self.speed = speed

    def __get_absolute_position(self):
        if self.relative_object is None:
            return self.position
        return (self.position[0] + self.relative_object.position[0],
                self.position[1] + self.relative_object.position[1])
    absolute_position = property(__get_absolute_position)

    def on_up_pressed(self):
        self.position = self.position[0], self.position[1]+self.speed

    def on_down_pressed(self):
        self.position = self.position[0], self.position[1]-self.speed

    def on_left_pressed(self):
        self.position = self.position[0]-self.speed, self.position[1]

    def on_right_pressed(self):
        self.position = self.position[0]+self.speed, self.position[1]

    # on_up_released = on_down_pressed
    # on_down_released = on_up_pressed


class Graphics:
    # TODO: @relative_drawing
    # pyglet.gl.glPushMatrix()
    # pyglet.gl.glTranslatef(self.position[0], self.position[1], 0)
    # ...
    # pyglet.gl.glPopMatrix()

    # @staticmethod
    # def relative_drawing(f):
    #     def new_f(self, *args, **kwargs):
    #         Graphics._translate_push(f.__self__.position)
    #         print("hi,")
    #         f(self, *args, **kwargs)
    #         Graphics._translate_pop()
    #     return new_f

    @classmethod
    def _translate_push(cls, position: Position):
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(position[0], position[1], 0)

    @classmethod
    def _translate_pop(cls):
        pyglet.gl.glPopMatrix()

    @classmethod
    def draw_diamond(cls, palette: Palette, position: Position = None):
        if position:
            cls._translate_push(position)

        pyglet.graphics.draw(
            4, pyglet.gl.GL_POLYGON,
            (
                'v2f',
                (0, 10) +
                (10, 0) +
                (0, -10) +
                (-10, 0)
            ),
            (
                'c3B',
                palette[0] +
                palette[1] +
                palette[2] +
                palette[3]
            )
        )

        if position:
            cls._translate_pop()

    @classmethod
    def draw_striped_background(cls, palette: Palette):
        for i, color in zip(range(100), cycle(palette)):
            width = 10
            offset = i * width - Game.data.display_size[0] - Game.data.display_size[1]# - 300# + random.randint(-2, 1)
            pyglet.graphics.draw(
                4, pyglet.gl.GL_POLYGON,
                (
                    'v2f',
                    (offset+1000, +1000+width) +
                    (offset+1000+width, +1000) +
                    (offset-1000, -1000-width) +
                    (offset-1000-width, -1000)
                ),
                (
                    'c3B',
                    color * 4
                )
            )

    @classmethod
    def draw_wobbly_stripes(cls, palette: Palette, position: Position = None):
        if position:
            cls._translate_push(position)

        for i, color in enumerate(palette):
            width = Game.data.display_size[0] / len(palette) / 2
            x = -width * len(palette) / 2 + i * width + random.randint(-1, 1)
            pyglet.graphics.draw(
                4, pyglet.gl.GL_POLYGON,
                (
                    'v2f',
                    (x, -100) +
                    (x, +100) +
                    (x+40, +100) +
                    (x+40, -100)
                ),
                (
                    'c3B',
                    color * 4
                )
            )

        if position:
            cls._translate_pop()
