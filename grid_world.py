"""
Mykyta S.
grid_world.py
A module that contains necessary grid classes
"""

import pygame
import player_character
import enemies


# A class that stores information about the grid world in a dictionary
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
                        new_tile = CornerTile(value)
                    elif "exit" in value:
                        new_tile = Exit(value)
                    else:
                        new_tile = Tile("empty")
                    # Add player and enemies
                    if value == "player":
                        self.player = \
                            player_character.Player(self, row, column)
                    elif value == "enemy":
                        self.enemies.append(enemies.Enemy(self, row, column))
                    elif value == "coin":
                        self.coins.append(enemies.Coin(self, row, column))

                    self.map[(row, column)] = new_tile
                    if new_tile.is_active:
                        new_tile.set_coordinates(self, row, column)
                        self.active_tiles.append(new_tile)

    # Update enemy movement
    def update_enemies(self, delta_time):
        for enemy in self.enemies:
            enemy.update(delta_time)
        i = 0
        while i < len(self.coins):
            self.coins[i].update(delta_time)
            if self.coins[i].is_picked_up:
                self.coins.remove(self.coins[i])
            else:
                i += 1

    # Draw enemies and coins
    def draw_enemies(self, surface):
        for enemy in self.enemies:
            surface.blit(*enemy.draw_sprite())
        for coin in self.coins:
            surface.blit(*coin.draw_sprite())

    # Returns the rect of a tile based on the grid
    def get_tile_rect(self, row, column):
        x = self.tile_size * column
        y = self.tile_size * row
        return pygame.Rect(x, y, self.tile_size, self.tile_size)

    # Draws the entire grid and returns the picture
    def draw_grid(self) -> pygame.Surface:
        # Create a new surface
        self.surface = pygame.Surface((self.width * self.tile_size,
                                       self.height * self.tile_size)) \
            .convert_alpha()
        # Draw individual tiles
        for row in range(self.height):
            for column in range(self.width):
                self.surface.blit(self.floor_sprite,
                                  self.get_tile_rect(row, column))
                self.map[(row, column)].draw(self.surface,
                                             self.get_tile_rect(row, column))
        # Return the rendered image
        return self.surface

    # Checks if the player can go there
    def is_open_space(self, row, column):
        if (row, column) not in map:
            return False
        return self.map[(row, column)].name != "wall"

    # Returns the tile at this location
    def get_tile_at(self, row, column):
        return self.map.get((row, column), Tile())


# A parent class that contains basic methods for drawing a tile
class Tile:
    wall_sprite = None

    # A basic wall tile
    def __init__(self, name="wall"):
        self.name = name
        # Can the tile interact with entities?
        self.is_active = False

    # Loads the basic wall sprite
    @staticmethod
    def get_wall_sprite():
        if Tile.wall_sprite is None:
            Tile.wall_sprite = pygame.image.load("sprites/wall.png")
        return Tile.wall_sprite

    # Draws the tile
    def draw(self, surface: pygame.Surface, rect: pygame.Rect):
        if self.name == "empty":
            return
        surface.blit(Tile.get_wall_sprite(), rect)


# A class for the corners that turn the boomerang
class CornerTile(Tile):
    corner_sprites = None

    # Loads the sprites into memory
    @staticmethod
    def load_sprites():
        if CornerTile.corner_sprites is not None:
            return CornerTile.corner_sprites
        CornerTile.corner_sprites = dict()
        for name in ["cornerUL", "cornerDL", "cornerUR", "cornerDR"]:
            CornerTile.corner_sprites[name] = pygame.image \
                .load("sprites/" + name + ".png")
        return CornerTile.corner_sprites

    # Draws the tile
    def draw(self, surface: pygame.Surface, rect: pygame.Rect):
        surface.blit(CornerTile.load_sprites()[self.name], rect)


# A method for active tiles
class ActiveTile(Tile):

    def __init__(self, name="wall"):
        super().__init__(name)
        self.grid = None
        self.row = -1
        self.column = -1
        self.is_active = True

    def set_coordinates(self, grid: Grid, row, column):
        self.row = row
        self.column = column
        self.grid = grid


# A class for the spikes
class Spikes(ActiveTile):
    sprites = None

    # Initialize the spikes
    def __init__(self, name="spikes"):
        self.is_armed = True
        if "unarmed" in name:
            self.is_armed = False
            name = name.split(" ")[0]
        super().__init__(name)

    # Loads sprites for the spikes
    @staticmethod
    def load_sprites():
        if Spikes.sprites is None:
            Spikes.sprites = []
            for name in ["spikes", "spikes-hidden"]:
                Spikes.sprites.append(pygame.image
                                      .load("sprites/" + name + ".png"))
        return Spikes.sprites

    # Toggles the spikes
    def toggle(self):
        self.is_armed = not self.is_armed

    # Draws the tile
    def draw(self, surface: pygame.Surface, rect: pygame.Rect):
        # Pick the sprite depending on whether the spikes are armed
        sprite_id = 0 if self.is_armed else 1
        surface.blit(Spikes.load_sprites()[sprite_id], rect)


# A class for a switch
class Switch(ActiveTile):
    sprites = None

    def __init__(self, name="switch"):
        super().__init__(name)
        self.is_activated = False

    # Loads sprites for the spikes
    @staticmethod
    def load_sprites():
        if Switch.sprites is None:
            Switch.sprites = []
            for name in ["switch-left", "switch-right"]:
                Switch.sprites.append(pygame.image
                                      .load("sprites/" + name + ".png"))
        return Switch.sprites

    # Toggles the switch
    def toggle(self):
        self.is_activated = not self.is_activated
        # Switches spikes
        letter = self.name.removeprefix("switch")
        for tile in self.grid.active_tiles:
            if "spikes" in tile.name:
                if letter in tile.name.removeprefix("spikes"):
                    tile.toggle()
        for enemy in self.grid.enemies:
            enemy.update_path(True)

    # Draws the switch
    def draw(self, surface: pygame.Surface, rect: pygame.Rect):
        # Pick the sprite depending on whether the spikes are armed
        sprite_id = 0 if not self.is_activated else 1
        surface.blit(Switch.load_sprites()[sprite_id], rect)


# A class for the exit
class Exit(ActiveTile):
    sprites = None

    # Loads sprites for the exit
    @staticmethod
    def load_sprites():
        if Exit.sprites is None:
            Exit.sprites = [pygame.image.load("sprites/exit.png")]
        return Exit.sprites

    # Get level from the name
    def get_next_level(self):
        return self.name.split(" ")[1]

    # Draws the tile
    def draw(self, surface: pygame.Surface, rect: pygame.Rect):
        # Use the regular sprite
        surface.blit(Exit.load_sprites()[0], rect)
