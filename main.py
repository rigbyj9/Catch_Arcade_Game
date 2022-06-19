import arcade
import random

#Game Constants
SCREEN_HEIGHT_Y = 750
SCREEN_WIDTH_X = 1000
SCREEN_TITLE = "Catch"
CHARACTER_SCALE = 1
BLOCK_SCALE = 1
MOVE_SPEED = 20
BLOCK_COUNT = 50

class Block(arcade.Sprite):

    #This is the block's fall speed
    def update(self):
        self.center_y -=15

class Player(arcade.Sprite):

    #This creates borders so player stays within game window
    def update(self):
        if self.left < 0:
           self.left = 0
        if self.right > SCREEN_WIDTH_X:
           self.right = SCREEN_WIDTH_X

class Game(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH_X, SCREEN_HEIGHT_Y, SCREEN_TITLE)

        #Create lists
        self.block_list = None
        self.player_list = None
        self.score = 0

    def create_block(self, delta_time):

        #Create blocks, then randomize where they fall
        block = Block("Sprites/tile.png", BLOCK_SCALE)
        block.center_x = random.randrange(10,SCREEN_WIDTH_X - 10)
        block.center_y = SCREEN_HEIGHT_Y

        self.block_list.append(block)

        #This will delete the sprite once offscreen to maintain memory
        if  block.center_y < 0:
            block.remove_from_sprite_lists()
            
    def setup(self):
        #Load background
        self.background = arcade.load_texture("background.jpg")

        #Create empty lists for sprites
        self.player_list = arcade.SpriteList()
        self.block_list = arcade.SpriteList()

        #import character sprite and set sizing and location
        self.player = Player("Sprites/player_default.png", CHARACTER_SCALE)

        #Set default position 
        self.player.center_x = SCREEN_WIDTH_X //2
        self.player.center_y = 50
        self.player_list.append(self.player)

        #import falling objects
        arcade.schedule(self.create_block, 1)


    def on_draw(self):

        #Render creates the game window
        arcade.start_render()

        #Draw the background
        arcade.draw_texture_rectangle(SCREEN_WIDTH_X // 2, SCREEN_HEIGHT_Y // 2, SCREEN_WIDTH_X, SCREEN_HEIGHT_Y, self.background)

        #Draw the sprites
        self.player_list.draw()
        self.block_list.draw()

        #Display score
        score_output = f"Score: {self.score}"
        arcade.draw_text(score_output, 20, 700, 
                        arcade.color.WHITE_SMOKE,
                        20, 'right')

    def update(self, delta_time):

        #Calls all sprites in respective lists
        self.player_list.update()
        self.block_list.update()

        self.player.center_x += self.player.change_x
        self.player.center_y += self.player.change_y

        #Collision checker
        block_hits_player = arcade.check_for_collision_with_list(self.player,self.block_list)

        for block in block_hits_player:
            block.remove_from_sprite_lists()
            self.score += random.randint(5,9)
            

    def on_key_press(self, key, modifiers):

        #Keyboard inputs
        if key == arcade.key.UP:
            self.player.change_y = MOVE_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -MOVE_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVE_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVE_SPEED
        elif key == arcade.key.Q:
             arcade.close_window()
        

    def on_key_release(self, key, modifiers):

        #Program recognizes when key is released
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or arcade.key.RIGHT:
            self.player.change_x = 0
        

def main():
    game = Game()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
