from settings import * # importing variables, constants, etc. from settings.py
from pytmx.util_pygame import load_pygame
from os.path import join

from sprites import Sprite, Button
from groups import AllSprites


class Game:
    def __init__(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode((WIN_WID, WIN_HGT)) # setting resolution of window
        pygame.display.set_caption('epic game') # sets caption of game window
        self.clock = pygame.time.Clock()

        self.all_sprites = AllSprites()

        self.font = pygame.font.Font(None,30)

        self.import_assets()
        self.setup(self.tmx_maps['nz'])

        
        self.testbutton = Button('yo', 100, 100, (30,670), self.font)
        

    def import_assets(self):
        self.tmx_maps = {
            'nz': load_pygame(join('Unesco-game-2026', 'data','maps','newzealand.tmx'))
            }

        print(self.tmx_maps)

    def setup(self, tmx_map):
        # terrain
        for layer in ['Terrain', 'Terrain Top']:
            for x,y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        # objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            Sprite((obj.x, obj.y), obj.image, self.all_sprites)

        #entities
        for entity in tmx_map.get_layer_by_name('Entities'):
            pass #do stuff
        
    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            #event loop
            for event in pygame.event.get(): # check for pygame events
                if event.type == pygame.QUIT: # if player closes main window:
                    pygame.quit() # quit the game
                    exit()

            #game logic
            self.all_sprites.update(dt)
            self.display_surf.fill('black')
            self.all_sprites.draw()
            self.testbutton.draw(self.display_surf)
            pygame.display.update() # update display


if __name__ == '__main__': # initialise game (failsafe; checks if this file is called main)
    game = Game()
    game.run()  