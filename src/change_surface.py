import pygame
import random

def recolor_surface(surface, old_color, new_color):
    """Replace all pixels of old_color with new_color"""
    pxarray = pygame.PixelArray(surface.copy())  # Create editable copy
    pxarray.replace(old_color, new_color, distance=0.0)  # Exact color match
    return pxarray.surface  # Return new surface

def random_tile_fill(surface,bounds_rect,tiles_array,zoom,tile_height,tile_width): # practice for renderer (bad btw)
    rSurface = pygame.Surface((bounds_rect.w, bounds_rect.h)) #create a surface the size of bounds rectangle
    scaled_tile_height, scaled_tile_width = tile_height * zoom, tile_width * zoom #actual dimensions
    for y in range(0, bounds_rect.h-(scaled_tile_height) +1, scaled_tile_height):
            for x in range(0, bounds_rect.w -(scaled_tile_width)+1, scaled_tile_width):
                random_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255)) #generate a random color
                rSurface.blit(recolor_surface(pygame.transform.scale_by(tiles_array[random.randint(0,len(tiles_array)-1)], zoom),(255,255,255),random_color), (x, y))#paste one tile
    surface.blit(rSurface,(bounds_rect.topleft)) #paste the now filled surface onto initial surface   