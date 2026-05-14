from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.offset = vector()

    def draw(self, player_center):
        self.offset.x = -(player_center[0] - WIN_WID / 2)
        self.offset.y = -(player_center[1] - WIN_HGT / 2)

        for sprite in self:
            self.display_surf.blit(sprite.image, sprite.rect.topleft + self.offset)
