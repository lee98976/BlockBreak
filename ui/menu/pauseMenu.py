# pauseMenu.py

from ui.menu.menuOption import MenuOption
import pygame
import sys
from storage.gameVars import *

class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 8)

        self.options = [
            MenuOption("Resume", vec(WIDTH//2 - 50, HEIGHT//2 - 40), self.font, (255, 255, 255)),
            MenuOption("Main Menu", vec(WIDTH//2 - 50, HEIGHT//2 - 20), self.font, (255, 255, 255)),
            MenuOption("Quit", vec(WIDTH//2 - 50, HEIGHT//2), self.font, (255, 255, 255)),
        ]

        self.index = 0
        self.inputCooldown = 0
        self.pauseSurface = None

    def update(self, events, dt):
        keys = pygame.key.get_pressed()
        self.inputCooldown -= dt * DESIGN_FPS

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.index < 0:
                        self.index = 0
                        continue
                    self.index = (self.index + 1) % len(self.options)

                elif event.key == pygame.K_UP:
                    if self.index < 0:
                        self.index = 0
                        continue
                    self.index = (self.index - 1) % len(self.options)

                elif event.key == pygame.K_c:
                    self.select()

        for i, opt in enumerate(self.options):
            opt.selected = (i == self.index)
            opt.update(dt, i)

    def select(self):
        option = self.options[self.index]

        if option.text == "Resume":
            self.game.state = "game"

        elif option.text == "Main Menu":
            self.game.fading = True
            self.game.fade_target = "menu"
            self.game.menu.index = -1

        elif option.text == "Quit":
            pygame.quit()
            sys.exit()

    def draw(self, screen):
        if self.pauseSurface:
            screen.blit(self.pauseSurface, (0, 0))

        # tint overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))

        screen.blit(overlay, (0, 0))

        for opt in self.options:
            opt.draw(screen)