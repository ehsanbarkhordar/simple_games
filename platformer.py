import arcade
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"
CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5
COIN_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player_list = None
        self.coin_list = None
        self.wall_list = None
        self.player_sprite = None
        arcade.set_background_color(arcade.csscolor.ALICE_BLUE)
        self.physics_engine = None
        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/male_person/malePerson_climb1.png",
                                           CHARACTER_SCALING)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 120
        self.player_list.append(self.player_sprite)
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        coordinate_list = [[512, 96],
                           [256, 96],
                           [768, 96]]
        for coordinate in coordinate_list:
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.player_list.draw()
        self.coin_list.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        # if symbol == arcade.key.UP or symbol == arcade.key.W:
        #     self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        # elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
        #     self.player_sprite.change_y = - PLAYER_MOVEMENT_SPEED
        if symbol == arcade.key.UP or symbol == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.player_sprite.change_x = - PLAYER_MOVEMENT_SPEED

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.player_sprite.change_y = 0
        elif symbol == arcade.key.UP or symbol == arcade.key.W:
            self.player_sprite.change_y = 0
        elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.player_sprite.change_x = 0
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time: float):
        self.physics_engine.update()

        changed = False
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom += bottom_boundary - self.player_sprite.bottom
            changed = True
        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
