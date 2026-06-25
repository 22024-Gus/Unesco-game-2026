from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Button:
    def __init__(self, text, wid, hgt, pos, font, action, tower_type):
        self.pressed = False

        # main button
        self.rect = pygame.Rect(pos[0], pos[1], wid, hgt)
        self.colour = "#2b292c"

        # text
        self.text_surf = font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.rect.center)

        self.tower_type = tower_type
        self.action = action
    
    def draw(self, display):
        pygame.draw.rect(display, self.colour, self.rect)
        display.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    if self.tower_type:
                        self.action(self.tower_type)
                    else:
                        self.action()
                    self.pressed = False
        else:
            if not pygame.mouse.get_pressed()[0]:
                self.pressed = False

class Tower(pygame.sprite.Sprite):
    def __init__(self, pos, tower_type, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.tower_type = tower_type
        
        pixel_x = pos[0] * TILE_SIZE
        pixel_y = pos[1] * TILE_SIZE
        
        self.rect = self.image.get_frect(topleft = (pixel_x, pixel_y))
        
        info = tower_info.get(tower_type, {'damage': 10, 'range': 3, 'cooldown': 1.0}) #collects info from settings.py, resorts to default config if cant find
        self.damage = info['damage']

        self.range = info['range'] * TILE_SIZE #range * tile size to map into pixels
        self.fire_rate = info['cooldown']
        self.fire_timer = 0

    def find_target(self, all_sprites): #finds the enemy furthest along track in range
        enemies_in_range = []
        tower_center = pygame.Vector2(self.rect.center) #find center of tower

        for sprite in all_sprites: #loops thru all sprites
            if isinstance(sprite, Enemy): #if sprite is an enemy
                enemy_center = pygame.Vector2(sprite.rect.center) #find center of enemy
                if tower_center.distance_to(enemy_center) <= self.range: #if tower range reaches enemy
                    enemies_in_range.append(sprite) #add to the list

        if not enemies_in_range: #if theres no enemy in range
            return None #return nil target
        
        #sort; look at waypoint index, then break ties by selecting closest to upcoming node
        enemies_in_range.sort(key=lambda enemy: (
            enemy.current_wypnt_idx,
            -pygame.Vector2(enemy.rect.center).distance_to(pygame.Vector2(enemy.waypoints[enemy.current_wypnt_idx]))
        ), reverse=True)

        return enemies_in_range[0]#returns closest to end
    
    def update(self, dt):
        if self.fire_timer > 0:
            self.fire_timer -= dt
        
        #pass group references to look thru active targets
        if self.groups():
            target = self.find_target(self.groups()[0])
            if target and self.fire_timer <= 0:
                self.shoot(target)

    def shoot(self, target):
        self.fire_timer = self.fire_rate
        target.health -= self.damage
        print(f"[{self.tower_type.title()}] shot {target.enemy_type.title()}, Remaining HP: {target.health}")

class Enemy(pygame.sprite.Sprite):
    def __init__(self, waypoints, enemy_type, surf, groups, game_ref):
        super().__init__(groups)
        self.game = game_ref
        self.image = surf
        self.enemy_type = enemy_type

        stats = enemy_info.get(enemy_type, {'speed': 50, 'health': 10, 'reward': 10}) #collects info from settings.py, resorts to default config if cant find
        self.speed = stats['speed']
        self.health = stats['health']
        self.reward = stats['reward']

        self.rect = self.image.get_frect(center=waypoints[0]) #set center to first waypoint
        self.waypoints = waypoints #for use in other functions
        self.current_wypnt_idx = 1 #if wypnt idx was 0, they would stall (distance would be 0, stuck etc.)

        self.pos = pygame.Vector2(self.rect.center)

    def update(self, dt):
        #death monitor
        if self.health <= 0:
            self.game.money += self.reward
            self.kill()
            return

        #map tracking
        if self.current_wypnt_idx >= len(self.waypoints):
            self.kill()
            print("enemy reached base, health loss")
            return
        
        #set target to next
        target = pygame.Vector2(self.waypoints[self.current_wypnt_idx])

        #calc vector
        direction = target - self.pos
        distance = direction.length()

        if distance > 0:
            direction = direction.normalize() #scale length to 1

            #move twrd
            self.pos += direction * self.speed * dt
            self.rect.center = self.pos

        #if close to target point, switch to next wypnt
        if distance < 2:
            self.current_wypnt_idx += 1