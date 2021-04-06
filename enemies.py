"""
Mykyta S.
enemies.py
A module for Enemy movement and AI
"""

import pygame
from grid_world import Grid, Tile
from player_character import Player, MovingEntity


# Defines a simple enemy
class Enemy(MovingEntity):

    # Sets the required variables
    def __init__(self, grid: Grid, player: Player, row=0, column=0):
        super().__init__(grid, row, column)
        self.sprite = pygame.image.load("sprites/enemy.png")
        self.speed = 2
        self.boomerang = None
        self.has_boomerang = True
        self.player = player
        self.is_dead = False

    # Updates position and decision making
    def update(self, delta_time, step=64):
        if self.is_dead:
            return
        self.set_moving(None)
        # Move towards the player
        if self.player.column + 0.5 < self.column:
            self.set_moving("left")
        elif self.player.column - 0.5 > self.column:
            self.set_moving("right")
        elif self.player.row + 0.5 < self.row:
            self.set_moving("up")
        elif self.player.row - 0.5 > self.row:
            self.set_moving("down")
        # Die if hit by boomerang
        if not self.player.has_boomerang:
            if self.distance_to(self.player.boomerang) < 0.7:
                self.is_dead = True
                return
        # Kill the player on touch
        if self.distance_to(self.player) < 0.7:
            self.player.kill(self)
        super().update(delta_time, step)


    # Tries to move the player in a given direction, returns True if succeeds
    def move(self, direction, distance):

        row_disp, column_disp = MovingEntity.dir_to_disp(direction)
        adjacent_tile = round(self.row + row_disp / 2), \
                        round(self.column + column_disp / 2)

        # If it's empty, go there
        if self.grid.is_open_space(*adjacent_tile):
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
