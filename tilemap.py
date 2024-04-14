import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE

class Tile:
    def __init__(self, image_path, walkable):
        """
        Initialize a tile with its image and walkability.
        image_path: Path to the image file for the tile.
        walkable: Boolean indicating whether the tile can be walked on.
        """
        self.image = pygame.image.load(image_path)  # Load the image from the given path
        self.walkable = walkable  # Store whether the tile is walkable

class TileMap:
    def __init__(self, tile_size, map_data):
        """
        Initialize the tile map with specified tile size and map data.
        tile_size: The size of each tile in pixels.
        map_data: A 2D list representing the layout of the tiles.
        """
        self.tile_size = TILE_SIZE  # Size of each tile in pixels
        self.tiles = {
            'G': Tile('img/grass.png', True),
            'P': Tile('img/path.png', True),
            'W': Tile('img/water.png', False),
            'D': Tile('img/wall.png', False)
        }  # Dictionary mapping tile symbols to Tile objects
        self.map_data = map_data  # The layout of the map using characters to represent tiles

    def draw(self, screen, offset_x, offset_y):
        """
        Draw the tile map to the screen with given offsets.
        screen: The pygame surface to draw on.
        offset_x, offset_y: Offsets to apply to tile positions, used for camera movement.
        """
        for y, row in enumerate(self.map_data):
            for x, tile_char in enumerate(row):
                tile = self.tiles[tile_char]  # Retrieve the tile object based on character in map_data
                # Calculate the screen position to draw the tile
                screen.blit(tile.image, (x * self.tile_size + offset_x, y * self.tile_size + offset_y))

    def is_walkable(self, x, y):
        """
        Check if the tile at the specified pixel coordinates is walkable.
        x, y: Pixel coordinates to check.
        Returns True if the tile is walkable, otherwise False.
        """
        grid_x = x // self.tile_size  # Convert pixel x-coordinate to grid coordinate
        grid_y = y // self.tile_size  # Convert pixel y-coordinate to grid coordinate
        if 0 <= grid_x < len(self.map_data[0]) and 0 <= grid_y < len(self.map_data):
            tile_type = self.map_data[grid_y][grid_x]  # Get the tile type from map data
            return self.tiles[tile_type].walkable  # Return the walkability of the tile
        return False  # Assume non-walkable if outside the map bounds

class Camera:
    def __init__(self, width, height):
        """
        Initialize a camera with a specified width and height of the view.
        width, height: Dimensions of the camera's view in pixels.
        """
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        """
        Adjust the position of an entity to be relative to the camera.
        entity: The entity (usually a player or tile) to adjust.
        Returns the adjusted position as a new Rect.
        """
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        """
        Update the camera position to center on the target entity.
        target: The entity to center in the camera view.
        """
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)

        # Limit camera movement to within the bounds of the map
        x = min(0, x)  # Prevent the camera from moving past the left edge
        x = max(-(self.width - SCREEN_WIDTH), x)  # Prevent the camera from moving past the right edge
        y = min(0, y)  # Prevent the camera from moving past the top edge
        y = max(-(self.height - SCREEN_HEIGHT), y)  # Prevent the camera from moving past the bottom edge

        self.camera = pygame.Rect(x, y, self.width, self.height)
