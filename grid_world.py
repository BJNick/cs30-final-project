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
                                       self.height * self.tile_size))

        # Opens the map data file and reads into memory
        with open("map_data.csv") as file:
            for row, line in enumerate(file):
                if len(line.strip()) == 0:
                    continue
                for column, value in enumerate(line.strip().split(",")):
                    if value == "wall":
                        new_tile = Tile("wall", (255,255,255))
                    elif value == "spikes":
                        new_tile = Tile("spikes", (255,100,100))
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
        self.surface.fill((0,0,0))
        # Draw individual tiles
        for row in range(self.height):
            for column in range(self.width):
                self.map[(row, column)].draw(self.surface,
                                             self.get_tile_rect(row, column))
        # Return the rendered image
        return self.surface

    # Checks if the player can go there
    def is_open_space(self, row, column):
        return self.map[(row, column)].name != "wall"



# A parent class that contains basic methods for drawing a tile
class Tile:

    # A basic tile contains it's row, column and color
    def __init__(self, name="empty", color=(100,100,100)):
        self.name = name
        self.color = color

    # Draws the tile
    def draw(self, surface : pygame.Surface, rect : pygame.Rect):
        surface.fill(self.color, rect)


class Player:

    def __init__(self, grid : Grid, row=0, column=0):
        self.grid = grid
        self.row = row
        self.column = column
        self.sprite = pygame.Surface((grid.tile_size, grid.tile_size))\
            .convert_alpha()

    # Tries to move the player in a given direction, returns True if succeeds
    def move(self, direction):
        new_row = self.row
        new_column = self.column
        if direction == "up":
            if self.row > 0:
                new_row -= 1
        elif direction == "down":
            if self.row < self.grid.height:
                new_row += 1
        elif direction == "left":
            if self.column > 0:
                new_column -= 1
        elif direction == "right":
            if self.column < self.grid.width:
                new_column += 1
        # If it's empty, go there
        if self.grid.is_open_space(new_row, new_column):
            if new_row != self.row or new_column != self.column:
                self.row = new_row
                self.column = new_column
                return True
        # Else stay where you are
        return False

    # Returns a rect in the position of the player
    def get_rect(self):
        x = self.grid.tile_size * self.column
        y = self.grid.tile_size * self.row
        return pygame.Rect(x, y, self.grid.tile_size, self.grid.tile_size)

    # Redraws the player's sprite and returns it
    def draw_sprite(self) -> pygame.Surface:
        # Clear the sprite with transparency
        self.sprite.fill((0,0,0,0))
        # Draw a circle in the center
        pygame.draw.circle(self.sprite, (0,255,0),
                           self.sprite.get_rect().center,
                           self.sprite.get_width()/3)
        return self.sprite
