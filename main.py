"""
Platformer Game
"""
import arcade
import time
import random

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCREEN_TITLE = "The quest for the .bat"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.3
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
L_GRAVITY = 0.005
PLAYER_JUMP_SPEED = 20

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100



class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__()
        self.window.set_mouse_visible(False)
        # Important variables to keep track of time and whether the game is over
        self.START_TIME = 0
        self.CUR_TIME = 0
        self.GAME_END = False
        self.WIN = False
        self.LOSE = False
        self.SCORE = 0

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.coin_list = None
        self.wall_list = None
        self.player_list = None

        # Separate variable that holds the player spritesheet
        self.player = None

        # Our physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Load sounds
        # self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        # self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.collect_coin_sound = None
        self.jump_sound = None
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()


        # Nýstilli nokkrar breytur
        self.START_TIME = time.time()
        self.SCORE = 0
        self.CUR_TIME = 0

        # Set up the player, specifically placing it at these coordinates.
        self.player = arcade.AnimatedTimeSprite()
        self.player.textures = []
        for y in range(2):
            for x in range(2):
                self.player.textures.append(arcade.load_texture("img/Bat.png", x=(x*224), y=(y*224), height=224, width=224))
        self.player.center_x = 448//2
        self.player.center_y = 448//2
        self.player_list.append(self.player)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 12500, 64):
            wall = arcade.Sprite("img/PlatformDes1.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites

        for x in range(1000, 12500, 300):
            # Add a crate on the ground
            wall = arcade.Sprite("img/SpikesV1-1.png.png", TILE_SCALING)
            wall.position = (random.randint(1,100)+x, 78)
            self.wall_list.append(wall)

        # Use a loop to place some coins for our character to pick up
        for x in range(128, 1250, 256):
            coin = arcade.Sprite("img/Bat.png", COIN_SCALING)
            coin.center_x = x
            coin.center_y = 96
            self.coin_list.append(coin)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list, GRAVITY)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        if self.GAME_END == False:
            arcade.draw_text(f"Score: {self.SCORE}", self.view_left + 100, self.view_bottom + 100, arcade.color.BLACK, 14)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W or arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x -= PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x += PLAYER_MOVEMENT_SPEED

    ''' def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0'''

    def update(self, delta_time):
        """ Movement and game logic """
        # Update the animation.
        self.player_list.update_animation()

        # Move the player with the physics engine
        self.physics_engine.update()


        self.CUR_TIME = time.time()
        self.SCORE = (self.CUR_TIME - self.START_TIME)**2
        self.player.change_x = 10 + (L_GRAVITY * ((self.CUR_TIME - self.START_TIME)/10)**2)
        print(self.START_TIME-self.CUR_TIME)
        if self.CUR_TIME - self.START_TIME > 60 and self.player.change_x > 2:
            self.GAME_END = True
            if self.LOSE == False:
                view = GameWin(self.SCORE)
                self.window.show_view(view)
            else:
                view = GameOver(self.SCORE)
                self.window.show_view(view)
        if self.CUR_TIME - self.START_TIME > 30 and self.player.change_x > 2:
            arcade.set_background_color(arcade.csscolor.DARK_BLUE)

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player,
                                                             self.coin_list)

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


class InstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Leiðbeiningar", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Space til þess að halda áfram, q til þess að byrja strax.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75, arcade.color.WHITE, font_size=20, anchor_x="center")
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.SPACE:
            game_view = FullInstructions()
            self.window.show_view(game_view)
        if key == arcade.key.Q:
            game_view = MyGame()
            game_view.setup()
            self.window.show_view(game_view)


class FullInstructions(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Leiðbeiningar", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=50,
                         anchor_x="center")
        arcade.draw_text("Þú ert leðurblaka sem ferðast sjálfkrafa til hægri, þú átt að reyna að lifa af í 60 sekúndur en leikurinn verður alltaf ", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 75, arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("hraðari og hraðari, í rauninni þá þarftu bara space takkan til þess að hoppa", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 100, arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text(
            "en wasd og örvatakkar geta verið notaðir fyrir nákvæmnri stjórn.",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 125, arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text(
            "Q til þess að byrja",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 160, arcade.color.WHITE, font_size=24, anchor_x="center")

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.Q:
            game_view = MyGame()
            game_view.setup()
            self.window.show_view(game_view)


class GameOver(arcade.View):
    def __init__(self, score):
        super().__init__()
        self.score = score

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Þú tapaðir.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE,
                         font_size=50, anchor_x="center")
        arcade.draw_text(f"Lokastig þín eru {self.score}, íttu á spacebar til þess að byrja aftur.", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 75, arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.SPACE:
            game_view = MyGame()
            game_view.setup()
            self.window.show_view(game_view)


class GameWin(arcade.View):
    def __init__(self, score):
        super().__init__()
        self.score = score


    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Þú vannst, til Hamingju.", SCREEN_WIDTH-200, SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text(f"Lokastig þín eru {self.score}, íttu á spacebar til þess að byrja aftur.", SCREEN_WIDTH-200, SCREEN_HEIGHT / 2-75, arcade.color.WHITE, font_size=20, anchor_x="center")
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.SPACE:
            game_view = MyGame()
            game_view.setup()
            self.window.show_view(game_view)


def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()