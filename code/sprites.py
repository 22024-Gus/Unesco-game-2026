from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Button:
    def __init__(self, tower_type, text, wid, hgt, pos, font):
        self.pressed = False

        # main button
        self.rect = pygame.Rect(pos[0], pos[1], wid, hgt)
        self.colour = "#2b292c"

        # text
        self.text_surf = font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.rect.center)

        self.tower_type = tower_type
    
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
                    placing = True
                    selected_tower = self.tower_type
                    print(placing, selected_tower)
                    self.pressed = False

class Tower:
    def __init__(self, pos, surf, groups):
        super.__init__(groups)
        self.image = surf
        
        # Snap the tower directly to the Tiled grid pixels
        # (grid_pos is a tuple like (5, 3))
        pixel_x = pos[0] * TILE_SIZE
        pixel_y = pos[1] * TILE_SIZE
        
        self.rect = self.image.get_frect(topleft = (pixel_x, pixel_y))
        
        # Add tower logic stats here later (range, damage, cooldown))
