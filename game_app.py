import pygame

from pygame_gui import UIManager

from main_menu_state import MainMenuState
from game_state import GameState


class GameApp:
    def __init__(self):
        # initialises attributes
        pygame.init()

        self.window_surface = pygame.display.set_mode((640, 480))
        self.ui_manager = UIManager(window_resolution=self.window_surface.get_size())

        self.states = {"main_menu_state": MainMenuState(self.window_surface, self.ui_manager),
                       "game_state": GameState(self.window_surface, self.ui_manager)}
        self.active_state = self.states["main_menu_state"]
        self.active_state.start()

        self.clock = pygame.time.Clock()
        self.is_running = True

    def run(self):
        # Keeps looping the application until it's time to quit.
        while self.is_running:
            time_delta = self.clock.tick(30)/1000.0

            self.check_transition()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                self.active_state.process_event(event)

            self.active_state.update(time_delta=time_delta)

            self.active_state.draw()

            pygame.display.update()

    def check_transition(self):
        # Checks our active state to see if it's time to change over to a different state.
        if self.active_state.time_to_transition():
            self.active_state.stop()
            new_state = self.states[self.active_state.get_transition_target()]
            new_state.start()
            self.active_state = new_state

if __name__ == '__main__':
    app = GameApp()
    app.run()