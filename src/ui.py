import pygame

class textbox:
    def __init__(self,
                 bounds: pygame.rect,
                 content: str,
                 tileset: list[pygame.Surface],
                 ):
        self.string = content
        self.bounds_rect = bounds
        self.tileset = tileset
        self.surface = pygame.Surface(bounds.size, pygame.SRCALPHA)
        self._render_text()

    def _render_text(self):
        self.surface.fill((0,0,0,0))
        cursor_x, cursor_y = 0,0
        tile_w, tile_h = self.tileset[0].get_size()

        for char in self.string:
            if char == '\n':
                cursor_x = 0
                cursor_y += tile_h

            tile_index = ord(char) - 32
            if 0 <= tile_index < len(self.tileset):
                self.surface.blit(self.tileset[tile_index], (cursor_x,cursor_y))
                cursor_x += tile_w

    def draw(self, target_surface: pygame.Surface):
        self._render_text()
        target_surface.blit(self.surface,self.bounds_rect.topleft)
        return self.surface


