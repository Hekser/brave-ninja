import arcade
import random
import os

import mountains

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

COIN_SCALE = 0.5
COIN_COUNT = 50

MOVEMENT_SPEED = 5

class MyGame(arcade.Window):

    mountains = mountains.Mountains(SCREEN_WIDTH)

    def __init__(self, width, height):
        super().__init__(width, height, "Brave Ninja")

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.all_sprites_list = None
        self.coin_list = None

        # Set up the player
        self.score = 0
        self.player = None

    def setup(self):
        self.all_sprites_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player = arcade.AnimatedWalkingSprite()

        character_scale = 0.75
        self.player.stand_right_textures = []
        self.player.stand_right_textures.append(arcade.load_texture("images/1.png", scale=character_scale))
        self.player.stand_left_textures = []
        self.player.stand_left_textures.append(arcade.load_texture("images/1.png", scale=character_scale, mirrored=True))

        self.player.walk_right_textures = []

        self.player.walk_right_textures.append(arcade.load_texture("images/1.png", scale=character_scale))
        self.player.walk_right_textures.append(arcade.load_texture("images/2.png", scale=character_scale))
        self.player.walk_right_textures.append(arcade.load_texture("images/3.png", scale=character_scale))
        self.player.walk_right_textures.append(arcade.load_texture("images/4.png", scale=character_scale))

        self.player.walk_left_textures = []

        self.player.walk_left_textures.append(arcade.load_texture("images/1.png", scale=character_scale, mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("images/2.png", scale=character_scale, mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("images/3.png", scale=character_scale, mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("images/4.png", scale=character_scale, mirrored=True))

        self.player.walk_up_textures = []

        self.player.walk_up_textures.append(arcade.load_texture("images/jump.png", scale=character_scale))

        self.player.texture_change_distance = 20

        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player.scale = 1.2

        self.all_sprites_list.append(self.player)

        self.back = []
        self.back = self.mountains.getMountains(self.back)

        # Set the background color
        arcade.set_background_color(arcade.color.DARK_CYAN)

        self.background = arcade.ShapeElementList()

        color1 = (150, 255, 100)
        color2 = (0, 187, 195)
        points = (0, 0), (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)
        colors = (color1, color1, color2, color2)
        rect = arcade.create_rectangles_filled_with_colors(points, colors)

        self.background.append(rect)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        self.background.draw()

        for mountain_range in self.back:
            mountain_range.draw()

        # Draw all the sprites.
        self.all_sprites_list.draw()

        # Put the text on the screen.
        output = "Score: {}".format(self.score)
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def update(self, delta_time):

        self.all_sprites_list.update()
        self.all_sprites_list.update_animation()

        # Generate a list of all sprites that collided with the player.
        hit_list = \
            arcade.check_for_collision_with_list(self.player,
                                                 self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in hit_list:
            coin.kill()
            self.score += 1

def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
