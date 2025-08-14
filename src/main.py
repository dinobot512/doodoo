import pygame, os, time, random
from game import World, Entity
import tileset, renderer, input, ui, change_surface
from constants import FrozenConstants as FC
from constants import RuntimeConfig


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    #get this scripts path, turn it absolute(from root) get the name of the directory its in and make that the working directory (/projectName/src)

    pygame.init()
    pygame.key.set_repeat(FC.KEY_REPEAT_DELAY,FC.KEY_REPEAT_INTERVAL)

    display = pygame.display.set_mode(FC.DISPLAY_DIMENSIONS) #make window with following dimensions
    pygame.display.set_caption("doodoo") #call window this
    
    #ASCII_8x8 = tileset.generateScaledTilesets(FC.ZOOM_SCALES,tileset.load_tileset("8x8_ascii.png",(8,8))) #8x8 font ascii tiles

    CONFIG = RuntimeConfig()
    print(f"loaded configs")

    if os.path.exists(FC.WORLD_FILENAME):
        print(f"found {FC.WORLD_FILENAME}, loading")
        PLAY_WORLD = World.load(FC.WORLD_FILENAME)
        if PLAY_WORLD is None:
            print(f"unable to open {FC.WORLD_FILENAME}")
            quit()
    else:
        print(f"{FC.WORLD_FILENAME} does not exist")
        PLAY_WORLD = World(
            FC.WORLD_WIDTH_cx,
            FC.WORLD_HEIGHT_cx,
            FC.WORLD_HEIGHT_cx,
            FC.CHUNKS_SIDE_LEN_ux
            )
        World.save(PLAY_WORLD,FC.WORLD_FILENAME)
        print(f"{FC.WORLD_FILENAME} generated and saved")

    PLAY_RECT = pygame.Rect(FC.PLAY_AREA_TOPLEFT,FC.PLAY_AREA_DIMENSIONS) #designate play area
    print("built user interface")
    
    PLAY_TILES = tileset.generateScaledTilesets(FC.ZOOM_SCALES,tileset.load_tileset(FC.PLAY_TILES_FILENAME,FC.PLAY_TILES_DIMENSIONS))
    print(f"loaded tileset {FC.PLAY_TILES_FILENAME}")

    RENDERER = renderer.Renderer(PLAY_RECT,PLAY_TILES,PLAY_WORLD,FC.ZOOM_SCALES)
    print("initialized renderer")

    if FC.PLAYER_ENTITY_NAME not in PLAY_WORLD.entity_index:
        print("no player entity found")
        PLAYER_ENTITY = Entity(
            PLAY_WORLD,
            FC.PLAYER_ENTITY_NAME,
            CONFIG.PLAYER_ENTITY_TILE_ID,
            FC.PLAYER_SPAWN_COORDS_ux
            )
        World.save(PLAY_WORLD)
    else:
        PLAYER_ENTITY = PLAY_WORLD.entity_index[FC.PLAYER_ENTITY_NAME]
        print(f"found player entity at {PLAYER_ENTITY.coordinates_ux}")

    INPUT_HANDLER = input.InputHandler(PLAYER_ENTITY,PLAY_WORLD,RENDERER)
    print("initialized input handler")

    running = True
    updateRender = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                World.save(PLAY_WORLD)
            if event.type == pygame.KEYDOWN:
                updateRender = INPUT_HANDLER.handleKeydown(event.key)

        if updateRender:
            display.fill((0,0,0),PLAY_RECT)
            display.blit(RENDERER.render(PLAYER_ENTITY.coordinates_ux),PLAY_RECT)
            pygame.display.flip()
            updateRender = False
        
    pygame.quit()

if __name__ == "__main__":
     main()