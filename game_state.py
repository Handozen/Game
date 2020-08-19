import pygame

from pygame_gui import UIManager

from player import Player
from platform_create import PlatformCreate


class GameState:
    def __init__(self, window_surface: pygame.Surface, ui_manager: UIManager):
        # initialises attributes
        self.ui_manager = ui_manager
        self.window_surface = window_surface

        self.height = window_surface.get_height()
        self.width = window_surface.get_width()

        self.is_time_to_transition = False
        self.transition_target = "None"

        self.background_surface = None

        self.all_sprites = None
        self.platforms = None

        self.player = None

    def start(self):
        # Setup everything we need to run the state.

        # Resets transition variables
        self.is_time_to_transition = False
        self.transition_target = "None"

        # Creates a grey background on the screen
        self.background_surface = pygame.Surface(self.window_surface.get_size())
        self.background_surface.convert(self.window_surface)
        self.background_surface.fill(pygame.Color('#000000'))

        # create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

        # create player
        player_position = (self.window_surface.get_rect().centerx,
                           self.window_surface.get_rect().centery)
        #ADDITION self to this
        self.player = Player(self, pos=player_position,
                             all_sprites_group=self.all_sprites)

        # creates platforms
        p1 = PlatformCreate(0, self.height - 40, self.width, 40, self.all_sprites)
        self.all_sprites.add(p1)
        self.platforms.add(p1)

        #ADDITION
        p2 = PlatformCreate(self.width / 2 - 50, self.height * 3 / 4, 100, 20, self.all_sprites)
        self.all_sprites.add(p2)
        self.platforms.add(p2)

    def stop(self):
        # Cleanup everything we don't need once the state is no longer
        # running.
        self.background_surface = None

        # clean up player
        if self.player is not None:
            self.player.kill()
            self.player = None

        # double check the main sprite group is clear
        if self.all_sprites is not None:
            self.all_sprites.empty()
            self.all_sprites = None

        if self.platforms is not None:
            self.platforms.empty()
            self.platforms = None

    def time_to_transition(self) -> bool:
        # Check if it is time to leave this state and transition to
        # another.
        # Returns True if it is time to stop the state, False if it is
        # not.
        return self.is_time_to_transition

    def get_transition_target(self) -> str:
        # Get the ID string of the new state to transition to.
        # Returns string of state to transition to.
        return self.transition_target

    def update(self, time_delta: float):
        # Update the state once per loop including the amount of time
        # that has passed since the previous loop of the App.
        self.all_sprites.update(time_delta)
        self.ui_manager.update(time_delta=time_delta)

        # Collision detection
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.pos.y = hits[0].rect.top
            self.player.vel.y = 0

    def process_event(self, event: pygame.event.Event):
        # Give the state a chance to respond to any pygame events that
        # have been fired.
        self.player.process_event(event)
        self.ui_manager.process_events(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.is_time_to_transition = True
            self.transition_target = 'main_menu_state'


    def draw(self):
        # Draw this state to the application's window surface.
        self.window_surface.blit(self.background_surface, (0, 0))
        self.ui_manager.draw_ui(self.window_surface)
        self.all_sprites.draw(self.window_surface)