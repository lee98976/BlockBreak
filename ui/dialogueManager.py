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

    def update(self, dt=1/DESIGN_FPS):
        if not self.active:
            return

        if self.index >= len(self.dialogue):
            self.active = False
            return

        entry = self.dialogue[self.index]
        full_text = entry["text"]

        # typewriter
        speed = 30  # characters per second
        self.text_timer += dt * speed

        chars = int(self.text_timer)
        self.current_text = full_text[:chars]

        self.portrait.renderAnim(dt)

    def handle_input(self, event):
        if not self.active:
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            entry = self.dialogue[self.index]
            full_text = entry["text"]

            # finish typing
            if self.current_text != full_text:
                self.current_text = full_text
                speed = 30
                self.text_timer = len(full_text)
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
        BOX_PADDING = 4
        BOX_HEIGHT = 48
        rect = pygame.Rect(BOX_PADDING, HEIGHT - BOX_HEIGHT - BOX_PADDING, WIDTH - BOX_PADDING * 2, BOX_HEIGHT)
        pygame.draw.rect(screen, (20, 20, 30), rect)
        pygame.draw.rect(screen, (200, 200, 255), rect, 2)

        # --- portrait ---
        speaker = entry.get("speaker", "player")
        side = self.speaker_side.get(speaker, "left")

        PORTRAIT_PADDING = 4
        img = self.portrait.image
        portrait_width = img.get_width()
        portrait_height = img.get_height()

        if side == "left":
            img_x = rect.x + PORTRAIT_PADDING
            text_x = img_x + portrait_width + PORTRAIT_PADDING * 2
        else:
            img_x = rect.right - portrait_width - PORTRAIT_PADDING
            text_x = rect.x + PORTRAIT_PADDING

        img_y = rect.y + (rect.height - portrait_height) // 2
        self.portrait.rect.topleft = (img_x, img_y)

        img = self.portrait.image
        if side == "right":
            img = pygame.transform.flip(img, True, False)

        screen.blit(img, self.portrait.rect)

        # --- text ---
        text_width = rect.width - portrait_width - PORTRAIT_PADDING * 4
        if text_width < 16:
            text_width = rect.width - PORTRAIT_PADDING * 2

        lines = self.wrap_text(self.current_text, self.font, text_width)
        line_height = self.font.get_linesize()
        text_y = rect.y + PORTRAIT_PADDING

        for i, line in enumerate(lines):
            text_surf = self.font.render(line, True, (255, 255, 255))
            screen.blit(text_surf, (text_x, text_y + i * line_height))