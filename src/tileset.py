import os
import pygame

TILE_WIDTH, TILE_HEIGHT = 8, 8 #how big tiles are in pixels on the tileset image

def load_tileset(path="8x8_ascii.png",dims=(8,8)) -> list:
    tileset = pygame.image.load(os.path.join(os.path.dirname(__file__), path)).convert_alpha()
    tiles = [
        tileset.subsurface(pygame.Rect(x,y,dims[0],dims[1]))
        for y in range(0,tileset.get_height(),dims[1])
        for x in range(0,tileset.get_width(),dims[0])
    ]
    return tiles

def generateScaledTilesets(
        scaleRange: set[int],
        base_tileset: list[pygame.Surface]
) -> dict[int,list[pygame.Surface]]:
    scaled_sets = {}
    for scale in scaleRange:
        scaled_sets[scale] = [
            pygame.transform.scale_by(tile,scale)
            for tile in base_tileset
        ]
    return scaled_sets