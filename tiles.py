"""
Mykyta S.
tiles.py

A module that contains classes for tiles that are located on the grid but
cannot move unlike entities. Active tiles can still update over time through
entity interaction (such as a switch activated by a boomerang).

Tile         -> Corner, ActiveTile
ActiveTile   -> Spikes, Switch, Exit
PARENT CLASS    SUBCLASSES
"""

import pygame


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
class Corner(Tile):
    corner_sprites = None

    # Loads the sprites into memory
    @staticmethod
    def load_sprites():
        if Corner.corner_sprites is not None:
            return Corner.corner_sprites
        Corner.corner_sprites = dict()
        for name in ["cornerUL", "cornerDL", "cornerUR", "cornerDR"]:
            Corner.corner_sprites[name] = pygame.image \
                .load("sprites/" + name + ".png")
        return Corner.corner_sprites

    # Draws the tile
    def draw(self, surface: pygame.Surface, rect: pygame.Rect):
        surface.blit(Corner.load_sprites()[self.name], rect)


# A method for active tiles
class ActiveTile(Tile):

    def __init__(self, name="wall"):
        super().__init__(name)
        self.grid = None
        self.row = -1
        self.column = -1
        self.is_active = True

    def set_coordinates(self, grid, row, column):
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
        if len(self.name.split(" ")) <= 1:
            return None
        return self.name.split(" ")[1]

    # Draws the tile
    def draw(self, surface: pygame.Surface, rect: pygame.Rect):
        # Use the regular sprite
        surface.blit(Exit.load_sprites()[0], rect)
