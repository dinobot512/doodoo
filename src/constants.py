from dataclasses import dataclass

@dataclass (frozen=True)
class FrozenConstants:
    # Display
    DISPLAY_DIMENSIONS: tuple[int,int] = (800,600)

    # Input
    KEY_REPEAT_DELAY: int = 500 # in milliseconds
    KEY_REPEAT_INTERVAL: int = 100 # in ms

    # UI
    PLAY_AREA_TOPLEFT: tuple[int,int] = 50,50 # in px
    PLAY_AREA_DIMENSIONS: tuple[int,int] = (
        DISPLAY_DIMENSIONS[0] - PLAY_AREA_TOPLEFT[0] * 2,
        DISPLAY_DIMENSIONS[1] - PLAY_AREA_TOPLEFT[1] * 2
        )
    PLAY_TILES_FILENAME: str = "16x16_tiles.png"
    PLAY_TILES_DIMENSIONS: tuple[int,int] = (16,16) # in px

    # Zoom
    ZOOM_SCALES = [1,2,3,4,5,6,7,8] #zoom ordered list

    # World
    WORLD_FILENAME: str = "world.dat"
    WORLD_WIDTH_cx: int = 8
    WORLD_HEIGHT_cx: int = 8 
    WORLD_DEPTH_ux: int = 8
    CHUNKS_SIDE_LEN_ux: int = 16

    # Player
    PLAYER_ENTITY_NAME: str = "Player Entity"
    PLAYER_SPAWN_COORDS_ux: tuple[int,int,int] = (
        WORLD_WIDTH_cx*CHUNKS_SIDE_LEN_ux//2,
        WORLD_HEIGHT_cx*CHUNKS_SIDE_LEN_ux//2,
        0
        )

@dataclass
class RuntimeConfig:
    PLAYER_ENTITY_TILE_ID: int  = 3