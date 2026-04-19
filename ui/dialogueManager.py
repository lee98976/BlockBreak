import pygame
import math
from pygame.locals import *
from storage.gameVars import *
from storage.animatedObject import AnimatedObject

# TODO pls pls pls improve dialogue manager to have much more personality later
class DialogueManager:
    def __init__(self, game):
        self.game = game
        self.active = False
        self.dialogue = []
        self.index = 0
        self.text_timer = 0
        self.current_text = ""

        self.screen_width = WIDTH * UPSCALE
        self.screen_height = HEIGHT * UPSCALE
        self.scale = UPSCALE


        self.portrait = AnimatedObject(self.game.dialogueAnimSet)

        # cache font (IMPORTANT)
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 16)

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
    
    def draw(self, screen, dt):
        if not self.active or self.index >= len(self.dialogue):
            return

        entry = self.dialogue[self.index]

        SCALE = UPSCALE
        SCREEN_W = WIDTH * SCALE
        SCREEN_H = HEIGHT * SCALE

        # --- dialogue box ---
        BOX_PADDING = 4 * SCALE
        BOX_HEIGHT = 48 * SCALE

        rect = pygame.Rect(
            BOX_PADDING,
            SCREEN_H - BOX_HEIGHT - BOX_PADDING,
            SCREEN_W - BOX_PADDING * 2,
            BOX_HEIGHT
        )

        pygame.draw.rect(screen, (20, 20, 30), rect)
        pygame.draw.rect(screen, (200, 200, 255), rect, 2)

        # --- portrait ---
        speaker = entry.get("speaker", "player")
        side = self.speaker_side.get(speaker, "left")

        PORTRAIT_PADDING = 4 * SCALE

        img = self.portrait.image
        pw, ph = img.get_width(), img.get_height()

        # scale portrait
        img = pygame.transform.scale(img, (pw * SCALE, ph * SCALE))

        if side == "left":
            img_x = rect.x + PORTRAIT_PADDING
            text_x = img_x + pw * SCALE + PORTRAIT_PADDING * 2
        else:
            img_x = rect.right - pw * SCALE - PORTRAIT_PADDING
            text_x = rect.x + PORTRAIT_PADDING
            img = pygame.transform.flip(img, True, False)

        img_y = rect.y + (rect.height - ph * SCALE) // 2

        screen.blit(img, (img_x, img_y))

        # --- text ---
        text_width = rect.width - pw * SCALE - PORTRAIT_PADDING * 4
        if text_width < 16:
            text_width = rect.width - PORTRAIT_PADDING * 2

        # IMPORTANT: wrap using UNSCALED width
        lines = self.wrap_text(self.current_text, self.font, text_width)

        line_height = self.font.get_linesize() + 4
        text_y = rect.y + 4 * self.scale

        time = self.game.gameTime / 60 # TODO lazy use dt

        for i, line in enumerate(lines):
            x_offset = 0

            for j, char in enumerate(line):
                char_surf = self.font.render(char, True, (255, 255, 255))

                # subtle sine wobble
                wobble_y = int(math.sin(time + j * 0.5 + i) * 1.5)

                # shadow (draw first)
                shadow = self.font.render(char, True, (0, 0, 0))
                screen.blit(shadow, (
                    text_x + x_offset + 1,
                    text_y + i * line_height + wobble_y + 1
                ))

                # main char
                screen.blit(char_surf, (
                    text_x + x_offset,
                    text_y + i * line_height + wobble_y
                ))

                x_offset += char_surf.get_width()

        full_text = entry["text"]

        if self.current_text == full_text:
            pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 0.5

            indicator = self.font.render("Z", True, (255, 255, 255))
            alpha = int(150 + 105 * pulse)

            indicator.set_alpha(alpha)

            screen.blit(
                indicator,
                (rect.right - 32, rect.bottom - 32)
            )