import pygame
from game import World

class Renderer:
    def __init__(
            self,
            boundsRect: pygame.Rect,
            tileDict: dict[list[pygame.Surface]],
            world: World,
            zoomScales: dict[int]
            ) -> None:
        self.bounds = boundsRect
        self.tilesets = tileDict
        self.world = world
        self.zoom_scales = zoomScales
        self.zoom = zoomScales[1]
        self.tileset = self.tilesets[self.zoom]
        self.debug_mode = False
        self.surface_cache = {} # Format: {(cx, cy, uz, zoom)}
        self.bad_surfaces = set()

    def _render_cell(
            self,
            coords_ux: tuple[int,int,int],
            ) -> pygame.Surface:
        cell = self.world.getCell(coords_ux)
        rSurface = self.tileset[cell.terrainID].copy()
        if len(cell.entities) > 0:
            topEntity = cell.entities[0]
            if self.debug_mode:
                print(f"rendering entity at {coords_ux}: {topEntity}")
            rSurface.blit(self.tileset[topEntity.tileID],(0,0))
        return rSurface


    def _render_single_chunk(
            self,
            x_cx: int,
            y_cx: int,
            z_ux: int,
            ) -> pygame.Surface:
        
        cache_key = (x_cx, y_cx, z_ux, self.zoom)
        modified_key = (x_cx, y_cx, z_ux // self.world.chunk_size_ux)
        chunkModified = False
        if modified_key in self.world.modified_chunks:
            chunkModified = True
        if (cache_key in self.surface_cache and chunkModified == False):
            return self.surface_cache[cache_key]
        worldChunkSize_ux = self.world.chunk_size_ux
        tileWidth_px = self.tileset[0].get_width()
        tileHeight_px = self.tileset[0].get_height()
        chunkWidth_px = worldChunkSize_ux*tileWidth_px
        chunkHeight_px = worldChunkSize_ux*tileHeight_px
        rSurface = pygame.Surface((chunkWidth_px,chunkHeight_px))
        for y in range(worldChunkSize_ux):
            for x in range(worldChunkSize_ux):
                tileCoords_px = (x*tileWidth_px,y*tileHeight_px)
                rSurface.blit(self._render_cell((x_cx*worldChunkSize_ux+x,y_cx*worldChunkSize_ux+y,z_ux)),tileCoords_px)
        if self.debug_mode:
            for x in range(worldChunkSize_ux):
                xCoord_px = x*tileWidth_px
                pygame.draw.line(rSurface,(255,0,255),(xCoord_px,0),(xCoord_px,rSurface.get_height()))
            for y in range(worldChunkSize_ux):
                yCoord_px = y*tileHeight_px
                pygame.draw.line(rSurface,(255,0,255),(0,yCoord_px),(rSurface.get_width(),yCoord_px))
        self.surface_cache[cache_key]
        return rSurface

    def _render_chunks(
            self,
            chunksWidthRange_chunks: range,
            chunksHeightRange_chunks: range,
            z_ux: int,
            ) -> pygame.Surface:
        
        """for cx, cy, uz in self.world.modified_chunks:
            for zoom in self.zoom_scales:
                cache_key = (cx, cy, uz, zoom)
                if cache_key in self.surface_cache:
                    del self.chunk_cache[cache_key]"""
                                         
                                         
        chunkWidth_px = self.tileset[0].get_width()*self.world.chunk_size_ux
        chunkHeight_px = self.tileset[0].get_width()*self.world.chunk_size_ux
        surfaceWidth_px = len(chunksWidthRange_chunks)*chunkWidth_px
        surfaceHeight_px = len(chunksHeightRange_chunks)*chunkHeight_px
        returnSurface = pygame.Surface((surfaceWidth_px,surfaceHeight_px))
        px,py = 0,0
        chunksRenderedString = ""
        for cy in chunksHeightRange_chunks:
            for cx in chunksWidthRange_chunks:
                chunk = self.world.chunks.get((cx, cy, z_ux // self.world.chunk_size_ux))
                if chunk:
                    intermediateSurface = self._render_single_chunk(cx,cy,z_ux)
                    returnSurface.blit(intermediateSurface, (px, py))
                    px += chunkWidth_px
                    chunksRenderedString += "#"
            px = 0
            py += chunkHeight_px
            chunksRenderedString += "\n"
        topleftChunkCoords_ux = (list(chunksWidthRange_chunks)[0],list(chunksHeightRange_chunks)[0])
        if self.debug_mode:
            print(f"rendered chunks (topleft: {topleftChunkCoords_ux}):\n{chunksRenderedString}")
        return returnSurface
    
    def decrementZoom(self):
         oldZoomScale = self.zoom
         self.zoom = max(self.zoom-1,min(self.zoom_scales))
         self.tileset = self.tilesets[self.zoom]
         if self.debug_mode:
            print(f"zoom changed from {oldZoomScale} to {self.zoom}")

    def incrementZoom(self):
         oldZoomScale = self.zoom
         self.zoom = min(self.zoom+1,max(self.zoom_scales))
         self.tileset = self.tilesets[self.zoom]
         if self.debug_mode:
            print(f"zoom changed from {oldZoomScale} to {self.zoom}")

    def toggleDebugMode(self):
        if self.debug_mode:
            self.debug_mode = False
        else:
            self.debug_mode = True
        print(f"grid overlay {self.debug_mode}")
    
    def render(
            self,
            coords: tuple[int, int, int],
            ) -> pygame.Surface:
        scaledTileset = self.tilesets[self.zoom]

        scaledTileWidth_px = scaledTileset[0].get_width()
        scaledTileHeight_px = scaledTileset[0].get_height()

        scaledChunkWidth_px = self.world.chunk_size_ux * scaledTileWidth_px
        scaledChunkHeight_px = self.world.chunk_size_ux * scaledTileHeight_px

        chunksWidth_cx = max(3,(self.bounds.w // scaledChunkWidth_px)+2)
        chunksHeight_cx = max(3,(self.bounds.h // scaledChunkHeight_px)+2)

        startChunkX_cx = max(0,coords[0] // self.world.chunk_size_ux - chunksWidth_cx // 2)
        startChunkY_cx = max(0,coords[1] // self.world.chunk_size_ux - chunksHeight_cx // 2)

        chunksWidthRange_cx = range(startChunkX_cx,chunksWidth_cx+startChunkX_cx)
        chunksHeightRange_cx = range(startChunkY_cx,chunksHeight_cx+startChunkY_cx)
        z_ux = coords[2]

        chunksSurface = self._render_chunks(chunksWidthRange_cx ,chunksHeightRange_cx,z_ux)

        playerX_px = (coords[0] - startChunkX_cx * self.world.chunk_size_ux)*scaledTileWidth_px
        playerY_px = (coords[1] - startChunkY_cx * self.world.chunk_size_ux)*scaledTileHeight_px

        xOffset_px = playerX_px - self.bounds.w // 2
        yOffset_px = playerY_px - self.bounds.h // 2

        centeredRect = pygame.Rect(max(0,xOffset_px),max(0,yOffset_px),self.bounds.w,self.bounds.h)
        clippedRect = centeredRect.clip(chunksSurface.get_rect())
        clippedSurface = chunksSurface.subsurface(clippedRect)
        blitOffset_px = (abs(min(0,xOffset_px)),abs(min(0,yOffset_px)))

        returnSurface = pygame.Surface(self.bounds.size)
        returnSurface.blit(clippedSurface,blitOffset_px)
        return returnSurface