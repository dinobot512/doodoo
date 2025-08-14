import pygame
from game import Entity, World
from renderer import Renderer


class InputHandler:
        def __init__(self,player: Entity,world: World, renderer: Renderer):
                self.player = player
                self.world = world
                self.renderer = renderer

                self.keybinds = {
                        pygame.K_w:     {"func": lambda: self.player.move(0,-1,0), "render": True},
                        pygame.K_a:     {"func": lambda: self.player.move(-1,0,0), "render": True},
                        pygame.K_s:     {"func": lambda: self.player.move(0,1,0), "render": True},
                        pygame.K_d:     {"func": lambda: self.player.move(1,0,0), "render": True},                   
                        pygame.K_q:     {"func": lambda: self.player.move(-1,-1,0), "render": True},
                        pygame.K_e:     {"func": lambda: self.player.move(1,-1,0), "render": True},
                        pygame.K_z:     {"func": lambda: self.player.move(-1,1,0), "render": True},
                        pygame.K_c:     {"func": lambda: self.player.move(1,1,0), "render": True},

                        pygame.K_MINUS:     {"func": lambda: self.renderer.decrementZoom(), "render": True},
                        pygame.K_EQUALS:    {"func": lambda: self.renderer.incrementZoom(), "render": True},

                        pygame.K_F5:     {"func": lambda: self.world.saveWorld(), "render": False},
                        pygame.K_F5:     {"func": lambda: self.world.loadWorld(), "render": False},

                        pygame.K_F3: {"func": lambda: self.renderer.toggleDebugMode(),"render": True}
                }

        def handleKeydown(self, key) -> bool:
                if key in self.keybinds:
                        self.keybinds[key]["func"]()
                        return self.keybinds[key]["render"]
                return False