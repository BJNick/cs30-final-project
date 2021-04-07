"""
Mykyta S.
enemies.py
A module for Enemy movement and AI
"""

import pygame
from player_character import MovingEntity


# Defines a simple enemy
class Enemy(MovingEntity):

    # Sets the required variables
    def __init__(self, grid, row=0, column=0):
        super().__init__(grid, row, column)
        self.sprite = pygame.image.load("sprites/enemy.png")
        self.speed = 2
        self.is_dead = False

    # Updates position and decision making
    def update(self, delta_time, step=64):
        if self.is_dead:
            return
        self.set_moving(None)
        # Move towards the player
        if self.grid.player.column + 0.5 < self.column:
            self.set_moving("left")
        elif self.grid.player.column - 0.5 > self.column:
            self.set_moving("right")
        elif self.grid.player.row + 0.5 < self.row:
            self.set_moving("up")
        elif self.grid.player.row - 0.5 > self.row:
            self.set_moving("down")
        # Die if hit by boomerang
        if not self.grid.player.has_boomerang:
            if self.distance_to(self.grid.player.boomerang) < 0.7:
                self.is_dead = True
                self.grid.player.boomerang.bounce()
                self.grid.coins.append(Coin(self.grid,
                                                 round(self.row),
                                                 round(self.column)))
                return
        # Kill the player on touch
        if self.distance_to(self.grid.player) < 0.7:
            self.grid.player.kill(self)
        # Update with active tiles
        self.update_with_tiles()
        super().update(delta_time, step)

    # Updates active tiles such as spikes
    def update_with_tiles(self):
        tiles = self.grid.active_tiles
        for tile in tiles:
            if "spikes" in tile.name:
                spikes = tile
                if spikes.is_armed and self.distance_to(spikes) < 0.5:
                    self.is_dead = True

    # Tries to move the player in a given direction, returns True if succeeds
    def move(self, direction, distance):

        row_disp, column_disp = MovingEntity.dir_to_disp(direction)
        adjacent_tile = round(self.row + row_disp / 2), \
                        round(self.column + column_disp / 2)

        # If it's empty, go there
        tile = self.grid.get_tile_at(*adjacent_tile)
        if "wall" not in tile.name:
            if "spikes" in tile.name and tile.is_armed:
                return False
            if row_disp != 0 or column_disp != 0:
                self.row += row_disp * distance
                self.column += column_disp * distance
                return True
        # Else stay where you are
        return False

    # Draws the enemy sprite
    def draw_sprite(self) -> (pygame.Surface, pygame.Rect):
        # Turn the character over if it's dead
        if self.is_dead:
            return pygame.transform.rotate(self.sprite, 90), self.get_rect()
        return super().draw_sprite()


class Coin(MovingEntity):

    # Initialize the coin
    def __init__(self, grid, row=0, column=0):
        super().__init__(grid, row, column)
        self.sprites = [pygame.image.load("sprites/coin_1.png"),
                        pygame.image.load("sprites/coin_2.png"),
                        pygame.image.load("sprites/coin_3.png"),
                        pygame.image.load("sprites/coin_4.png")]
        self.speed = 0
        self.animation_progress = 0
        self.animation_speed = 5
        self.is_picked_up = False

    def update(self, delta_time, step=64):
        if self.is_picked_up:
            return
        super().update(delta_time, step)
        self.animation_progress += delta_time * self.animation_speed
        # Add to score if touches player
        if self.distance_to(self.grid.player) < 0.7:
            self.is_picked_up = True
            self.grid.player.coin_count += 1

    # Draw the coin
    def draw_sprite(self) -> (pygame.Surface, pygame.Rect):
        if self.is_picked_up:
            return self.sprites[0], (-1000, -1000)
        return self.sprites[round(self.animation_progress) % 4], \
               self.get_rect()
