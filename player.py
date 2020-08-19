from typing import Tuple

import pygame

vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, GameState, pos: Tuple[int, int], all_sprites_group: pygame.sprite.Group):
        super().__init__(all_sprites_group)

        # ADDITION added attribute and var for gamestate
        self.GameState = GameState

        # Creates image and rectangle
        self.all_sprites_group = all_sprites_group
        self.image = pygame.Surface((20, 40))
        self.image.fill(pygame.Color('#FFFF00'))
        self.rect = self.image.get_rect()

        # Creates position, velocity and acceleration vectors
        self.pos = vec(pos[0], pos[1])
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.move_left = False
        self.move_right = False

        # Motion constants
        self.player_acc = 0.7
        self.player_friction = -0.12

    def process_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_left = True
            elif event.key == pygame.K_RIGHT:
                self.move_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.move_left = False
            elif event.key == pygame.K_RIGHT:
                self.move_right = False

        # ADDITION
        # Check when to jump
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.jump()

    # ADDITION
    def jump(self):
        # jump only when standing on a platform
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.GameState.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y += -15

    def update(self, time_delta: float):
        # Change in acceleration depending on player inputs
        self.acc = vec(0, 0.7)
        # ADDITION (ADDED IF FUNCTION SO BOTH MEANS NOTHING)
        if not (self.move_left and self.move_right):
            if self.move_left:
                self.acc.x = -self.player_acc
            if self.move_right:
                self.acc.x = self.player_acc

        # apply friction
        self.acc.x += self.vel.x * self.player_friction
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos
