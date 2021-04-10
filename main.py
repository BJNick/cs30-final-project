"""
Mykyta S.
main.py

The run-time main class of this application. Class Game displays the game on
the screen.
"""

import sys
import os
import time

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Import my own modules (grid_world.py imports the rest)
import grid_world


# Convert path to EXE file data location
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# The class containing the primary methods and processes for updating and
# rendering the game on the screen, as well as receiving input.
class Game:

    # Initialize permanent variables
    def __init__(self, initial_map):
        pygame.init()
        pygame.display.set_icon(pygame.image.load(
            resource_path("sprites/enemy.png")))
        pygame.display.set_caption(
            "\"Boomerang\" Weekly Game Jam - Week 195 submission by BJNick")
        self.pixel_scale = 4
        self.size = self.width, self.height = \
            self.pixel_scale * 160, self.pixel_scale * 160
        self.screen = pygame.display.set_mode(self.size)
        font_path = resource_path("assets/DisposableDroidBB.ttf")
        self.ui_font_big = pygame.font.Font(font_path, self.pixel_scale * 16)
        self.ui_font = pygame.font.Font(font_path, self.pixel_scale * 8)
        self.grid, self.surface, self.last_inputs = None, None, None
        self.coin_count = 0
        self.throw_count = 0
        self.current_map = initial_map
        self.hint_text = []
        self.delta_time = 0.01
        # Load and play music
        pygame.mixer.music.load(resource_path("assets/music_compressed.ogg"))
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
        self.load_map(initial_map)

    # Initialize variables for a specific map
    def load_map(self, map_name):
        if self.grid and self.grid.player:
            self.last_inputs = self.grid.player.movement_directions
        self.current_map = map_name
        map_data_path = resource_path("levels/" + map_name + "_map_data.csv")
        self.grid = grid_world.Grid(map_data_path, 16)
        self.surface = pygame.Surface((self.grid.width * self.grid.tile_size,
                                       self.grid.height * self.grid.tile_size))
        self.width, self.height = self.surface.get_rect().size
        self.width *= self.pixel_scale
        self.height *= self.pixel_scale
        self.size = self.width, self.height
        self.screen = pygame.display.set_mode(self.size)
        self.hint_text = []
        # Load text labels if necessary
        if "tutorial" in map_name or "the_end" in map_name:
            self.load_tutorial_text(map_name)

    # Load text hints for the tutorial
    def load_tutorial_text(self, level_name):
        file_name = resource_path("levels/" + level_name + "_text.csv")
        self.hint_text = []
        with open(file_name) as file:
            for row, line in enumerate(file):
                if len(line.strip()) == 0:
                    continue
                hint = line.strip().split(",")
                hint = hint[0].replace(";", ","), float(hint[1]) - 1, float(
                    hint[2]) - 1
                self.hint_text.append(hint)

    def display_level_info(self):
        # Display level name
        level_text = self.current_map.replace("_", " ").capitalize()
        space = self.draw_top_text(level_text, self.ui_font,
                                   self.pixel_scale * 4)
        # Display coin amount
        coin_text = "Coins: " + \
                    str(self.coin_count + self.grid.player.coin_count)
        space = self.draw_top_text(coin_text, self.ui_font, space)
        # Display the number of throws
        throws_text = "Throws: " + \
                      str(self.throw_count + self.grid.player.throw_count)
        self.draw_top_text(throws_text, self.ui_font, space)

    # Process key presses and exits
    def process_events(self):
        for event in pygame.event.get():
            # Exit when quit button is pressed
            if event.type == pygame.QUIT:
                sys.exit()
            # Process the key down presses
            elif event.type == pygame.KEYDOWN:
                # Throw the boomerang on space bar
                if event.key == pygame.K_SPACE:
                    if self.grid.player.is_dead:
                        self.load_map(self.current_map)
                    else:
                        self.grid.player.throw_boomerang()

            self.grid.player.process_key_presses(event)

    # Draws text on the top of the screen
    def draw_top_text(self, string, font: pygame.font.Font, space):
        text = font.render(string, False, (255, 255, 255))
        text_rect = text.get_rect()
        coordinates = (0, 4 * self.pixel_scale)
        self.screen.blit(text, (coordinates[0] + space, coordinates[1]))
        return space + text_rect.width + 16 * self.pixel_scale

    # Draws text in the middle
    def draw_middle_text(self, string, font: pygame.font.Font, space):
        text = font.render(string, False, (255, 255, 255))
        text_rect = text.get_rect()
        coordinates = (self.width / 2 - text_rect.width / 2,
                       self.height / 2 - text_rect.height / 2)
        self.screen.blit(text, (coordinates[0], coordinates[1] + space))
        return space + font.get_linesize() - 4 * self.pixel_scale

    # The main procedure with game logic
    def game_loop(self):
        # Process keyboard input
        self.process_events()
        # Update positions
        self.grid.update_entities(self.delta_time)
        # Draw everything on the screen
        self.surface.fill((0, 0, 0))
        self.grid.draw_grid(self.surface)
        self.grid.draw_entities(self.surface)
        # Scale up to fit the screen
        pygame.transform.scale(self.surface, self.size, self.screen)
        # Show coins and throws if the tutorial is finished
        if "tutorial_1" not in self.current_map:
            self.display_level_info()
        # Show Game Over if the player has died
        if self.grid.player.is_dead:
            line = self.draw_middle_text("Game Over", self.ui_font_big, 0)
            self.draw_middle_text("Press space to retry", self.ui_font, line)
        # Show tutorial tips
        for hint in self.hint_text:
            text = self.ui_font.render(hint[0], False, (255, 255, 255))
            hint_pos = (hint[2] * 16 + 4) * self.pixel_scale, \
                       (hint[1] * 16 + 4) * self.pixel_scale
            self.screen.blit(text, hint_pos)
        # Change the frame
        pygame.display.flip()
        time.sleep(0.01)
        # Next level
        if self.grid.player.on_exit:
            if "tutorial_1" not in self.current_map:
                self.coin_count += self.grid.player.coin_count
                self.throw_count += self.grid.player.throw_count
            next_level = self.grid.player.on_exit.get_next_level()
            if next_level is None:
                sys.exit()
            self.load_map(next_level)


# Starts the game on run
if __name__ == "__main__":
    game = Game("tutorial_1")
    while True:
        game.game_loop()
