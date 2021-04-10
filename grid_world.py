"""
Mykyta S.
grid_world.py

A module that contains the definition of a game map called the Grid, which
stores the information about tiles and entities from a map data file.
"""

# My own module
from tiles import *
from moving_entities import *


# A class that stores information about the game map, tiles on the grid,
# and all entities located within its boundaries.
class Grid:

    # Initialize all the needed variables
    def __init__(self, file_name, tile_size=16):
        self.map = {}
        self.width, self.height = 0, 0
        self.tile_size = tile_size
        self.floor_sprite = pygame.image.load("sprites/floor.png")
        self.active_tiles = []
        self.enemies = []
        self.player = None
        self.coins = []
        self.surface = None

        # Opens the map data file and reads into memory
        with open(file_name) as file:
            for row, line in enumerate(file):
                if len(line.strip()) == 0:
                    continue
                self.height = max(self.height, row + 1)
                for column, value in enumerate(line.strip().split(",")):
                    value = value.strip()
                    self.width = max(self.width, column + 1)
                    # Add a tile based on the name
                    if value == "wall":
                        new_tile = Tile("wall")
                    elif "spikes" in value:
                        new_tile = Spikes(value)
                    elif "switch" in value:
                        new_tile = Switch(value)
                    elif "corner" in value:
                        new_tile = Corner(value)
                    elif "exit" in value:
                        new_tile = Exit(value)
                    else:
                        new_tile = Tile("empty")
                    # Add player and enemies
                    if value == "player":
                        self.player = Player(self, row, column)
                    elif value == "enemy":
                        self.enemies.append(Enemy(self, row, column))
                    elif value == "coin":
                        self.coins.append(Coin(self, row, column))

                    self.map[(row, column)] = new_tile
                    if new_tile.is_active:
                        new_tile.set_coordinates(self, row, column)
                        self.active_tiles.append(new_tile)

    # Update entity movement
    def update_entities(self, delta_time):
        # Update the player and the boomerang if it's in the air
        self.player.update(delta_time)
        if self.player.boomerang_in_air():
            self.player.boomerang.update(delta_time)
        # Update enemies
        for enemy in self.enemies:
            enemy.update(delta_time)
        # Update coins and remove ones that were picked up
        i = 0
        while i < len(self.coins):
            self.coins[i].update(delta_time)
            if self.coins[i].is_picked_up:
                self.coins.remove(self.coins[i])
            else:
                i += 1

    # Draw all entities
    def draw_entities(self, surface):
        # Draw enemies and coins
        for enemy in self.enemies:
            surface.blit(*enemy.draw_sprite())
        for coin in self.coins:
            surface.blit(*coin.draw_sprite())
        # Draw the player and the boomerang if it's in the air
        surface.blit(*self.player.draw_sprite())
        if self.player.boomerang_in_air():
            surface.blit(*self.player.boomerang.draw_sprite())

    # Returns the rect of a tile based on the grid
    def get_tile_rect(self, row, column):
        x = self.tile_size * column
        y = self.tile_size * row
        return pygame.Rect(x, y, self.tile_size, self.tile_size)

    # Draws the entire grid and returns the picture
    def draw_grid(self, screen : pygame.Surface):
        # Create a new surface / clear the previous one
        self.surface = pygame.Surface((self.width * self.tile_size,
                                       self.height * self.tile_size)) \
            .convert_alpha()
        # Draw individual tiles
        for row in range(self.height):
            for column in range(self.width):
                # First render floor
                self.surface.blit(self.floor_sprite,
                                  self.get_tile_rect(row, column))
                # Then draw a tile on top of it
                self.map[(row, column)].draw(self.surface,
                                             self.get_tile_rect(row, column))
        # Blit the final image onto the screen
        screen.blit(self.surface, screen.get_rect())

    # Checks if the player can go there
    def is_open_space(self, row, column):
        if (row, column) not in map:
            return False
        return self.map[(row, column)].name != "wall"

    # Returns the tile at this location
    def get_tile_at(self, row, column):
        return self.map.get((row, column), Tile())
