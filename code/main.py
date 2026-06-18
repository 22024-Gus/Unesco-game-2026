from settings import * #importing variables, constants, etc. from settings.py
from pytmx.util_pygame import load_pygame #
from os.path import join

from sprites import Sprite, Button, Tower, Enemy
from groups import AllSprites

class Game:
    def __init__(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode((WIN_WID, WIN_HGT)) #setting resolution of window
        pygame.display.set_caption('epic game') #sets caption of game window
        self.clock = pygame.time.Clock() #start game clock

        self.all_sprites = AllSprites() #sprite group for updating (see groups.py)

        #tower attributes
        self.placing_tower = False #bool for if player is in placement mode (hover)
        self.tower_type = None #which tower they are placing
        self.active_tower_surf = None #graphic for hover/placement

        self.import_assets() #import assets for towers (and enemy, etc)
        self.setup(self.tmx_maps['nz']) #setup the map

        #wave attributes
        self.waypoints = self.get_path_waypoints(self.tmx_maps['nz']) #gather waypoints
        self.current_wave_idx = 0 #start at wave 0 (dict start at 0, its named wave 1)
        self.spawn_q = [] #spawn queue, spawn 'q' get it hahahah haha
        self.wave_active = False #track if running (for intermissions)

        #enemy attributes
        self.enemy_spawn_timer = 0
        self.spawn_cooldown = 1.5 #time (in secs) between enemy spawns
        
        self.font = pygame.font.Font(None,30) #create font for buttons
        self.ui_buttons = [
            Button('yo chalamet', 100, 100, (30,670), self.font, self.placement, 'timothy chalamet'),
            Button('yo einstein', 100, 100, (160,670), self.font, self.placement, 'albert einstein'),
            Button('yo nikola', 100, 100, (290,670), self.font, self.placement, 'nikola tesla'),
            Button('start next wave', 100, 100, (770, 670), self.font, self.next_wave, None)
        ]  

    def get_path_waypoints(self, tmx_map):
        rawpoints = []

        for wypnt in tmx_map.get_layer_by_name('Path Points'): #checks for objects in the path points layer
            try:
                point_order = int(wypnt.name)
            except (TypeError, ValueError): #if the name of the point isnt '0' or '11', etc.. then warn
                point_order = 0
                print(f"point at ({wypnt.x}, {wypnt.y}) is missing a numeric name") #show which point is missing the name

            rawpoints.append((point_order, (wypnt.x, wypnt.y))) #
        
        rawpoints.sort(key=lambda pt: pt[0]) #sorts points in numeric order which is same as order they move, 
        #this also removes the useless point number, passing a ordered list with just (x,y).
        
        waypoints = [point[1] for point in rawpoints]
        print(f"successfully loaded {len(waypoints)} waypoints")

        return waypoints

        
    def placement(self, tower_type): #gets triggered when clicked 
        self.placing_tower = True
        self.tower_type = tower_type
    
        self.active_tower_surf = self.tower_surfs[tower_type] #from import_assets (show image instead)

        self.tower_rect = self.active_tower_surf.get_frect() #rectangle to show where the tower wants to go

        self.walkable = tower_rules.get(tower_type, {}).get('land_ok', True) #fetch rule for if tower can be placed on land
        self.waterable = tower_rules.get(tower_type, {}).get('water_ok', False) #fetch rule for if tower can be placed on water
        self.snowable = tower_rules.get(tower_type, {}).get('snow_ok', False) #fetch rule for if tower can be placed on snow

        print(f"Placing mode active for {tower_type} [can walk: {self.walkable} | can swim: {self.waterable} | can snow: {self.snowable}]")

    def next_wave(self):
        if not self.wave_active: #only prepare if we arent already running one
            if self.current_wave_idx < len(enemy_waves):
                self.prepare_wave()
                self.wave_active = True
            else:
                print('no more waves')

    def import_assets(self):
        self.tmx_maps = { #import map from data folder
            'nz': load_pygame(join('Unesco-game-2026', 'data','maps','newzealand.tmx'))
            }
        
        self.tower_surfs = { #import surface textures from graphics folder
            'timothy chalamet': pygame.image.load(join('Unesco-game-2026', 'graphics', 'characters', 'chalamet.png')).convert_alpha(),
            'albert einstein': pygame.image.load(join('Unesco-game-2026', 'graphics', 'characters', 'einstein.png')).convert_alpha(),
            'nikola tesla': pygame.image.load(join('Unesco-game-2026', 'graphics', 'characters', 'tesla.png')).convert_alpha(),
        }

        self.enemy_surfs = { #import surface textures from graphics folder
            'jeff bezos': pygame.image.load(join('Unesco-game-2026', 'graphics', 'characters', 'bezos.png')).convert_alpha(),
            'donald trump': pygame.image.load(join('Unesco-game-2026', 'graphics', 'characters', 'trump.png')).convert_alpha(),
        }

    def setup(self, tmx_map):
        #terrain
        for layer in ['Terrain', 'Water', 'Snow', 'Path', 'Terrain Top']: # checks for 5 different layers, and creates tile sprites
            for x,y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites) #create sprite for tile

        #objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            Sprite((obj.x, obj.y), obj.image, self.all_sprites)

    def prepare_wave(self): #unpacks wave tuple in config into a flatlist queue
        #check if player has beaten all waves
        if self.current_wave_idx >= len(enemy_waves):
            print('you win')
            return

        current_wave_data = enemy_waves[self.current_wave_idx]
        self.spawn_q = []

        #convert [('jeff bezos', 67)] into ['jeff bezos', 'jeff bezos', 'jeff bezos', ...]

        for enemy_type, amount in current_wave_data:
            for _ in range(amount):
                self.spawn_q.append(enemy_type)

        print(f'--- wave {self.current_wave_idx + 1} prepared; {len(self.spawn_q)} total enemies ---')
    
    def check_wave_status(self): #checks if wave is cleared to progress
        if not self.wave_active: #if not active, dont check/add wave
            return
        #count enemies left
        enemies_alive = any(isinstance(sprite, Enemy) for sprite in self.all_sprites)

        # if q is empty and no enemies onscreen, trigger wave
        if len(self.spawn_q) == 0 and not enemies_alive:
            self.current_wave_idx += 1
            self.wave_active = False
        
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
                            #calculate grid position
                            #mouse_pos = pygame.mouse.get_pos()
                            grid_x = mouse_pos[0] // TILE_SIZE
                            grid_y = mouse_pos[1] // TILE_SIZE

                            #map layers
                            tmx_data = self.tmx_maps['nz']
                            path_idx = tmx_data.layers.index(tmx_data.get_layer_by_name('Path'))
                            water_idx = tmx_data.layers.index(tmx_data.get_layer_by_name('Water'))
                            snow_idx = tmx_data.layers.index(tmx_data.get_layer_by_name('Snow'))

                            #checking if tile at point has a sprite or not
                            has_path = tmx_data.get_tile_image(grid_x, grid_y, path_idx) is not None
                            has_water = tmx_data.get_tile_image(grid_x, grid_y, water_idx) is not None
                            has_snow = tmx_data.get_tile_image(grid_x, grid_y, snow_idx) is not None

                            #check for grid occupation
                            has_tower = False
                            for sprite in self.all_sprites:
                                if isinstance(sprite, Tower):
                                    #print(f"Tower at: {sprite.rect.topleft} | Preview at: {self.tower_rect.topleft}")
                                    if sprite.rect.colliderect(self.tower_rect):
                                        has_tower = True
                                        print('theres something there')
                                        break

                            #validation
                            can_place = True

                            if has_tower: #checks for existing towers, uses the grid occupation logic just above
                                can_place = False
                            elif has_path: #checks using has_path (if there is a sprite on path layer)
                                can_place = False
                            elif has_water and not self.waterable: #checks using has_water (if there is a sprite on water layer), matches with tower rules
                                can_place = False
                            elif has_snow and not self.snowable: #checks using has_snow (if there is a sprite on snow layer), matches with tower rules
                                can_place = False

                            #place tower
                            if can_place:
                                Tower((grid_x, grid_y), self.tower_type, self.active_tower_surf, self.all_sprites)
                                self.placing_tower = False

            #enemy spawning
            if self.wave_active and self.waypoints and self.spawn_q:
                self.enemy_spawn_timer += dt
                if self.enemy_spawn_timer >= self.spawn_cooldown:
                    #pull next enemy type out of q
                    next_enemy = self.spawn_q.pop(0)

                    #make enemy and feed it waypoints
                    Enemy(self.waypoints, next_enemy, self.enemy_surfs[next_enemy], self.all_sprites)
                    self.enemy_spawn_timer = 0 #reset timer

            self.check_wave_status()

            #game logic
            self.all_sprites.update(dt)
            self.display_surf.fill('black')
            self.all_sprites.draw()

            #ghost preview for towers
            if self.placing_tower and self.active_tower_surf: #if placing & has surface & on correct surface
                mouse_pos = pygame.mouse.get_pos()
                clicked_on_ui = mouse_pos[1] >= 640
                if not clicked_on_ui: #if it isnt ui
                    snap_x = (mouse_pos[0] // TILE_SIZE) * TILE_SIZE
                    snap_y = (mouse_pos[1] // TILE_SIZE) * TILE_SIZE

                    #update tower rect for collision detect
                    self.tower_rect.topleft = (snap_x, snap_y)
                    #show tower for real
                    self.display_surf.blit(self.active_tower_surf, (snap_x, snap_y))


            #buttons
            for button in self.ui_buttons:
                button.draw(self.display_surf)



            
            pygame.display.update() #update display


if __name__ == '__main__': #initialise game (failsafe; checks if isnt being called from different file)
    game = Game()
    game.run()