import pygame


class PlatformCreate(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, all_sprites_group: pygame.sprite.Group):
        super().__init__(all_sprites_group)
        self.image = pygame.Surface((w, h))
        self.image.fill(pygame.Color('#00FF00'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y