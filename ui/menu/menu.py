from storage.gameVars import *
from ui.menu.menuOption import MenuOption
import sys

class Menu:
    def __init__(self, game):
        self.game = game

        self.options = [
            MenuOption("Start", vec(WIDTH//2 - 50, HEIGHT//2)),
            MenuOption("Quit", vec(WIDTH//2 - 50, HEIGHT//2 + 20)),
        ]

        self.index = -1
        self.inputCooldown = 0
        self.time = 0
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        self.inputCooldown -= dt * DESIGN_FPS

        if self.inputCooldown <= 0:
            if keys[pygame.K_DOWN]:
                self.index = (self.index + 1) % len(self.options)
                self.inputCooldown = 10

            if keys[pygame.K_UP]:
                self.index = (self.index - 1) % len(self.options)
                self.inputCooldown = 10

            if keys[pygame.K_c]:
                self.select()

        # update selection
        for i, opt in enumerate(self.options):
            opt.selected = (i == self.index)
            opt.update(dt, i)
    
    def select(self):
        option = self.options[self.index]

        if option.text == "Start":
            self.game.state = "game"

        elif option.text == "Quit":
            pygame.quit()
            sys.exit()
    
    def draw(self, screen):
        # # --- draw gameplay in background ---
        # self.game.draw_game_world(background_only=True)

        # # --- fake blur (dark overlay) ---
        # overlay = pygame.Surface((WIDTH, HEIGHT))
        # overlay.fill((0, 0, 0))
        # overlay.set_alpha(140)
        # screen.blit(overlay, (0, 0))

        # --- draw menu options ---
        for opt in self.options:
            opt.draw(screen)