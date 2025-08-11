import pygame, os, time, random
from game import World, Entity
import tileset, renderer, input, ui, change_surface


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    #get this scripts path, turn it absolute(from root) get the name of the directory its in and make that the working directory (/projectName/src)

    pygame.init()
    pygame.key.set_repeat(500,100)

    DISPLAY_WIDTH, DISPLAY_HEIGHT = 1800, 900
    display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT)) #make window with following dimensions
    pygame.display.set_caption("doodoo") #call window this
    ZOOM_SCALES = [1,2,3,4,5,6,7,8] #zoom ordered list

    ASCII_8x8 = tileset.generateScaledTilesets(ZOOM_SCALES,tileset.load_tileset("8x8_ascii.png",(8,8))) #8x8 font ascii tiles

    loadingTextRect = pygame.Rect(100,100,1600,700)
    debugTextbox = ui.textbox(loadingTextRect,"loading infos:",ASCII_8x8[2])

    WORLD_FILENAME = "world.dat"
    if os.path.exists(WORLD_FILENAME):
        debugTextbox.string += f"\nfound {WORLD_FILENAME}, loading"
        debugTextbox.draw(display)
        pygame.display.update(loadingTextRect)
        print(f"found {WORLD_FILENAME}, loading")

        PLAY_WORLD = World.loadWorld(WORLD_FILENAME)
        if PLAY_WORLD == None:
            debugTextbox.string += f"\nunable to open {WORLD_FILENAME}"
            debugTextbox.draw(display)
            pygame.display.update(loadingTextRect)
            print(f"unable to open {WORLD_FILENAME}")
            quit()
    else:
        debugTextbox.string += f"\n{WORLD_FILENAME} does not exist, generating world and saving to file"
        debugTextbox.draw(display)
        pygame.display.update(loadingTextRect)
        print(f"{WORLD_FILENAME} does not exist, generating world and saving to file")
        WORLD_WIDTH_CHUNKS = 8
        WORLD_HEIGHT_CHUNKS = 8 
        WORLD_DEPTH_CHUNKS = 1
        CHUNKS_SIDE_LEN_ux = 16
        PLAY_WORLD = World(WORLD_WIDTH_CHUNKS,WORLD_HEIGHT_CHUNKS,WORLD_DEPTH_CHUNKS,CHUNKS_SIDE_LEN_ux)
        World.saveWorld(PLAY_WORLD,WORLD_FILENAME)
        debugTextbox.string += f"\n{WORLD_FILENAME} generated and saved"
        debugTextbox.draw(display)
        pygame.display.update(loadingTextRect)
        print(f"{WORLD_FILENAME} generated and saved")

    debugTextbox.string += "\nbuilding user interface"
    debugTextbox.draw(display)
    pygame.display.update(loadingTextRect)
    print("building user interface")

    MARGINS = 50
    PLAY_RECT = pygame.Rect(MARGINS,MARGINS,DISPLAY_WIDTH-2*MARGINS,DISPLAY_HEIGHT-2*MARGINS) #designate play area

    PLAY_TILES_FILENAME = "16x16_tiles.png"
    
    debugTextbox.string += f"\nloading tileset {PLAY_TILES_FILENAME}"
    debugTextbox.draw(display)
    pygame.display.update(loadingTextRect)
    print(f"loading tileset {PLAY_TILES_FILENAME}")

    PLAY_TILES = tileset.generateScaledTilesets(ZOOM_SCALES,tileset.load_tileset(PLAY_TILES_FILENAME,(16,16)))
    
    debugTextbox.string += "\ninitializing renderer"
    debugTextbox.draw(display)
    pygame.display.update(loadingTextRect)
    print("initializing renderer")

    RENDERER = renderer.Renderer(PLAY_RECT,PLAY_TILES,PLAY_WORLD,ZOOM_SCALES)

    print("Keys in entity_index", PLAY_WORLD.entity_index.keys())
    PLAYER_ENTITY_NAME = "Player Entity"
    SPAWN_COORDS_ux = [PLAY_WORLD.dimensions_ux[0]//2,
                   PLAY_WORLD.dimensions_ux[1]//2,
                   0]
    if PLAYER_ENTITY_NAME not in PLAY_WORLD.entity_index:
        debugTextbox.string += f"\nno player entity found"
        debugTextbox.draw(display)
        pygame.display.update(loadingTextRect)
        print(f"no player entity found")

        debugTextbox.string += f"\nplacing player entity at {SPAWN_COORDS_ux}"
        debugTextbox.draw(display)
        pygame.display.update(loadingTextRect)
        print(f"placing player entity at {SPAWN_COORDS_ux}")

        PLAYER_ENTITY = Entity(PLAY_WORLD,PLAYER_ENTITY_NAME,3,SPAWN_COORDS_ux)
        World.saveWorld(PLAY_WORLD)
    else:
        PLAYER_ENTITY = PLAY_WORLD.entity_index[PLAYER_ENTITY_NAME]
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
            if event.type == pygame.QUIT:
                running = False
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