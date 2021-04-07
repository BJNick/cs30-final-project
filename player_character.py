"""
Mykyta S.
player_character.py
A module that contains classes Player and Boomerang
"""

import pygame


# Defines basics of movement and rendering
class MovingEntity:

    def __init__(self, grid, row=0, column=0):
        self.grid = grid
        self.row = row
        self.column = column
        self.speed = 4
        self.movement_directions = []
        self.sprite = None
        self.adjusting_trajectory = False

    # Update position based on passed time
    def update(self, delta_time, step=64):
        for direction in self.movement_directions:
            rounded_distance = (delta_time * self.speed * step) / step
            self.move(direction, rounded_distance)
            if self.adjusting_trajectory:
                self.adjust_trajectory(direction)

    # Makes the entity move in a given direction
    def set_moving(self, direction, condition=True):
        if direction is None:
            self.movement_directions = []
        if condition:
            if direction not in self.movement_directions:
                self.movement_directions.insert(0, direction)
            reversed_dir = MovingEntity.reverse(direction)
            if reversed_dir in self.movement_directions:
                self.movement_directions.remove(reversed_dir)
        elif direction in self.movement_directions:
            self.movement_directions.remove(direction)

    # Move the entity in a given direction
    def move(self, direction, distance):
        row_disp, column_disp = MovingEntity.dir_to_disp(direction)
        self.row += row_disp * distance
        self.column += column_disp * distance
        return True

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

    # Get the rect of this entity
    def get_rect(self):
        x = self.grid.tile_size * self.column
        y = self.grid.tile_size * self.row
        return pygame.Rect(x, y, self.grid.tile_size, self.grid.tile_size)

    # Draw a placeholder square
    def draw_sprite(self) -> (pygame.Surface, pygame.Rect):
        if self.sprite is not None:
            return self.sprite, self.get_rect()
        surface = pygame.Surface((16, 16))
        surface.fill((1, 1, 1, 1))
        return surface, self.get_rect()

    def distance_to(self, other) -> float:
        return ((self.row - other.row) ** 2 +
                (self.column - other.column) ** 2) ** .5

    # Converts a direction string into displacement
    @staticmethod
    def dir_to_disp(direction):
        row_displacement = 0
        column_displacement = 0

        if direction == "up":
            row_displacement = -1
        elif direction == "down":
            row_displacement = 1
        elif direction == "left":
            column_displacement = -1
        elif direction == "right":
            column_displacement = 1

        return row_displacement, column_displacement

    # Reverses the given direction
    @staticmethod
    def reverse(direction):
        if direction == "up":
            return "down"
        elif direction == "down":
            return "up"
        elif direction == "left":
            return "right"
        elif direction == "right":
            return "left"


# Contains all information about the player character in the game
class Player(MovingEntity):

    def __init__(self, grid, row=0, column=0):
        super().__init__(grid, row, column)
        self.speed = 4
        self.sprite = pygame.image.load("sprites/player.png")
        self.boomerang = None
        self.has_boomerang = True
        self.is_dead = False
        self.on_exit = False
        self.coin_count = 0
        self.throw_count = 0

    # Update movement and tiles
    def update(self, delta_time, step=64):
        if self.is_dead:
            return
        super().update(delta_time, step)
        self.update_with_tiles()
        if self.boomerang_in_air():
            self.boomerang.update(delta_time)

    # Updates active tiles such as spikes and switches
    def update_with_tiles(self):
        tiles = self.grid.active_tiles
        for tile in tiles:
            if "spikes" in tile.name:
                spikes = tile
                if spikes.is_armed and self.distance_to(spikes) < 0.5:
                    self.kill(None)
            elif "exit" in tile.name:
                if self.distance_to(tile) < 0.2 and self.has_boomerang:
                    self.on_exit = tile

    # Sets it moving in the needed direction
    def set_moving(self, direction, condition=True):
        super().set_moving(direction, condition)

    # Tries to move the player in a given direction, returns True if succeeds
    def move(self, direction, distance):

        row_disp, column_disp = MovingEntity.dir_to_disp(direction)
        adjacent_tile = round(self.row + row_disp / 2), \
                        round(self.column + column_disp / 2)

        # If it's empty, go there
        tile = self.grid.get_tile_at(*adjacent_tile)
        if "wall" not in tile.name:
            if row_disp != 0 or column_disp != 0:
                self.row += row_disp * distance
                self.column += column_disp * distance
                return True
        # Else stay where you are
        return False

    # Process user input
    def process_key_presses(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            condition = True
        elif event.type == pygame.KEYUP:
            condition = False
        else:
            return
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            self.set_moving("left", condition)
        if event.key == pygame.K_RIGHT or event.key == ord('d'):
            self.set_moving("right", condition)
        if event.key == pygame.K_UP or event.key == ord('w'):
            self.set_moving("up", condition)
        if event.key == pygame.K_DOWN or event.key == ord('s'):
            self.set_moving("down", condition)

    # Checks if the boomerang was thrown
    def boomerang_in_air(self):
        return self.boomerang is not None

    # Creates and throws the boomerang
    def throw_boomerang(self):
        # If doesn't have the boomerang, try to catch it
        if not self.has_boomerang and self.distance_to(self.boomerang) < 1.5:
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
            self.throw_count += 1
        else:
            return

    # Draws the player's sprite
    def draw_sprite(self) -> (pygame.Surface, pygame.Rect):
        # Turn the character over if it's dead
        if self.is_dead:
            return pygame.transform.rotate(self.sprite, 90), self.get_rect()
        return super().draw_sprite()

    # When hit by an enemy
    def kill(self, enemy):
        self.is_dead = True


class Boomerang(MovingEntity):

    # Initializes all the needed variables
    def __init__(self, grid, row=0, column=0):
        super().__init__(grid, row, column)
        self.sprite = pygame.image.load("sprites/boomerang.png")
        self.sprite45 = pygame.image.load("sprites/boomerang-45.png")
        self.speed = 7
        self.rotation = 0
        self.adjusting_trajectory = True

    # Updates the position based on speed
    def update(self, delta_time, step=32):
        if len(self.movement_directions) == 0:
            return
        last_dir = self.movement_directions[0]
        rounded_distance = (delta_time * self.speed * step) / step
        has_moved = self.move(last_dir, rounded_distance)
        if has_moved:
            self.adjust_trajectory(last_dir)
        next_tile, next_pos = self.get_next_tile(last_dir)
        if self.collides_with(next_tile, next_pos):
            # If it collided with something, reverse direction
            if "corner" in next_tile.name:
                new_dir = self.corner_bounce(last_dir, next_tile.name)
            else:
                new_dir = self.reverse(last_dir)
            self.set_moving(last_dir, False)
            self.set_moving(new_dir, True)
        self.update_with_tiles()

    # Updates active tiles such as spikes and switches
    def update_with_tiles(self):
        tiles = self.grid.active_tiles
        for tile in tiles:
            if "switch" in tile.name:
                switch = tile
                if self.distance_to(switch) < 0.1:
                    self.bounce()
                    switch.toggle()

    # Bounce the boomerang off an enemy
    def bounce(self):
        last_dir = self.movement_directions[0]
        new_dir = self.reverse(last_dir)
        self.set_moving(last_dir, False)
        self.set_moving(new_dir, True)

    # Bounce off a corner
    def corner_bounce(self, direction: str, corner_name: str):
        init_dir_letter = direction[0].upper()
        # If coming to a flat side, then reverse
        if init_dir_letter not in corner_name:
            return self.reverse(direction)
        # Else find the other direction to go
        else:
            new_dir_letter = corner_name.removeprefix("corner") \
                .replace(init_dir_letter, "")
            for direction in ["up", "down", "left", "right"]:
                if new_dir_letter.lower() in direction:
                    return self.reverse(direction)

    # Returns the next tile according to movement in this direction
    def get_next_tile(self, direction):
        row_disp, column_disp = MovingEntity.dir_to_disp(direction)
        adjacent_tile = round(self.row + row_disp / 2), \
                        round(self.column + column_disp / 2)
        return self.grid.get_tile_at(*adjacent_tile), adjacent_tile

    # Tries to move the player in a given direction, returns None if succeeds
    def move(self, direction, distance):

        row_disp, column_disp = MovingEntity.dir_to_disp(direction)
        next_tile, next_tile_pos = self.get_next_tile(direction)

        # If it's empty, go there
        if next_tile.name != "wall":
            if row_disp != 0 or column_disp != 0:
                self.row += row_disp * distance
                self.column += column_disp * distance
                return True
        # Else stay where you are
        return False

    # Redraws the player's sprite and returns it
    def draw_sprite(self) -> (pygame.Surface, pygame.Rect):
        # Calculate the angle of rotation (0, 45, 90, 135 etc.)
        angle_step = 45
        rounded_rotation = (self.rotation // angle_step) * angle_step
        sprite = self.sprite if rounded_rotation % 10 == 0 else self.sprite45
        rounded_rotation = (rounded_rotation // 90) * 90
        # Rotate and draw the sprite
        rotated_sprite = pygame.transform.rotate(sprite, rounded_rotation)
        rotated_rect = rotated_sprite.get_rect(center=self.get_rect().center)
        self.rotation += 5
        return rotated_sprite, rotated_rect

    # Checks for collision with a tile
    def collides_with(self, tile, tile_pos, position=None):
        if position is None:
            position = self.row, self.column
        my_row, my_column = position
        tile_row, tile_column = tile_pos
        # If it's a wall
        if "wall" in tile.name:
            if tile_row + 1 < my_row or tile_row > my_row + 1:
                return False
            if tile_column + 1 < my_column or tile_column > my_column + 1:
                return False
            return True
        # If it's a corner
        elif "corner" in tile.name:
            if len(self.movement_directions) != 0 and \
                    self.movement_directions[0][0].upper() not in tile.name:
                if tile_row + 1 < my_row or tile_row > my_row + 1:
                    return False
                if tile_column + 1 < my_column or tile_column > my_column + 1:
                    return False
                return True
            if abs(tile_row - my_row) < 0.1 and \
                    abs(tile_column - my_column) < 0.1:
                return True
        return False
