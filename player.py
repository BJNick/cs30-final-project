"""
Mykyta S.
player.py
A module that contains classes Player and Boomerang
"""

import pygame
from grid_world import Grid, Tile


# Contains all information about the player character in the game
class Player:

    def __init__(self, grid: Grid, row=0, column=0):
        self.grid = grid
        self.row = row
        self.column = column
        self.sprite = pygame.image.load("sprites/player.png")
        self.speed = 3.5
        self.movement_directions = []
        self.boomerang = None
        self.has_boomerang = True

    # Updates the movement based on key presses
    def update(self, delta_time):
        for direction in self.movement_directions:
            self.move(direction, round(delta_time * self.speed * 32) / 32)
        # if len(self.movement_directions) > 0:
        #    self.move(self.movement_directions[0], delta_time * self.speed)

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
        #self.sprite.fill((0, 0, 0, 0))
        # Draw a circle in the center
        #pygame.draw.circle(self.sprite, (0, 255, 0),
        #                   self.sprite.get_rect().center,
        #                   self.sprite.get_width() / 3)
        return self.sprite

    # Checks if the boomerang was thrown
    def boomerang_in_air(self):
        return self.boomerang is not None

    # Creates and throws the boomerang
    def throw_boomerang(self):
        # If doesn't have the boomerang, try to catch it
        if not self.has_boomerang and \
                abs(self.row - self.boomerang.row) < 1 and \
                abs(self.column - self.boomerang.column) < 1:
            self.has_boomerang = True
            self.boomerang = None
            return
        if not self.has_boomerang:
            return
        # Else create and throw the boomerang
        if len(self.movement_directions) > 0:
            self.boomerang = Boomerang(self.grid, self.row, self.column)
            self.boomerang.set_moving(self.movement_directions[0], True)
            self.has_boomerang = False
        else:
            return


class Boomerang:

    def __init__(self, grid: Grid, row=0, column=0):
        self.grid = grid
        self.row = row
        self.column = column
        self.sprite = pygame.image.load("sprites/boomerang.png")
        self.sprite45 = pygame.image.load("sprites/boomerang-45.png")
        self.speed = 7
        self.movement_direction = ""
        self.rotation = 0

    # Updates the movement
    def update(self, delta_time):
        last_dir = self.movement_direction
        has_moved = self.move(last_dir, delta_time * self.speed)
        if has_moved:
            self.adjust_trajectory(last_dir)
        next_tile, next_pos = self.get_next_tile(last_dir)
        if self.collides_with(next_tile, next_pos):
            # If it collided with something, reverse direction
            if "corner" in next_tile.name:
                new_dir = self.corner_bounce(last_dir, next_tile.name)
            else:
                new_dir = self.reverse_direction(last_dir)
            self.set_moving(last_dir, False)
            self.set_moving(new_dir, True)

    # Makes the boomerang move in a given direction
    def set_moving(self, direction, condition):
        if condition:
            self.movement_direction = direction
        elif direction in self.movement_direction:
            self.movement_direction = ""

    # Reverses the given direction
    @staticmethod
    def reverse_direction(direction):
        if direction == "up":
            return "down"
        elif direction == "down":
            return "up"
        elif direction == "left":
            return "right"
        elif direction == "right":
            return "left"

    # Bounce off a corner
    def corner_bounce(self, direction: str, corner_name: str):
        init_dir_letter = direction[0].upper()
        # If coming to a flat side, then reverse
        if init_dir_letter not in corner_name:
            return self.reverse_direction(direction)
        # Else find the other direction to go
        else:
            new_dir_letter = corner_name.removeprefix("corner") \
                .replace(init_dir_letter, "")
            for direction in ["up", "down", "left", "right"]:
                if new_dir_letter.lower() in direction:
                    return self.reverse_direction(direction)

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
    def adjust_trajectory(self, direction):
        if direction in ["up", "down"]:
            adjust = round(self.column) - self.column
            if abs(adjust) <= 0.01:
                self.column = round(self.column)
            else:
                self.column += adjust / 10
        else:
            adjust = round(self.row) - self.row
            if abs(adjust) <= 0.01:
                self.row = round(self.row)
            else:
                self.row += adjust / 10

    # Returns a rect in the position of the player
    def get_rect(self):
        x = self.grid.tile_size * self.column
        y = self.grid.tile_size * self.row
        return pygame.Rect(x, y, self.grid.tile_size, self.grid.tile_size)

    # Redraws the player's sprite and returns it
    def draw_sprite(self) -> (pygame.Surface, pygame.Rect):
        # Clear the sprite with transparency
        #self.sprite.fill((0, 0, 0, 0))
        # Draw a circle in the center
        #pygame.draw.circle(self.sprite, (255, 100, 0),
        #                   self.sprite.get_rect().center,
        #                   self.sprite.get_width() / 4)
        angle_step = 45
        rounded_rotation = (self.rotation // angle_step) * angle_step
        sprite = self.sprite if rounded_rotation % 10 == 0 else self.sprite45

        rounded_rotation = (rounded_rotation // 90) * 90

        rotated_sprite = pygame.transform.rotate(sprite, rounded_rotation)

        rotated_rect = rotated_sprite.get_rect(center=self.get_rect().center)
        self.rotation += 5
        return rotated_sprite, rotated_rect

    # Checks for collision with a tile
    def collides_with(self, tile: Tile, tile_pos, position=None):
        if position is None:
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
            if self.movement_direction != "" and \
                    self.movement_direction[0].upper() not in tile.name:
                if tile_row + 1 < my_row or tile_row > my_row + 1:
                    return False
                if tile_column + 1 < my_column or tile_column > my_column + 1:
                    return False
                return True
            if abs(tile_row - my_row) < 0.1 and \
                    abs(tile_column - my_column) < 0.1:
                return True
        return False
