"""
Mykyta S.
enemies.py
A module for Enemy movement and AI
"""
import random

import pygame
from player_character import MovingEntity
import pathfinding


# Defines a simple enemy
class Enemy(MovingEntity):

    # Sets the required variables
    def __init__(self, grid, row=0, column=0):
        super().__init__(grid, row, column)
        self.sprite = pygame.image.load("sprites/enemy.png")
        self.speed = 2
        self.is_dead = False
        self.last_path = None
        self.last_path_self, self.last_path_player = None, None
        self.movement_goal = None
        self.waiting = 0

    # Updates position and decision making
    def update(self, delta_time, step=64):
        if self.is_dead:
            return
        self.set_moving(None)
        # Move towards the player
        self.update_path()
        self_pos = round(self.row), round(self.column)
        # Walk along the path or wander around aimlessly
        self.waiting -= delta_time
        if self.last_path and len(self.last_path) > 1:
            self.movement_goal = self.last_path[1].position
        # Wait or move to a random spot
        elif self.waiting <= 0 and (not self.movement_goal or
                self.distance_to(self, self.movement_goal) < 0.1):
            # Pick a random goal
            self.movement_goal = [(self_pos[0] + 1, self_pos[1]),
                                  (self_pos[0] - 1, self_pos[1]),
                                  (self_pos[0], self_pos[1] + 1),
                                  (self_pos[0], self_pos[1] - 1), *[None] * 2]\
                [random.randrange(6)]
            # If the goal is to wait, start the timer
            if not self.movement_goal:
                self.waiting = random.random() * 1
            elif not pathfinding.can_pass_through(self.grid,
                                                  self.movement_goal,
                                                  enemy=self,
                                                  avoid_spikes=True,
                                                  avoid_switches=True):
                self.movement_goal = None
        # Move towards the goal
        if self.movement_goal:
            if self.movement_goal[1] + 0.05 < self.column:
                self.set_moving("left")
            elif self.movement_goal[1] - 0.05 > self.column:
                self.set_moving("right")
            if self.movement_goal[0] + 0.05 < self.row:
                self.set_moving("up")
            elif self.movement_goal[0] - 0.05 > self.row:
                self.set_moving("down")
            self.last_path = self.last_path
        else:
            self.set_moving(None)
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

    # Updates the current saved path with new information
    def update_path(self, force_update=False):
        player_pos = round(self.grid.player.row), \
                     round(self.grid.player.column)
        self_pos = round(self.row), round(self.column)
        if force_update or not self.last_path_self or (
                self.last_path is not None and
                (self.last_path_self != self_pos or
                 self.last_path_player != player_pos)):
            self.last_path = pathfinding \
                .breadth_first_search(self.grid, self_pos, player_pos, self)
        self.last_path_player = player_pos
        self.last_path_self = self_pos

    # Updates active tiles such as spikes
    def update_with_tiles(self):
        tiles = self.grid.active_tiles
        for tile in tiles:
            if "spikes" in tile.name:
                spikes = tile
                if spikes.is_armed and self.distance_to(spikes) < 0.5:
                    self.is_dead = True
                    self.grid.coins.append(Coin(self.grid,
                                                round(self.row),
                                                round(self.column)))

    # Tries to move the player in a given direction, returns True if succeeds
    def move(self, direction, distance):

        row_disp, column_disp = MovingEntity.dir_to_disp(direction)
        adjacent_tile = round(self.row + row_disp / 2), \
                        round(self.column + column_disp / 2)

        # If it's not empty, stay
        tile = self.grid.get_tile_at(*adjacent_tile)
        if "wall" in tile.name:
            return False
        if "spikes" in tile.name and tile.is_armed:
            return False
        # Avoid other enemies
        new_position = (self.row + row_disp * distance,
                        self.column + column_disp * distance)
        for e in self.grid.enemies:
            if e is not self and not e.is_dead and \
                    self.distance_to(e, new_position) < 0.7:
                return False

        # If it's empty, go there
        if row_disp != 0 or column_disp != 0:
            self.row += row_disp * distance
            self.column += column_disp * distance
            return True

    # Draws the enemy sprite
    def draw_sprite(self) -> (pygame.Surface, pygame.Rect):
        # Turn the character over if it's dead
        if self.is_dead:
            return pygame.transform.rotate(self.sprite, 90), self.get_rect()
        return super().draw_sprite()


# Defines pick-up-able coins
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
