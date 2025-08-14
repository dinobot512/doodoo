import pygame
from game import World
from dataclasses import dataclass
from enum import Enum

class RCode(Enum): #R is short for render
    SUCCESS = 0
    ERROR = 1
    CACHE_HIT = 2

    def __str__(self):
        messages = {
            RCode.SUCCESS:     "successfully rendered",
            RCode.ERROR:       "failed render",
            RCode.CACHE_HIT:   "used cached surface"
        }
        return messages[self]

@dataclass
class RResult:
    surface: pygame.Surface
    code: RCode

    def __str__(self):
        return f"{self.code} (Code: {self.code.value})"

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
        self.good_surfaces = {} # Format: {(cx, cy, uz, zoom)}

    def _render_cell(
            self,
            coords_ux: tuple[int,int,int],
            ) -> RResult:
        cell = self.world.getCell(coords_ux)
        rSurface = self.tileset[cell.terrainID].copy()
        if len(cell.entities) > 0:
            topEntity = cell.entities[0]
            if self.debug_mode:
                print(f"rendering entity at {coords_ux}: {topEntity}")
            rSurface.blit(self.tileset[topEntity.tileID],(0,0))
        return RResult(rSurface,RCode.SUCCESS)


    def _render_single_chunk(
            self,
            chunk_cx: tuple[int,int,int]
            ) -> RResult:

        x_cx, y_cx, z_ux = chunk_cx[0], chunk_cx[1], chunk_cx[2]

        cache_key = (x_cx, y_cx, z_ux, self.zoom)
        modified_key = (x_cx, y_cx, z_ux)

        if (cache_key in self.good_surfaces and modified_key not in self.world.modified_chunks):
            rSurface = self.good_surfaces[cache_key]
            return RResult(rSurface,RCode.CACHE_HIT)

        worldChunkSize_ux = self.world.chunk_size_ux
        tileWidth_px = self.tileset[0].get_width()
        tileHeight_px = self.tileset[0].get_height()
        chunkWidth_px = worldChunkSize_ux*tileWidth_px
        chunkHeight_px = worldChunkSize_ux*tileHeight_px

        rSurface = pygame.Surface((chunkWidth_px,chunkHeight_px))

        for y in range(worldChunkSize_ux):
            for x in range(worldChunkSize_ux):
                tileCoords_px = (x*tileWidth_px,y*tileHeight_px)
                cellCoords_ux = (x_cx*worldChunkSize_ux+x,y_cx*worldChunkSize_ux+y,z_ux)
                cellRender = self._render_cell(cellCoords_ux)
                rSurface.blit(cellRender.surface,tileCoords_px)

        if self.debug_mode:
            for x in range(worldChunkSize_ux):
                if x == 0: borderColor = (255,0,255)
                else: borderColor = (128,128,128)
                xCoord_px = x*tileWidth_px
                pygame.draw.line(rSurface,borderColor,(xCoord_px,0),(xCoord_px,rSurface.get_height()))
            for y in range(worldChunkSize_ux):
                if y == 0: borderColor = (255,0,255)
                else: borderColor = (128,128,128)
                yCoord_px = y*tileHeight_px
                pygame.draw.line(rSurface,borderColor,(0,yCoord_px),(rSurface.get_width(),yCoord_px))

        self.good_surfaces[cache_key] = rSurface
        self.world.markChunkCorrected(modified_key)
        return RResult(rSurface,RCode.SUCCESS)

    def _render_chunks(
            self,
            chunksWidthRange_chunks: range,
            chunksHeightRange_chunks: range,
            z_ux: int,
            ) -> RResult:

        for cx, cy, uz in self.world.modified_chunks:
            for zoom in self.zoom_scales:
                cache_key = (cx, cy, uz, zoom)
                if cache_key in self.good_surfaces:
                    del self.good_surfaces[cache_key]
                                                           
        chunkWidth_px = self.tileset[0].get_width()*self.world.chunk_size_ux
        chunkHeight_px = self.tileset[0].get_width()*self.world.chunk_size_ux
        surfaceWidth_px = len(chunksWidthRange_chunks)*chunkWidth_px
        surfaceHeight_px = len(chunksHeightRange_chunks)*chunkHeight_px
        rSurface = pygame.Surface((surfaceWidth_px,surfaceHeight_px))

        if self.debug_mode:
            chunksRenderedString = ""
            chunksRendered = 0
            chunkCacheHits = 0
        px,py = 0,0
        for cy in chunksHeightRange_chunks:
            for cx in chunksWidthRange_chunks:
                chunk = self.world.chunks.get((cx, cy, z_ux // self.world.chunk_size_ux))
                if chunk:
                    chunk_cx = (cx,cy,z_ux)
                    chunkRender = self._render_single_chunk(chunk_cx)
                    rSurface.blit(chunkRender.surface, (px, py))
                px += chunkWidth_px

                if chunk and self.debug_mode and chunkRender.code == RCode.SUCCESS:
                    chunksRenderedString += "R"
                    chunksRendered += 1
                elif chunk and self.debug_mode and chunkRender.code == RCode.CACHE_HIT:
                    chunksRenderedString += "C"
                    chunkCacheHits += 1
                elif self.debug_mode:
                    chunksRenderedString += "X"
            px = 0
            py += chunkHeight_px

            if self.debug_mode:
                chunksRenderedString += "\n"

        if self.debug_mode:
            topleftChunkCoords_ux = (list(chunksWidthRange_chunks)[0],list(chunksHeightRange_chunks)[0])
            print(f"rendered chunks (topleft: {topleftChunkCoords_ux}):\n{chunksRenderedString}\nchunks rendered: {chunksRendered}\nsurfaces reused: {chunkCacheHits}")

        return RResult(rSurface,RCode.SUCCESS)
    
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
        self.good_surfaces.clear()
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

        chunksWidth_cx = max(3,(self.bounds.w // scaledChunkWidth_px))
        chunksHeight_cx = max(3,(self.bounds.h // scaledChunkHeight_px))

        startChunkX_cx = max(0,coords[0] // self.world.chunk_size_ux - chunksWidth_cx // 2)
        startChunkY_cx = max(0,coords[1] // self.world.chunk_size_ux - chunksHeight_cx // 2)

        chunksWidthRange_cx = range(startChunkX_cx,chunksWidth_cx+startChunkX_cx)
        chunksHeightRange_cx = range(startChunkY_cx,chunksHeight_cx+startChunkY_cx)
        z_ux = coords[2]

        chunksSurface = self._render_chunks(chunksWidthRange_cx ,chunksHeightRange_cx,z_ux).surface

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