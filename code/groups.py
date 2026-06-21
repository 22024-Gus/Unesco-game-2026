from settings import * #importing variables, constants, etc. from settings.py

class AllSprites(pygame.sprite.Group): #creates a group (named AllSprites).
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface() #sets up the surface
        self.offset = vector() #position of the sprite

    def draw(self): #draw function
        for sprite in self: #for every sprite in the group
            self.display_surf.blit(sprite.image, sprite.rect) #draws the sprites onto the screen
