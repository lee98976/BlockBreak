from storage.animatedObject import AnimatedObject
from storage.gameVars import *
from ui.menu.menuOption import MenuOption
import pygame
import sys

class Menu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 8)

        # --- menu states ---
        self.state = "main"  # "main" or "level_select"

        # --- options ---
        self.main_options = [
            MenuOption("Start", vec(WIDTH//2 - 50, HEIGHT//2 - 50), self.font, (0, 0, 0)),
            MenuOption("Quit",  vec(WIDTH//2 - 50, HEIGHT//2 - 30), self.font, (0, 0, 0)),
        ]

        self.level_options = [
            MenuOption("Level 1", vec(WIDTH//2 - 50, HEIGHT//2 - 50), self.font, (0, 0, 0)),
            MenuOption("Level 2", vec(WIDTH//2 - 50, HEIGHT//2 - 30), self.font, (0, 0, 0)),
            MenuOption("Back",    vec(WIDTH//2 - 50, HEIGHT//2 - 10), self.font, (0, 0, 0)),
        ]

        self.options = self.main_options

        # --- animation ---
        self.startAnim = AnimatedObject(game.menuStartAnimSet)

        # --- control ---
        self.index = -2
        self.inputCooldown = 0
        self.time = 0

    def update(self, events, dt):
        keys = pygame.key.get_pressed()

        self.startAnim.renderAnim(dt)
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
        print(option.text)

        # =========================
        # MAIN MENU
        # =========================
        if self.state == "main":
            if option.text == "Start":
                self.state = "level_select"
                self.options = self.level_options
                self.index = 0

            elif option.text == "Quit":
                pygame.quit()
                sys.exit()

        # =========================
        # LEVEL SELECT
        # =========================
        elif self.state == "level_select":
            self.state = "main"
            if option.text == "Level 1":
                self.start_game(1)

            elif option.text == "Level 2":
                self.start_game(2)

            elif option.text == "Back":
                self.state = "main"
                self.options = self.main_options
                self.index = 0

    def start_game(self, level):
        # reinitialize game with chosen level
        self.game.__init__(self.game.screen, level=level)
        self.game.state = "game"

    def draw(self, screen):
        # --- menu options ---
        for opt in self.options:
            opt.draw(screen)

        # --- background animation ---
        screen.blit(self.startAnim.image, (0, 0))