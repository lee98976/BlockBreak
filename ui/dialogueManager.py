import pygame
from pygame.locals import *
from storage.gameVars import *
from storage.animatedObject import AnimatedObject


class DialogueManager:
    def __init__(self, game):
        self.game = game
        self.active = False
        self.dialogue = []
        self.index = 0
        self.text_timer = 0
        self.current_text = ""


        self.portrait = AnimatedObject(self.game.dialogueAnimSet)

        # cache font (IMPORTANT)
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 8)

        self.speaker_to_anim = {
            "player": 0,
            "bullie": 1,
            "reddie": 2,
            "boss": 3,
            "game": 4,
        }

        self.speaker_side = {
            "player": "left",
            "bullie": "right",
            "reddie": "right",
            "boss": "right",
            "game": "right"
        }
    
    def start(self, dialogue):
        if not dialogue:
            return

        self.active = True
        self.dialogue = dialogue
        self.index = 0
        self.current_text = ""
        self.text_timer = 0

        self.updatePortrait()
    
    def updatePortrait(self):
        if not self.dialogue or self.index >= len(self.dialogue):
            return

        entry = self.dialogue[self.index]
        speaker = entry.get("speaker", "reddie")

        anim = self.speaker_to_anim.get(speaker, 0)
        self.portrait.changeAnim(anim)
        self.portrait.defaultAnim = anim

    def update(self):
        if not self.active:
            return

        if self.index >= len(self.dialogue):
            self.active = False
            return

        entry = self.dialogue[self.index]
        full_text = entry["text"]

        # typewriter
        self.text_timer += 1
        speed = 2

        chars = self.text_timer // speed
        self.current_text = full_text[:chars]

    def handle_input(self, event):
        if not self.active:
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            entry = self.dialogue[self.index]
            full_text = entry["text"]

            # finish typing
            if self.current_text != full_text:
                self.current_text = full_text
                self.text_timer = len(full_text) * 2
            else:
                self.index += 1
                self.text_timer = 0

                if self.index >= len(self.dialogue):
                    self.active = False
                    return

                self.updatePortrait()
    
    def wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            width, _ = font.size(test_line)

            if width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines
    
    def draw(self):
        if not self.active or self.index >= len(self.dialogue):
            return

        screen = self.game.screen
        entry = self.dialogue[self.index]

        # --- dialogue box ---
        rect = pygame.Rect(25, HEIGHT - 150, WIDTH - 50, 100)
        pygame.draw.rect(screen, (20, 20, 30), rect)
        pygame.draw.rect(screen, (200, 200, 255), rect, 3)

        # --- portrait ---
        speaker = entry.get("speaker", "player")
        side = self.speaker_side.get(speaker, "left")

        PORTRAIT_PADDING = 20

        self.portrait.renderAnim()
        img = self.portrait.image

        if side == "left":
            x = rect.x + PORTRAIT_PADDING
            change = 100
        else:
            x = rect.right - img.get_width() - PORTRAIT_PADDING
            change = 20

        y = rect.y + 20
        self.portrait.renderAnim()
        self.portrait.rect.topleft = (x, y)

        img = self.portrait.image
        if side == "right":
            img = pygame.transform.flip(img, True, False)
        
        screen.blit(img, self.portrait.rect)

        # --- text ---
        lines = self.wrap_text(self.current_text, self.font, rect.width - 120)

        for i, line in enumerate(lines):
            text_surf = self.font.render(line, True, (255, 255, 255))
            
            screen.blit(text_surf, (rect.x + change, rect.y + 20 + i * 24))