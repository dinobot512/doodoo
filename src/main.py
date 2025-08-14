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
    
    ASCII_8x8 = tileset.generateScaledTilesets(FC.ZOOM_SCALES,tileset.load_tileset("8x8_ascii.png",(8,8))) #8x8 font ascii tiles

    loadingTextRect = pygame.Rect(100,100,1600,700)
    debugTextbox = ui.textbox(loadingTextRect,"loading infos:",ASCII_8x8[1])

    CONFIG = RuntimeConfig()

    debugTextbox.string += f"loaded configs"
    debugTextbox.draw(display)
    pygame.display.update(loadingTextRect)
    print(f"loaded configs")

    if os.path.exists(FC.WORLD_FILENAME):
        debugTextbox.string += f"\nfound {FC.WORLD_FILENAME}, loading"
        debugTextbox.draw(display)
        pygame.display.update(loadingTextRect)
        print(f"found {FC.WORLD_FILENAME}, loading")

        PLAY_WORLD = World.loadWorld(FC.WORLD_FILENAME)
        if PLAY_WORLD is None:
            debugTextbox.string += f"\nunable to open {FC.WORLD_FILENAME}"
            debugTextbox.draw(display)
            pygame.display.update(loadingTextRect)
            print(f"unable to open {FC.WORLD_FILENAME}")
            quit()
    else:
        debugTextbox.string += f"\n{FC.WORLD_FILENAME} does not exist, generating world and saving to file"
        debugTextbox.draw(display)
        pygame.display.update(loadingTextRect)
        print(f"{FC.WORLD_FILENAME} does not exist, generating world and saving to file")
        PLAY_WORLD = World(
            FC.WORLD_WIDTH_cx,
            FC.WORLD_HEIGHT_cx,
            FC.WORLD_HEIGHT_cx,
            FC.CHUNKS_SIDE_LEN_ux
            )
        World.saveWorld(PLAY_WORLD,FC.WORLD_FILENAME)
        debugTextbox.string += f"\n{FC.WORLD_FILENAME} generated and saved"
        debugTextbox.draw(display)
        pygame.display.update(loadingTextRect)
        print(f"{FC.WORLD_FILENAME} generated and saved")

    debugTextbox.string += "\nbuilding user interface"
    debugTextbox.draw(display)
    pygame.display.update(loadingTextRect)
    print("building user interface")

    PLAY_RECT = pygame.Rect(FC.PLAY_AREA_TOPLEFT,FC.PLAY_AREA_DIMENSIONS) #designate play area
    
    debugTextbox.string += f"\nloading tileset {FC.PLAY_TILES_FILENAME}"
    debugTextbox.draw(display)
    pygame.display.update(loadingTextRect)
    print(f"loading tileset {FC.PLAY_TILES_FILENAME}")

    PLAY_TILES = tileset.generateScaledTilesets(FC.ZOOM_SCALES,tileset.load_tileset(FC.PLAY_TILES_FILENAME,FC.PLAY_TILES_DIMENSIONS))
    
    debugTextbox.string += "\ninitializing renderer"
    debugTextbox.draw(display)
    pygame.display.update(loadingTextRect)
    print("initializing renderer")

    RENDERER = renderer.Renderer(PLAY_RECT,PLAY_TILES,PLAY_WORLD,FC.ZOOM_SCALES)

    print("Keys in entity_index", PLAY_WORLD.entity_index.keys())
    if FC.PLAYER_ENTITY_NAME not in PLAY_WORLD.entity_index:
        debugTextbox.string += f"\nno player entity found"
        debugTextbox.draw(display)
        pygame.display.update(loadingTextRect)
        print(f"no player entity found")
        debugTextbox.string += f"\nplacing player entity at {FC.PLAYER_SPAWN_COORDS_ux}"
        debugTextbox.draw(display)
        pygame.display.update(loadingTextRect)
        print(f"placing player entity at {FC.PLAYER_SPAWN_COORDS_ux}")
        PLAYER_ENTITY = Entity(
            PLAY_WORLD,
            FC.PLAYER_ENTITY_NAME,
            CONFIG.PLAYER_ENTITY_TILE_ID,
            FC.PLAYER_SPAWN_COORDS_ux
            )
        World.saveWorld(PLAY_WORLD)
    else:
        PLAYER_ENTITY = PLAY_WORLD.entity_index[FC.PLAYER_ENTITY_NAME]
        debugTextbox.string += f"\nfound player entity at {PLAYER_ENTITY.coordinates_ux}"
        debugTextbox.draw(display)
        pygame.display.update(loadingTextRect)
        print(f"found player entity at {PLAYER_ENTITY.coordinates_ux}")

    debugTextbox.string += "\ninitializing input handler"
    debugTextbox.draw(display)
    pygame.display.update(loadingTextRect)
    print("initializing input handler")

    INPUT_HANDLER = input.InputHandler(PLAYER_ENTITY,PLAY_WORLD,RENDERER)
 
    debugTextbox.string += "\ndone! press any key"
    debugTextbox.draw(display)
    pygame.display.update(loadingTextRect)
    print(f"done! press any key")
    
    keyPressed = False
    while keyPressed == False:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keyPressed = True

    running = True
    updateRender = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                World.saveWorld(PLAY_WORLD)
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