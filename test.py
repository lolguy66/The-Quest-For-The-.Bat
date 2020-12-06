import random
import arcade

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.1
SPRITE_SCALING_LASER = 0.2
COIN_COUNT = 5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_SPEED = 5

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Alexander Viðar Garðarsson")

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None
        self.diamond_list = None
        self.bullet_list = None
        self.OI_FECKING_CUNT = False

        # Set up the player info
        self.player = None
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)
        self.laser_sound = arcade.load_sound("laser.ogg")
        arcade.set_background_color(arcade.color.BEIGE)

    def setup(self):

        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.diamond_list = arcade.SpriteList()


        # Set up the player
        self.score = 0

        # Image from kenney.nl
        self.player = arcade.AnimatedTimeSprite()
        self.player.textures = []
        for y in range(2):
            for x in range(2):
                self.player.textures.append(arcade.load_texture("img/Bat.png", x=(x*224), y=(y*224), height=224, width=224))
        self.player.center_x = 448//2
        self.player.center_y = 448//2
        self.player_list.append(self.player)

        # Create the coins
        for i in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite("img/PlatformDes1.png", SPRITE_SCALING_COIN)
            diamond = arcade.Sprite("img/SpikesV1-1.png.png", 0.4)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(120, SCREEN_HEIGHT)

            diamond.center_x = random.randrange(SCREEN_WIDTH)
            diamond.center_y = random.randrange(120, SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)
            self.diamond_list.append(diamond)

        # Set the background color
        arcade.set_background_color(arcade.color.BEIGE)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.coin_list.draw()
        self.diamond_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

        # Render the text
        if self.OI_FECKING_CUNT == False:
            arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.BLACK, 14)
        else:
            arcade.draw_text(f"LOKASTIG {self.score} Leikurinn er búinn.", 200, 150, arcade.color.BLACK, 24)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """

        # Create a bullet
        if self.OI_FECKING_CUNT == False:
            bullet = arcade.Sprite("img/Bat.png", SPRITE_SCALING_LASER)
            arcade.play_sound(self.laser_sound)

        # The image points to the right, and we want it to point up. So
        # rotate it.

        # Position the bullet
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top
            bullet.change_y = BULLET_SPEED

        # Add the bullet to the appropriate lists
            self.bullet_list.append(bullet)

    def update(self, delta_time):
        """ Movement and game logic """
        if self.score == 30:
            self.OI_FECKING_CUNT = True
            arcade.set_background_color(arcade.color.BABY_BLUE)
        # Call update on all sprites
        self.coin_list.update()
        self.diamond_list.update()
        self.bullet_list.update()
        self.player_list.update_animation()

        # Loop through each bullet
        for bullet in self.bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.coin_list)
            hit_list_diamond = arcade.check_for_collision_with_list(bullet, self.diamond_list)
            # If it did, get rid of the bullet
            if len(hit_list) > 0 or len(hit_list_diamond) > 0:
                bullet.remove_from_sprite_lists()

            # For every coin we hit, add to the score and remove the coin
            for coin in hit_list:
                coin.remove_from_sprite_lists()
                self.score += 1

            for diamond in hit_list_diamond:
                diamond.remove_from_sprite_lists()
                self.score += 5

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()