from __future__ import annotations
import pygame
import random
from typing import Dict
import pickle 
import gzip
    
class World:
    WIDTH_CHUNKS = 8
    HEIGHT_CHUNKS = 8
    DEPTH_CHUNKS = 8
    CHUNK_SIZE_UX = 16

    def __init__(self):
        self.chunks: Dict[tuple, Chunk] = {}
        self.entity_index = {}
        self._init_empty_world()
        self.modified_chunks = set() # Format: {(cx, cy, uz)} uz and cz are the same because chunk depth is 1

    @staticmethod
    def uxToCX(coords_ux: tuple[int, int, int]):
        coords_cx = (coords_ux[0]//World.CHUNK_SIZE_UX, coords_ux[1]//World.CHUNK_SIZE_UX, coords_ux[2])
        return coords_cx

    def markParentChunkModified(self, coords_ux: tuple[int, int, int]):
        coords_cx = self.uxToCX(coords_ux)
        self.modified_chunks.add(coords_cx)

    def markChunkCorrected(self, coords_cx: tuple[int,int,int]):
        if coords_cx in self.modified_chunks:
            self.modified_chunks.remove(coords_cx)

    def _init_empty_world(self) -> None:      
        for cx in range(World.WIDTH_CHUNKS):
            for cy in range(World.HEIGHT_CHUNKS):
                for cz in range(World.DEPTH_CHUNKS):
                    self.chunks[(cx, cy, cz)] = Chunk(World.CHUNK_SIZE_UX) # fill chunks[] with a chunk

    def save(self, filename="world.dat"):
        with gzip.open(filename, "wb") as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"{filename} saved")

    def load(filename="world.dat"):
        try:
            with gzip.open(filename, 'rb') as f:
                print(f"{filename} loaded")
                return pickle.load(f)
        except (EOFError, pickle.UnpicklingError):
            print(f"unable to open {filename}")
            return None
        
    def getChunkFromCX(self,coords_cx: tuple[int, int, int]):
        if self.chunks.get(coords_cx):
            return self.chunks.get(coords_cx)
        return None
            
    def getChunkFromUX(self,coords_ux: tuple[int, int, int]) -> Chunk:
        coords_cx = self.uxToCX(coords_ux)
        return self.getChunkFromCX(coords_cx)

    def getCell(self,coords_ux: tuple[int, int, int]) -> Cell:
        chunk = self.getChunkFromUX(coords_ux)
        if chunk is None:
            return None
        elif chunk.getCell(coords_ux):
            return chunk.getCell(coords_ux)
        return None

class Cell:
    def __init__(self, terrainID=1,passable=True):
        self.entities = [] #cell has list of entities
        self.terrainID  = terrainID
        self.passable = passable

class Chunk:
    def __init__(self):
        self.cells = [[[Cell(random.randint(1, 2), True) for z in range(World.CHUNK_SIZE_UX)]
                       for y in range(World.CHUNK_SIZE_UX)]
                       for x in range(World.CHUNK_SIZE_UX)]

    def getCell(self,coords_ux: tuple[int, int, int]) -> Cell:
        x, y, z = (coord % World.CHUNK_SIZE_UX for coord in coords_ux)
        if self.cells[x][y][z]:
            return self.cells[x][y][z]
        return None
    
    def __repr__(self):
        return f"{World.CHUNK_SIZE_UX}^3 volume chunk at --,--,--"
    
class Entity:
    def __init__(self,world: World, name = "Unnamed Entity",tileID = 3,coords_ux = None):
        self.coordinates_ux = None
        self.world = world
        self.tileID = tileID
        self.name = name
        self.world.entity_index[self.name] = self
        self.setPosition(coords_ux)

    def setPosition(self,newCoords_ux: tuple[int, int, int]) -> int:
        newCell = self.world.getCell(newCoords_ux)
        if(newCell is None):
            print(f"{self.name} tried to move out of bounds             ( {self.coordinates_ux} -/> {newCoords_ux} )")
        elif(newCell.passable == False):
            print(f"{self.name} tried to move into an impassable cell   ( {self.coordinates_ux} -/> {newCoords_ux} )")
        elif(self.coordinates_ux == newCoords_ux):
            print(f"{self.name} stayed still                            ( {self.coordinates_ux}  =  {newCoords_ux} )")
        elif(self.coordinates_ux is None):
            self._add_to_cell(newCoords_ux)
            print(f"{self.name} spawned                                 ( {self.coordinates_ux} )")
        else:
            oldCoords_ux = self.coordinates_ux
            self._remove_from_cell(oldCoords_ux)
            self._add_to_cell(newCoords_ux)
            print(f"{self.name} moved                                   ( {oldCoords_ux} --> {self.coordinates_ux} )")

    def _add_to_cell(self,coords_ux):
        cell = self.world.getCell(coords_ux)
        if self not in cell.entities:
            cell.entities.append(self)
            self.coordinates_ux = coords_ux
            self.world.markParentChunkModified(coords_ux)

    def _remove_from_cell(self,coords_ux):
        cell = self.world.getCell(coords_ux)
        if self in cell.entities:
            cell.entities.remove(self)
            self.coordinates_ux = None
            self.world.markParentChunkModified(coords_ux)

    def move(self,magnitudeX_ux,magnitudeY_ux,magnitudeZ_ux):
        self.setPosition([
            self.coordinates_ux[0] + magnitudeX_ux,
            self.coordinates_ux[1] + magnitudeY_ux,
            self.coordinates_ux[2] + magnitudeZ_ux
        ])

    def __repr__(self):
        return f"<{self.name} at {self.coordinates_ux}>"

