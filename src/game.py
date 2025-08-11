from __future__ import annotations
import pygame
import random
from typing import Dict
import pickle 
import gzip
    
class World:
    def __init__(self, width_chunks=8,height_chunks=8,depth_chunks=1,chunk_size_ux=16):
        self.dimensions_chunks = (width_chunks, height_chunks, depth_chunks)
        self.dimensions_ux = (width_chunks*chunk_size_ux,height_chunks*chunk_size_ux,depth_chunks*chunk_size_ux)
        self.width_chunks = width_chunks
        self.height_chunks = height_chunks
        self.depth_chunks = depth_chunks
        self.chunk_size_ux = chunk_size_ux
        self.chunks: Dict[tuple, Chunk] = {}
        self.entity_index = {}
        self._init_empty_world()
        self.modified_chunks = set()

    def markChunkModified(self, coords_cx: tuple[int, int, int]):
        self.modified_chunks.add(coords_cx)

    def _init_empty_world(self) -> None:      
        for cx in range(self.width_chunks):
            for cy in range(self.height_chunks):
                for cz in range(self.depth_chunks):
                    self.chunks[(cx, cy, cz)] = Chunk(self.chunk_size_ux) # fill chunks[] with a chunk

    def saveWorld(world, filename="world.dat"):
        with gzip.open(filename, "wb") as f:
            pickle.dump(world, f, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"{filename} saved")

    def loadWorld(filename="world.dat"):
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
        cx, cy, cz = (coord // self.chunk_size_ux for coord in coords_ux)
        return self.getChunkFromCX((cx, cy, cz))

    def getCell(self,coords_ux: tuple[int, int, int]) -> Cell:
        chunk = self.getChunkFromUX(coords_ux)
        if chunk == None:
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
    def __init__(self, sideLength_ux):
        self.sideLength_ux = sideLength_ux
        self.cells = [[[Cell(random.randint(1, 2), True) for z in range(sideLength_ux)]
                       for y in range(sideLength_ux)]
                       for x in range(sideLength_ux)]

    def getCell(self,coords_ux: tuple[int, int, int]) -> Cell:
        x, y, z = (coord % self.sideLength_ux for coord in coords_ux)
        if self.cells[x][y][z]:
            return self.cells[x][y][z]
        return None
    
    def __repr__(self):
        return f"{self.sideLength_ux}^3 volume chunk at --,--,--"
    
class Entity:
    def __init__(self,world: World, name = "Unnamed Entity",tileID = 3,coords_ux = (0,0,0)):
        self.coordinates_ux = coords_ux
        self.world = world
        self.tileID = tileID
        self.name = name
        self.world.entity_index[self.name] = self
        self.setPosition(coords_ux)

    def setPosition(self,newCoords_ux: tuple[int, int, int]):
        newCell = self.world.getCell(newCoords_ux)
        if(newCell == None):
            print(f"{self.name} tried to move out of bounds")
        elif(newCell.passable == False):
            print(f"{self.name} tried to move into an impassable cell at {newCoords_ux}")
        elif(self.coordinates_ux == newCoords_ux):
            print(f"{self.name} stayed still at {newCoords_ux}")
        else:
            oldCell = self.world.getCell(self.coordinates_ux)
            if self in oldCell.entities:
                oldCell.entities.remove(self)
            newCell.entities.insert(0,self)
            oldCoordinates = self.coordinates_ux
            self.coordinates_ux = newCoords_ux
            print(f"{self.name} moved from {oldCoordinates} to {self.coordinates_ux}")

    def move(self,magnitudeX_ux,magnitudeY_ux,magnitudeZ_ux):
        self.setPosition([
            self.coordinates_ux[0] + magnitudeX_ux,
            self.coordinates_ux[1] + magnitudeY_ux,
            self.coordinates_ux[2] + magnitudeZ_ux
        ])

    def __repr__(self):
        return f"<{self.name} at {self.coordinates_ux}>"

