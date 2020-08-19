import pygame

from pygame_gui import UIManager, UI_BUTTON_PRESSED
from pygame_gui.elements import UIButton


class MainMenuState:
    def __init__(self, window_surface: pygame.Surface, ui_manager: UIManager):
        # initialises attributes
        self.window_surface = window_surface
        self.ui_manager = ui_manager

        self.start_game_button = None

        self.is_time_to_transition = False
        self.transition_target = "None"

        self.background_surface = None

    def start(self):
        # Setup everything we need to run the state.

        # Resets transition variables
        self.is_time_to_transition = False
        self.transition_target = "None"

        # Creates a grey background on the screen
        self.background_surface = pygame.Surface(self.window_surface.get_size())
        self.background_surface.convert(self.window_surface)
        self.background_surface.fill(pygame.Color('#202020'))

        # Creates the button to start the game
        start_game_button_pos_rect = pygame.Rect(0, 0, 150, 40)
        start_game_button_pos_rect.centerx = self.window_surface.get_rect().centerx
        start_game_button_pos_rect.top = self.window_surface.get_height() * 0.4
        self.start_game_button = UIButton(relative_rect=start_game_button_pos_rect,
                                          text="Start Game",
                                          manager=self.ui_manager)

    def stop(self):
        # Cleanup everything we don't need once the state is no longer
        # running.
        self.start_game_button.kill()

        self.background_surface = None

        self.start_game_button = None

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
        self.ui_manager.update(time_delta=time_delta)

    def process_event(self, event: pygame.event.Event):
        # Give the state a chance to respond to any pygame events that
        # have been fired.
        self.ui_manager.process_events(event)

        if (event.type == pygame.USEREVENT and
                event.user_type == UI_BUTTON_PRESSED and
                event.ui_element == self.start_game_button):

            self.is_time_to_transition = True
            self.transition_target = 'game_state'

    def draw(self):
        # Draw this state to the application's window surface.
        self.window_surface.blit(self.background_surface, (0, 0))
        self.ui_manager.draw_ui(self.window_surface)