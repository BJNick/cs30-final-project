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
                    elif "corner" in value:
                        new_tile = Tile(value, (255,255,100))
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

    # Returns the tile at this location
    def get_tile_at(self, row, column):
        return self.map[(row, column)]



# A parent class that contains basic methods for drawing a tile
class Tile:

    # A basic tile contains it's row, column and color
    def __init__(self, name="empty", color=(100,100,100)):
        self.name = name
        self.color = color

    # Draws the tile
    def draw(self, surface : pygame.Surface, rect : pygame.Rect):
        surface.fill(self.color, rect)


# Contains all information about the player character in the game
class Player:

    def __init__(self, grid : Grid, row=0, column=0):
        self.grid = grid
        self.row = row
        self.column = column
        self.sprite = pygame.Surface((grid.tile_size, grid.tile_size))\
            .convert_alpha()
        self.speed = 3.5
        self.movement_directions = []
        self.boomerang = None
        self.has_boomerang = True

    # Updates the movement based on key presses
    def update(self, delta_time):
        if len(self.movement_directions) > 0:
            self.move(self.movement_directions[0], delta_time * self.speed)

    # Makes the player move in a given direction
    def set_moving(self, direction, condition):
        if condition:
            self.movement_directions.insert(0, direction)
        elif direction in self.movement_directions:
            self.movement_directions.remove(direction)

    # Tries to move the player in a given direction, returns True if succeeds
    def move(self, direction, distance):
        row_displacement = 0
        column_displacement = 0
        # Set displacement according to the direction
        if direction == "up":
            row_displacement = -1
        elif direction == "down":
            row_displacement = 1
        elif direction == "left":
            column_displacement = -1
        elif direction == "right":
            column_displacement = 1

        adjacent_tile = round(self.row + row_displacement / 2), \
                        round(self.column + column_displacement / 2)

        # If it's empty, go there
        if self.grid.is_open_space(*adjacent_tile):
            if row_displacement != 0 or column_displacement != 0:
                self.row += row_displacement * distance
                self.column += column_displacement * distance
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

    # Checks if the boomerang was thrown
    def boomerang_in_air(self):
        return self.boomerang != None

    # Creates and throws the boomerang
    def throw_boomerang(self):
        if not self.has_boomerang and \
                abs(self.row - self.boomerang.row) < 1 and \
                abs(self.column - self.boomerang.column) < 1:
            self.has_boomerang = True
            self.boomerang = None
            return
        if not self.has_boomerang:
            return
        if len(self.movement_directions) > 0:
            self.boomerang = Boomerang(self.grid, self.row, self.column)
            self.boomerang.set_moving(self.movement_directions[0], True)
            self.has_boomerang = False
        else:
            return


class Boomerang:

    def __init__(self, grid : Grid, row=0, column=0):
        self.grid = grid
        self.row = row
        self.column = column
        self.sprite = pygame.Surface((grid.tile_size, grid.tile_size))\
            .convert_alpha()
        self.speed = 5
        self.movement_directions = set()

    # Updates the movement based on key presses
    def update(self, delta_time):
        last_dirs = set(self.movement_directions)
        for dir in last_dirs:
            has_moved = self.move(dir, delta_time * self.speed)
            if has_moved:
                self.adjust_trajectory(dir, delta_time)
            next_tile, next_pos = self.get_next_tile(dir)
            if self.collides_with(next_tile, next_pos):
                # If it collided with something, reverse direction
                if "corner" in next_tile.name:
                    new_dir = self.corner_bounce(dir, next_tile.name)
                else:
                    new_dir = self.reverse_direction(dir)
                self.set_moving(dir, False)
                self.set_moving(new_dir, True)

    # Makes the boomerang move in a given direction
    def set_moving(self, direction, condition):
        if condition:
            self.movement_directions.add(direction)
        elif direction in self.movement_directions:
            self.movement_directions.remove(direction)

    # Reverses the given direction
    def reverse_direction(self, direction):
        if direction == "up":
            return "down"
        elif direction == "down":
            return "up"
        elif direction == "left":
            return "right"
        elif direction == "right":
            return "left"

    # Bounce off a corner
    def corner_bounce(self, direction : str, corner_name : str):
        init_dir_letter = direction[0].upper()
        # If coming to a flat side, then reverse
        if not init_dir_letter in corner_name:
            return self.reverse_direction(direction)
        # Else find the other direction to go
        else:
            new_dir_letter = corner_name.removeprefix("corner")\
                .replace(init_dir_letter, "")
            for dir in ["up", "down", "left", "right"]:
                if new_dir_letter.lower() in dir:
                    return self.reverse_direction(dir)

    # Returns the next tile according to movement in this direction
    def get_next_tile(self, direction):
        row_displacement = 0
        column_displacement = 0
        # Set displacement according to the direction
        if direction == "up":
            row_displacement = -1
        elif direction == "down":
            row_displacement = 1
        elif direction == "left":
            column_displacement = -1
        elif direction == "right":
            column_displacement = 1
        adjacent_tile = round(self.row + row_displacement / 2), \
                        round(self.column + column_displacement / 2)
        return self.grid.get_tile_at(*adjacent_tile), adjacent_tile

    # Tries to move the player in a given direction, returns None if succeeds
    def move(self, direction, distance):
        row_displacement = 0
        column_displacement = 0
        # Set displacement according to the direction
        if direction == "up":
            row_displacement = -1
        elif direction == "down":
            row_displacement = 1
        elif direction == "left":
            column_displacement = -1
        elif direction == "right":
            column_displacement = 1

        next_tile, next_tile_pos = self.get_next_tile(direction)

        # If it's empty, go there
        if next_tile.name != "wall":
            if row_displacement != 0 or column_displacement != 0:
                self.row += row_displacement * distance
                self.column += column_displacement * distance
                return True
        # Else stay where you are
        return False

    # Adjust trajectory to stay on round coordinates
    def adjust_trajectory(self, direction, delta_time):
        if direction in ["up", "down"]:
            adjust = round(self.column) - self.column
            if abs(adjust) <= 0.01:
                self.column = round(self.column)
            else:
                self.column += adjust/10
        else:
            adjust = round(self.row) - self.row
            if abs(adjust) <= 0.01:
                self.row = round(self.row)
            else:
                self.row += adjust/10

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
        pygame.draw.circle(self.sprite, (255,100,0),
                           self.sprite.get_rect().center,
                           self.sprite.get_width()/4)
        return self.sprite

    # Checks for collision with a tile
    def collides_with(self, tile : Tile, tile_pos, position=None):
        if position == None:
            position = self.row, self.column
        my_row, my_column = position
        tile_row, tile_column = tile_pos
        if tile.name == "wall":
            if tile_row + 1 < my_row or tile_row > my_row + 1:
                return False
            if tile_column + 1 < my_column or tile_column > my_column + 1:
                return False
            return True
        elif "corner" in tile.name:
            if abs(tile_row - my_row) < 0.1 and \
                    abs(tile_column - my_column) < 0.1:
                return True
        return False
