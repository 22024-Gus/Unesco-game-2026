from settings import * # importing variables, constants, etc. from settings.py
from pytmx.util_pygame import load_pygame
from os.path import join

from sprites import Sprite
from entities import Player

class Game:
    def __init__(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode((WIN_WID, WIN_HGT)) # setting resolution of window
        pygame.display.set_caption('epic game') # sets caption of game window
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()

        self.import_assets()
        self.setup(self.tmx_maps['world'], 'house')

    def import_assets(self):
        self.tmx_maps = {'world': load_pygame(join('Unesco-game-2026', 'data','maps','world.tmx'))}
        print(self.tmx_maps)

    def setup(self, tmx_map, player_start_pos):
        for x,y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
           Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'player' and obj.properties['pos'] == 'player_start_pos':
                Player((obj.x, obj.y), self.all_sprites)

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
            self.all_sprites.draw(self.display_surf)
            print(self.clock.get_fps())
            pygame.display.update() # update display

if __name__ == '__main__': # initialise game (failsafe; checks if this file is called main)
    game = Game()
    game.run()  