import pygame
from config import PLAYER_SPEED

class Player:
    def __init__(self, x, y, tile_map, size=(50, 50)):
        """
        Initialize the player with position, image, and reference to the tile map.
        x, y: Initial position coordinates of the player on the screen.
        tile_map: Reference to the TileMap object for collision detection.
        size: Tuple indicating the width and height of the player image.
        """
        # Load and scale the player image to the specified size
        self.image = pygame.image.load('img/player.png')
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Movement speed and velocity
        self.speed = PLAYER_SPEED
        self.vel_x = 0
        self.vel_y = 0

        # Reference to the tile map for checking walkable areas
        self.tile_map = tile_map

    def draw(self, screen):
        """
        Draw the player on the screen.
        screen: The pygame surface on which to draw the player.
        """
        screen.blit(self.image, self.rect)

    def update(self, dt):
        """
        Update the player's position based on velocity and check for collisions.
        dt: Delta time, or the amount of time passed since the last frame.
        """
        # Calculate potential new position
        new_x = int(self.rect.x + self.vel_x * dt)
        new_y = int(self.rect.y + self.vel_y * dt)

        # Calculate the center of the new position for collision checking
        center_x = new_x + self.rect.width // 2
        center_y = new_y + self.rect.height // 2

        # Check if the new position is walkable before updating coordinates
        if self.tile_map.is_walkable(center_x, center_y):
            self.rect.x = new_x
            self.rect.y = new_y
        else:
            # Stop movement if the new position hits a non-walkable tile
            self.stop_x()
            self.stop_y()

    def move_up(self):
        """
        Set the vertical velocity to move up.
        """
        self.vel_y = -self.speed

    def move_down(self):
        """
        Set the vertical velocity to move down.
        """
        self.vel_y = self.speed

    def move_left(self):
        """
        Set the horizontal velocity to move left.
        """
        self.vel_x = -self.speed

    def move_right(self):
        """
        Set the horizontal velocity to move right.
        """
        self.vel_x = self.speed

    def stop_x(self):
        """
        Stop horizontal movement by setting horizontal velocity to zero.
        """
        self.vel_x = 0

    def stop_y(self):
        """
        Stop vertical movement by setting vertical velocity to zero.
        """
        self.vel_y = 0
