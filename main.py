"""
Mykyta S.
main.py
The main class of this application
"""

import sys
import pygame
import time
# Import my own module
import grid_world


if __name__ == "__main__":

    pygame.init()
    size = width, height = 640, 640
    black = (0, 0, 0)

    # Initialize variables
    screen = pygame.display.set_mode(size)

    grid = grid_world.Grid(64)
    player = grid_world.Player(grid, 2, 2)

    while True:
        for event in pygame.event.get():
            # Exit when quit button is pressed
            if event.type == pygame.QUIT:
                sys.exit()
            # Process the key down presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    player.set_moving("left", True)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    player.set_moving("right", True)
                if event.key == pygame.K_UP or event.key == ord('w'):
                    player.set_moving("up", True)
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    player.set_moving("down", True)
                # Throw the boomerang on space bar
                if event.key == pygame.K_SPACE:
                    player.throw_boomerang()
            # Process the key up events
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    player.set_moving("left", False)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    player.set_moving("right", False)
                if event.key == pygame.K_UP or event.key == ord('w'):
                    player.set_moving("up", False)
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    player.set_moving("down", False)
        # Update positions
        player.update(0.01)
        if player.boomerang_in_air():
            player.boomerang.update(0.01)
        # Draw everything on the screen
        screen.fill(black)
        screen.blit(grid.draw_grid(), screen.get_rect())
        screen.blit(player.draw_sprite(), player.get_rect())
        if player.boomerang_in_air():
            screen.blit(player.boomerang.draw_sprite(),
                        player.boomerang.get_rect())
        pygame.display.flip()
        time.sleep(0.01)
