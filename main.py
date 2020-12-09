"""
Platformer Game
"""  # Ég notaði template frá arcade.academy en ég breytti svo miklu að ég myndi bara segja að ég kóðaði flest allt.
import arcade  # Nokkur imports.
import time  # fyrir score og að breyta hraða.
import random
# ég hugsa að ég taki ekki út kommentin sem voru fyrir en geri heldur bara líka mín eigin
# Constants
# Breytur tengdar skjá, EKKI FÆRIBREYTUR og það má helst ekki vera að breyta þessum mikið.
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCREEN_TITLE = "The quest for the .bat"

# Constants used to scale our sprites from their original size
# Sprite scaling sem að ég held að ég hafi ekkert notað svo þetta eru eiginlega bara óþarfa breytur.
CHARACTER_SCALING = 0.3
TILE_SCALING = 0.5

# Movement speed of player, in pixels per frame
# Hérna eru breytur tengdar hreyfingu, ég hefði eiginlega bara átt að taka flesta hreyfingu út til þess að
# spara minni en ég ákvað að geima hana, það er samt varla hægt að breyta hraða sínum
PLAYER_MOVEMENT_SPEED = 5  # Hraði leikmanns.
GRAVITY = 1  # þingdarafl sem fer á characters
L_GRAVITY = 0.005  # Left gravity fyrir aðalpersónu, ég hefði alveg geta bara tekið þetta út.
PLAYER_JUMP_SPEED = 20  # Hversu hátt aðalmanneskja hoppar.

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250  # Left margin, hversu nálægt leikmaður má fara vinstri hlið áður en hún breytist.
RIGHT_VIEWPORT_MARGIN = 750  # Sama og left margin nema fyrir hægri hlið
BOTTOM_VIEWPORT_MARGIN = 50  # Sama nema fyrir botn
TOP_VIEWPORT_MARGIN = 100  # Sama nema fyrir topp


class MyGame(arcade.View):  # Þetta er klasinn mygame sem er child class af arcade.View klasanum,
    # ég geri þetta svona svo að ég geti skipt um það sem leikmaður sér léttilega
    """
    Main application class.
    """

    def __init__(self):  # Init fall sem fer í gang þegar tilvik er búið til.

        # Call the parent class and set up the window
        super().__init__()  # Súper init lætur þennan klasa fá alla eiginleika frá foreldra sínum.
        self.window.set_mouse_visible(False)  # Felur mús á meðan hún er yfir leik.
        # Important variables to keep track of time and whether the game is over
        # Ég held að engin af þessum breytum hafi verið hérna áður.
        self.START_TIME = 0  # Hvenær byrjaði leikurinn.
        self.CUR_TIME = 0  # Hvaða tími er núna.
        # self.GAME_END = False  # 3 breytur sem ég henti því ég fann betri leið til þess að sjá um þetta.
        # self.WIN = False
        # self.LOSE = False
        self.SCORE = 0  # Stig leikmanns

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        # Listar til þess að halda um alla hluti
        self.wall_list = None  # Listi sem heldur utanum gólfið, ekki spurja afhverju hann heitir wall list.
        self.kill_list = None  # Listi sem heldur utanum gaddana á jörðinni sem drepa leikmann.
        self.player_list = None  # Listi fyrir leikmann.
        self.bullet_list = None  # Listi fyrir skotin sem leikmaður skýtur.
        self.eagle_list = None  # Listi fyrir óvini sem hægt er að skjóta.

        # Separate variable that holds the player spritesheet
        self.player = None  # Hérna verður útlit leikmanns geimt.

        # Our physics engine
        self.physics_engine = None  # Eðlisfræði vél, það sem lætur leikmann finna fyrir þingdarafli
        # og ekki fljúga í gegnum veggi.

        # Used to keep track of our scrolling
        self.view_bottom = 0  # Hvar í leiknum við erum að horfa
        self.view_left = 0

        # Load sounds
        # self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.jump_sound = None  # Úff ég náði aldrei að fá hljóð til þess að virka almennilega svo ég bara tók þetta aldrei út.
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)  # Litur heimsins.

    def setup(self):  # setup, þar sem allar breytur fara á stað/ núllstillast.
        """ Set up the game here. Call this function to restart the game. """

        # Used to keep track of our scrolling
        self.view_bottom = 0  # Hvar í leiknum við erum að horfa
        self.view_left = 0

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()  # Hvernig leikmaður lítur út.
        self.wall_list = arcade.SpriteList()  # Hvernig gólfið lítur út.
        self.kill_list = arcade.SpriteList()  # Hvernig gaddarnir líta út.
        self.eagle_list = arcade.SpriteList()  # Hvernig óvinir líta út.
        self.bullet_list = arcade.SpriteList()  # Hvernig skot líta út.
        #  Þetta heldur líka um staðsetningar og svoleiðis.

        # Nýstilli nokkrar breytur
        self.START_TIME = time.time()  # Stilli tíman á hvað hann er akkúrat núna (í sekúndum)
        self.SCORE = 0  # Set stig sem 0
        self.CUR_TIME = 0  # Núllstilli nútímabreytuna.

        # Set up the player, specifically placing it at these coordinates.
        self.player = arcade.AnimatedTimeSprite()  # ÞETTA ER DEPRICATED FUNCTION EN ÞAÐ VIRKAR OKEI, og það er fyrir kalla sem hreifast.
        self.player.textures = []  # Stilli textures sem er undirbreyta player í ekkert
        for y in range(2):  # Tæknilega ætti þetta að vera x en mér finnst animationið líta betur út svona
            for x in range(2):  # For lykkja
                self.player.textures.append(arcade.load_texture("img/Bat.png", x=(x*224), y=(y*224), height=224, width=224))  # Bæta texture í lista.
        self.player.center_x = 448//2  # Stilli byrjunastað leikmanns.
        self.player.center_y = 448//2
        self.player_list.append(self.player)  # Bæti leikmann í leikinn (:

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        # Bý til jörðina.
        for x in range(0, 50000, 64):  # stóóóór for lykkja sem býr til mikið af jörð, kannski smá of mikið.
            wall = arcade.Sprite("img/PlatformDes1.png", TILE_SCALING)  # Stilli mynd
            wall.center_x = x  # þetta er svo að jörðin sé ekki öll á sama stað
            wall.center_y = 32  # Þetta er svo jörðin sé öll á sömu hæð.
            self.wall_list.append(wall)  # Bæti jörðinni inn.

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites

        for x in range(1000, 50000, 700):  # For lykkja til þess að smíða alla gaddana
            wall = arcade.Sprite("img/SpikesV1-1.png.png", TILE_SCALING)  # Stilli mynd
            xpos = x+random.randint(1, 500)  # haha, random tala því ég er hryllilegur, en já þetta er svo að þeir birtist ekki alltaf á sama stað.
            wall.position = (xpos, 78)  # Set þá inn
            self.kill_list.append(wall)  # og set þá inn í leikinn

        for x in range(12500, 50000, 700):  # Þessi for lykkja er fyrir fúgl og hún er kewl
            bat = arcade.Sprite("img/hiclipart.com.png", 2)  # Bæta fugl inn og stækka hann x2
            bat.position = (x+random.randint(1,1000), 300)  # RANDOM JIBBÍ og líka þeir eru hærri en oddarnir
            self.eagle_list.append(bat)  # Hendi þeim inn í leikinn

        # Create the 'physics engine' AKA heilaga björgin svo leikmaður fari ekki í gegnum veggi og fljúgi
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list, GRAVITY)

    def on_draw(self):  # Þegar skjárinn á að vera teiknaðir
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()  # Stroka allt ít

        # Draw our sprites
        self.wall_list.draw()  # Teikna allt (:
        self.kill_list.draw()
        self.player_list.draw()
        self.eagle_list.draw()
        self.bullet_list.draw()

        arcade.draw_text(f"Score: {self.SCORE}", self.view_left+ 10, self.view_bottom, arcade.color.YELLOW, 14)  # og líka teikna score og nafn mitt.
        arcade.draw_text("Alexander Viðar Garðarsson", self.view_left, self.view_bottom + SCREEN_HEIGHT - 20, arcade.csscolor.WHITE_SMOKE, 14)
    def on_key_press(self, key, modifiers):  # Þegar það er ítt á takka.
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE: # Ef takkin er uppör, W eða " " þá HOPPA.
            if self.physics_engine.can_jump():  # Ef leikmaður getur hoppað
                self.player.change_y = PLAYER_JUMP_SPEED  # hoppa
                arcade.play_sound(self.jump_sound)  # Spila hljóð sem er ekki til (:
        elif key == arcade.key.LEFT or key == arcade.key.A:  # Ef a eða vinstri ör þá færa sig í hana átt, sem virkar ekki því ég er evil (:.
            self.player.change_x -= PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:  # Ef d eða hægri ör þá færa sig í hana átt, sem virkar ekki því ég er evil (:.
            self.player.change_x += PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.E or key == arcade.key.RSHIFT or key == arcade.key.LSHIFT:  # Ef E eða shift er ítt þá skjóta.
            bullet = arcade.Sprite("img/kula.png", 0.4)  # hleð inn mynd af skotinu.
            bullet.center_x = self.player.center_x  # Stilli myðjuna
            bullet.bottom = self.player.top  # Stilli toppin
            bullet.change_x = 20  # Stilli hraðann

        # Add the bullet to the appropriate lists
            self.bullet_list.append(bullet)  # Bæti því í skot.
    # Það sem er fyrir neðan var tekið út því mér líkaði ekki við það.
    ''' def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0'''

    def update(self, delta_time):  # Update aka 90% af logic í leiknum, úff
        """ Movement and game logic """
        # Update the animation.
        self.player_list.update_animation()  # Update'a hluti sem hreifast
        self.bullet_list.update()  # Dittó
        # Move the player with the physics engine
        self.physics_engine.update()  # EÐLISFRÆÐI BOOM
        death_list = arcade.check_for_collision_with_list(self.player, self.kill_list)  # Ef leikmaður snertir odd og á að deyja fer hann í þennan lista.
        death_list2 = arcade.check_for_collision_with_list(self.player, self.eagle_list)  # Ef leikmaður snertir fugl og á að deyja fer hann í þennan lista.
        if len(death_list) != 0 or len(death_list2) != 0:  # Ef einhvver af dauðalistunum er ekki tómur þá drepa leikmann.
            view = GameOver(self.SCORE)  # Hérna bý ég till view af öðrum glugga
            self.window.show_view(view)  # Hérna sýni ég hann glugga.
        for bullet in self.bullet_list: # Fyrir hvert einasta skot.
            hit = arcade.check_for_collision_with_list(bullet, self.eagle_list)  # Ef það snerti örn þá fer það í lista.
            if len(hit) > 0:  # Ef listinn er ekki tómur
                bullet.remove_from_sprite_lists()  # þá hverfur skotið
            for eagle in hit:  # fyrir hvern örn sem var hittur
                eagle.remove_from_sprite_lists()  # þá hverfur örninn
                self.SCORE += 15  # og 15 stig sem eru alls ekki tekin í burtu strax af öðrum hlut (:
            if bullet.right > self.view_left + SCREEN_WIDTH:  # Ef skotið fer af skjánum.
                bullet.remove_from_sprite_lists()  # Eyða skotinu

        self.CUR_TIME = time.time()  # Setur hvaða tími er núna
        self.SCORE = (self.CUR_TIME - self.START_TIME)**2  # Tekur tímann sem þú ert búinn að spila hendir honum í 2 veldi og lætur það sem stig.
        self.player.change_x = 10 + (L_GRAVITY * ((self.CUR_TIME - self.START_TIME)/10)**2)  # Þetta er humm, það sem hreifir kallin til hægri.
        if self.CUR_TIME - self.START_TIME > 60 and self.player.change_x > 2:  # Ef 60 sek eru liðnar.
            view = GameWin(self.SCORE)  # Búa til glugga af you win clasanum
            self.window.show_view(view)  # Opna hann glugga og loka þessum
        if self.CUR_TIME - self.START_TIME > 30 and self.player.change_x > 2:  # Ef 30 sek eru liðnar
            arcade.set_background_color(arcade.csscolor.DARK_BLUE)  # Breyta lit.




        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False  # hvort það eigi að breyta.

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN  # Hversu langt leikmaður má fara til  vinstri.
        if self.player.left < left_boundary:  # Ef leikmaður er kominn of langt
            self.view_left -= left_boundary - self.player.left  # Færa skjá það sem hann sér
            changed = True  # segir að það þarf að breyta skjá

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN  # Hversu langt leikmaður má fara til  hægri.
        if self.player.right > right_boundary:  # Ef leikmaður er kominn of langt
            self.view_left += self.player.right - right_boundary  # Færa skjá það sem hann sér
            changed = True  # segir að það þarf að breyta skjá

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN  # Hversu langt leikmaður má fara upp.
        if self.player.top > top_boundary:  # Ef leikmaður er kominn of langt
            self.view_bottom += self.player.top - top_boundary  # Færa skjá það sem hann sér
            changed = True  # segir að það þarf að breyta skjá

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN  # Hversu langt leikmaður má fara niður.
        if self.player.bottom < bottom_boundary:  # Ef leikmaður er kominn of langt
            self.view_bottom -= bottom_boundary - self.player.bottom  # Færa skjá það sem hann sér
            changed = True  # segir að það þarf að breyta skjá

        if changed:  # Ef það þarf að breyta skjá.
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)  # Kíkir hvar leikmaður er
            self.view_left = int(self.view_left)  # Dittó

            # Do the scrolling
            arcade.set_viewport(self.view_left,  # Færir skjá til leikmanns.
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


class InstructionView(arcade.View):  # Leiðbeiningar child af arcade.View klasanum, það þarf samt ekki init fyrir þennan.
    def on_show(self):  # Þegar þetta kemur upp á skjá
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)  # Breyta lit
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)  # Færa myndavél
    def on_draw(self):  # Þegar það þarf að teikna skjá
        """ Draw this view """
        arcade.start_render()  # Starta upp Teikningarélinni
        # Næstu línur eru bara að segja tölvunni að sína texta.
        arcade.draw_text("Leiðbeiningar", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Space til þess að halda áfram, q til þess að byrja strax.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75, arcade.color.WHITE, font_size=20, anchor_x="center")
    def on_key_press(self, key, modifiers):  # Ef það er ýtt á takka
        """Called whenever a key is pressed. """

        if key == arcade.key.SPACE:  # Ef það er ítt á " " þá
            game_view = FullInstructions()  # Opna lengri leiðbeiningar
            self.window.show_view(game_view)  # Dittó
        if key == arcade.key.Q:  # ef það er ítt á q
            game_view = MyGame()  # Búa til leik
            game_view.setup()  # Setja leik upp
            self.window.show_view(game_view)  # Sýna leik.


class FullInstructions(arcade.View):  # Leiðbeiningar child af arcade.View klasanum, það þarf samt ekki init fyrir þennan.
    def on_show(self):  # Þegar þetta kemur upp á skjá
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)  # Breyta lit
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)  # Færa myndavél

    def on_draw(self):  # Þegar það þarf að teikna skjá
        """ Draw this view """
        arcade.start_render()  # Starta upp Teikningarélinni
        # Næstu línur eru bara að segja tölvunni að sína texta.
        arcade.draw_text("Leiðbeiningar", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=50,
                         anchor_x="center")
        arcade.draw_text("Þú ert leðurblaka sem ferðast sjálfkrafa til hægri, þú átt að reyna að lifa af í 60 sekúndur en leikurinn verður alltaf ", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 75, arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("hraðari og hraðari, í rauninni þá þarftu bara space takkan til þess að hoppa", SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 100, arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text(
            "en wasd og örvatakkar geta verið notaðir fyrir nákvæmnri stjórn.",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 125, arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Svo er notað e eða einn af shift tökkunum til þess að skjóta út kúlu.", SCREEN_WIDTH // 2, SCREEN_HEIGHT //2 -150
                         , arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text(
            "Q til þess að byrja",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 185, arcade.color.WHITE, font_size=24, anchor_x="center")

    def on_key_press(self, key, modifiers):  # Ef það er ýtt á takka.
        """Called whenever a key is pressed. """
        if key == arcade.key.Q:  # ef það er ítt á q
            game_view = MyGame()  # Búa til leik
            game_view.setup()  # Setja leik upp
            self.window.show_view(game_view)  # Sýna leik.


class GameOver(arcade.View):  # Þetta er skjár sem kemur upp þegar þú tapar, child af arcade.View
    def __init__(self, score):  # Þegar tilvik er búið til þá tekur það score með sér.
        super().__init__()  # Super init fyrir inheritance
        self.score = score  # Er núna kominn með stig hingað.

    def on_show(self):  # Þegar þetta er sýnt
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)  # Breyta lit

    def on_draw(self):  # Þegar þetta er teiknað
        """ Draw this view """
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)  # Færa skjá til upphafsstað
        arcade.start_render()  # Byrja að teikna
        # Svo er bara texti og einn f strengur.
        arcade.draw_text("Þú tapaðir.", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.WHITE,
                         font_size=50, anchor_x="center")
        arcade.draw_text(f"Lokastig þín eru {self.score}, íttu á q til þess að byrja aftur.", SCREEN_WIDTH // 2,
                         SCREEN_HEIGHT // 2 - 75, arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):  # Þegar það er ítt á takka
        """Called whenever a key is pressed. """
        if key == arcade.key.Q:  # Þegar það er ýtt á q
            game_view = MyGame()  # Búa til tilvik af MyGame
            game_view.setup()  # Setja tilvik upp
            self.window.show_view(game_view)  # Sýna tilvik


class GameWin(arcade.View):  # Þetta er skjár sem kemur upp þegar þú vinnur, child af arcade.View
    def __init__(self, score):  # Þegar tilvik er búið til þá tekur það score með sér.
        super().__init__()  # Super init fyrir inheritance
        self.score = score  # Er núna kominn með stig hingað.

    def on_show(self):  # Þegar þetta er sýnt
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)  # Breyta lit

    def on_draw(self):  # Þegar þetta er teiknað
        """ Draw this view """
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)  # Færa skjá til upphafsstað
        arcade.start_render()  # Byrja að teikna
        # Svo er bara texti og einn f strengur.
        arcade.draw_text("Þú vannst, til Hamingju.", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text(f"Lokastig þín eru {self.score}, íttu á q til þess að byrja aftur.", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 75, arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):  # Þegar það er ítt á takka
        """Called whenever a key is pressed. """
        if key == arcade.key.Q:  # Þegar það er ýtt á q
            game_view = MyGame()  # Búa til tilvik af MyGame
            game_view.setup()  # Setja tilvik upp
            self.window.show_view(game_view)  # Sýna tilvik


def main():  # main klasinn
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)  # Býr til glugga
    start_view = InstructionView()  # Býr til tilvik af leiðbeiningum
    window.show_view(start_view)  # opnar það
    arcade.run()  # startast


if __name__ == "__main__":  # ef nafn er main
    main()  # starta main klasanum