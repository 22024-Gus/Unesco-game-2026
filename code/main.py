from settings import * #importing variables, constants, etc. from settings.py
from pytmx.util_pygame import load_pygame #
from os.path import join

from sprites import Sprite, Button, Tower
from groups import AllSprites

class Game:
    def __init__(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode((WIN_WID, WIN_HGT)) #setting resolution of window
        pygame.display.set_caption('epic game') #sets caption of game window
        self.clock = pygame.time.Clock() #start game clock

        self.all_sprites = AllSprites() #sprite group for updating (see groups.py)

        self.font = pygame.font.Font(None,30) #create font for buttons

        self.placing_tower = False #bool for if player is in placement mode (hover)
        self.tower_type = None #which tower they are placing
        self.active_tower_surf = None #graphic for hover/placement

        self.import_assets()
        self.setup(self.tmx_maps['nz'])

        self.ui_buttons = [
            Button('chalamet tower','yo chalamet', 100, 100, (30,670), self.font, self.placement),
            Button('einstein tower','yo einstein', 100, 100, (160,670), self.font, self.placement),
            Button('tesla tower','yo nikola', 100, 100, (290,670), self.font, self.placement)
        ]
        
        
    def placement(self, tower_type): #gets triggered when clicked 
        self.placing_tower = True
        self.tower_type = tower_type
    
        self.active_tower_surf = self.tower_preview_surf #from import_assets

        walkable = tower_rules.get(tower_type, {}).get('land_ok', True) #fetch rule for if tower can be placed on land
        waterable = tower_rules.get(tower_type, {}).get('water_ok', False) #fetch rule for if tower can be placed on water
        snowable = tower_rules.get(tower_type, {}).get('snow_ok', False) #fetch rule for if tower can be placed on snow

        print(f"Placing mode active for {tower_type} [can walk: {walkable} | can swim: {waterable} | can snow: {snowable} ]")


    def import_assets(self):
        self.tmx_maps = {
            'nz': load_pygame(join('Unesco-game-2026', 'data','maps','newzealand.tmx'))
            }

        print(self.tmx_maps)

        self.tower_preview_surf = pygame.Surface((TILE_SIZE, TILE_SIZE)) #set size of tower preview
        self.tower_preview_surf.fill((0, 0, 255)) #set tint of tower preview
        self.tower_preview_surf.set_alpha(150) #set transparency of tower preview

    def setup(self, tmx_map):
        #terrain
        for layer in ['Terrain', 'Water', 'Path', 'Terrain Top']:
            for x,y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        #objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            Sprite((obj.x, obj.y), obj.image, self.all_sprites)

        #entities
        for entity in tmx_map.get_layer_by_name('Entities'):
            pass #do stuff
        
    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            #event loop
            for event in pygame.event.get(): #check for pygame events
                if event.type == pygame.QUIT: #if player closes main window:
                    pygame.quit() #quit the game
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN: #if player presses a mouse button

                    if event.button == 3: #if its right mb
                        self.placing_tower = False
                        print(f'cancel place')

                    if event.button == 1 and self.placing_tower: #if its left (and the 'placing' boolean is true)
                        #double check it isnt ui
                        clicked_on_ui = mouse_pos[1] >= 640
                        if not clicked_on_ui: #if it isnt ui
                            mouse_pos = pygame.mouse.get_pos()
                            grid_x = mouse_pos[0] // TILE_SIZE
                            grid_y = mouse_pos[1] // TILE_SIZE
                            
                            Tower((grid_x, grid_y), self.active_tower_surf, self.all_sprites)
                            self.placing_tower = False

            #game logic
            self.all_sprites.update(dt)
            self.display_surf.fill('black')
            self.all_sprites.draw()

            #ghost preview for towers
            if self.placing_tower and self.active_tower_surf: #if placing & has surface
                mouse_pos = pygame.mouse.get_pos()
                clicked_on_ui = mouse_pos[1] >= 640
                if not clicked_on_ui: #if it isnt ui
                    snap_x = (mouse_pos[0] // TILE_SIZE) * TILE_SIZE
                    snap_y = (mouse_pos[1] // TILE_SIZE) * TILE_SIZE
                    self.display_surf.blit(self.active_tower_surf, (snap_x, snap_y))


            #buttons
            for button in self.ui_buttons:
                button.draw(self.display_surf)



            
            pygame.display.update() #update display


if __name__ == '__main__': #initialise game (failsafe; checks if this file is called main)
    game = Game()
    game.run()  




    '''
    for swimmable/ no on path (edit/simplify, this is placeholder):
    
    def placement(self, tower_type): 
        self.placing_tower = True
        self.tower_type = tower_type
        self.active_tower_surf = self.tower_preview_surf  

        #Define custom rules for each tower type
        #'water_ok': True means it can only/also go on water
        tower_rules = {
            'basic tower':    {'water_ok': False},
            'einstein tower': {'water_ok': False},
            'sub marine':      {'water_ok': True} #Example of a future water tower
        }

        #Safely fetch rules, defaulting to False if the type isn't listed yet
        self.current_tower_can_swim = tower_rules.get(tower_type, {}).get('water_ok', False)
        
        print(f"Placing mode active for: {tower_type} (Can swim: {self.current_tower_can_swim})")

        if event.button == 1 and self.placing_tower:
    mouse_pos = pygame.mouse.get_pos()
    
    clicked_on_ui_bar = mouse_pos[1] >= 650 
    clicked_on_button = any(button.rect.collidepoint(event.pos) for button in self.ui_buttons)

    if not clicked_on_ui_bar and not clicked_on_button:
        grid_x = mouse_pos[0] // TILE_SIZE
        grid_y = mouse_pos[1] // TILE_SIZE
        
        #Pull references to your layers
        path_layer = self.tmx_maps['nz'].get_layer_by_name('Path')
        water_layer = self.tmx_maps['nz'].get_layer_by_name('Water')

        #Check if tiles exist at this coordinate (returns a surface or None)
        has_path = path_layer.get_tile_image(grid_x, grid_y) is not None
        has_water = water_layer.get_tile_image(grid_x, grid_y) is not None

        #--- VALIDATION LOGIC ---
        is_allowed = True

        if has_path:
            is_allowed = False
            print("Can't build on the track!")
            
        elif has_water and not self.current_tower_can_swim:
            is_allowed = False
            print("This tower will drown! Land only.")
            
        elif not has_water and self.current_tower_can_swim:
            #Optional: Remove this block if your water towers are allowed on land too!
            is_allowed = False 
            print("This is a water tower! Put it in the drink.")

        #--- SPAWN TOWER ---
        if is_allowed:
            snap_x = grid_x * TILE_SIZE
            snap_y = grid_y * TILE_SIZE
            
            #Pass the profile data down to your Tower instance if it needs it later
            Tower((snap_x, snap_y), self.active_tower_surf, self.all_sprites)
            self.placing_tower = False
    
    '''