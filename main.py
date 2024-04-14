import pygame
import sys
from player import Player
from tilemap import TileMap, Camera
from config import SCREEN_WIDTH, SCREEN_HEIGHT

# Initialize the Pygame library
pygame.init()

# Set up the display window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hero's Adventure Game")  # Set the window title

# Define the map data structure
# 'G' for grass, 'D' for wall, 'W' for water, 'P' for path
map_data = [['G' for _ in range(50)] for _ in range(50)]
# Define walls on the perimeter of the map
for i in range(50):
    map_data[0][i] = 'D'
    map_data[49][i] = 'D'
    map_data[i][0] = 'D'
    map_data[i][49] = 'D'
# Define a water area
for y in range(10, 15):
    for x in range(10, 15):
        map_data[y][x] = 'W'
# Define paths that cross in the middle of the map
for i in range(50):
    map_data[i][24] = 'P'
    map_data[24][i] = 'P'

# Create a TileMap object with a tile size of 50 pixels
tile_map = TileMap(50, map_data)

# Create a player object positioned at the center of the screen
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, tile_map)

# Initialize the camera with the size of the entire tilemap
camera = Camera(2500, 2500)  # Assuming your tiles are 50x50 pixels and the map is 50 tiles wide

# Initialize a clock for managing frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Compute delta time in seconds

    # Event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Respond to key presses for player movement
            if event.key == pygame.K_w:
                player.move_up()
            elif event.key == pygame.K_s:
                player.move_down()
            elif event.key == pygame.K_a:
                player.move_left()
            elif event.key == pygame.K_d:
                player.move_right()
        elif event.type == pygame.KEYUP:
            # Respond to key releases to stop the player
            if event.key in [pygame.K_w, pygame.K_s]:
                player.stop_y()
            if event.key in [pygame.K_a, pygame.K_d]:
                player.stop_x()

    # Update player's position based on current velocity and collisions
    player.update(dt)
    # Update the camera to center on the player
    camera.update(player)

    # Clear the screen with black color
    screen.fill((0, 0, 0))

    # Draw the tile map adjusted for camera position
    tile_map.draw(screen, camera.camera.x, camera.camera.y)
    # Draw the player adjusted for camera position
    screen.blit(player.image, camera.apply(player))

    # Refresh the screen
    pygame.display.flip()

# Quit Pygame when the main loop ends
pygame.quit()
sys.exit()
