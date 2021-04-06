"""
Mykyta S.
grid_world.py
A module that contains necessary grid classes
"""

import pygame


# A class that stores information about the grid world in a dictionary
class Grid:

    def __init__(self, tile_size=20):
        self.map = {}
        self.width = 10
        self.height = 10
        self.tile_size = tile_size
        self.surface = pygame.Surface((self.width * self.tile_size,
                                       self.height * self.tile_size))\
            .convert_alpha()
        self.floor_sprite = pygame.image.load("sprites/floor.png")

        # Opens the map data file and reads into memory
        with open("map_data.csv") as file:
            for row, line in enumerate(file):
                if len(line.strip()) == 0:
                    continue
                for column, value in enumerate(line.strip().split(",")):
                    value = value.strip()
                    if value == "wall":
                        new_tile = Tile("wall")
                    elif value == "spikes":
                        new_tile = Spikes("spikes")
                    elif "corner" in value:
                        new_tile = CornerTile(value)
                    else:
                        new_tile = Tile("empty")
                    self.map[(row, column)] = new_tile

    # Returns the rect of a tile based on the grid
    def get_tile_rect(self, row, column):
        x = self.tile_size * column
        y = self.tile_size * row
        return pygame.Rect(x, y, self.tile_size, self.tile_size)

    # Draws the entire grid and returns the picture
    def draw_grid(self) -> pygame.Surface:
        # Clear the surface
        self.surface.fill((0, 0, 0, 0))
        # Draw individual tiles
        for row in range(self.height):
            for column in range(self.width):
                self.surface.blit(self.floor_sprite, self.get_tile_rect(row, column))
                self.map[(row, column)].draw(self.surface,
                                             self.get_tile_rect(row, column))
        # Return the rendered image
        return self.surface

    # Checks if the player can go there
    def is_open_space(self, row, column):
        return self.map[(row, column)].name != "wall"

    # Returns the tile at this location
    def get_tile_at(self, row, column):
        return self.map[(row, column)]


# A parent class that contains basic methods for drawing a tile
class Tile:

    wall_sprite = None

    @staticmethod
    def get_wall_sprite():
        if Tile.wall_sprite is None:
            Tile.wall_sprite = pygame.image.load("sprites/wall.png")
        return Tile.wall_sprite

    # A basic tile contains it's row, column and color
    def __init__(self, name="empty"):
        self.name = name

    # Draws the tile
    def draw(self, surface: pygame.Surface, rect: pygame.Rect):
        if self.name == "empty":
            return
        surface.blit(Tile.get_wall_sprite(), rect)


class CornerTile(Tile):

    corner_sprites = None

    @staticmethod
    def load_sprites():
        if CornerTile.corner_sprites is not None:
            return CornerTile.corner_sprites
        CornerTile.corner_sprites = dict()
        for name in ["cornerUL", "cornerDL", "cornerUR", "cornerDR"]:
            CornerTile.corner_sprites[name] = pygame.image\
                .load("sprites/" + name + ".png")
        return CornerTile.corner_sprites


    def draw(self, surface: pygame.Surface, rect: pygame.Rect):
        surface.blit(CornerTile.load_sprites()[self.name], rect)


class Spikes(Tile):

    spike_sprites = None

    @staticmethod
    def load_sprites():
        if Spikes.spike_sprites is None:
            Spikes.spike_sprites = []
            for name in ["spikes"]:
                Spikes.spike_sprites.append(pygame.image
                    .load("sprites/" + name + ".png"))
        return Spikes.spike_sprites


    def draw(self, surface: pygame.Surface, rect: pygame.Rect):
        surface.blit(Spikes.load_sprites()[0], rect)