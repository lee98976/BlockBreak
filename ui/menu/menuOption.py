from storage.gameVars import *
import random
import math

class MenuOption:
    def __init__(self, text, pos, font, selectedColor):
        self.text = text
        self.base_pos = vec(pos)
        self.pos = vec(pos)
        self.font = font
        self.selectedColor = selectedColor

        self.selected = False

        self.hover_offset = 0
        self.time = random.random() * 3  # offset so they don’t sync
    
    def update(self, dt, index):
        frames = dt * DESIGN_FPS

        self.time += frames

        # float motion
        float_y = math.sin(self.time * 0.05 + index) * 2

        # hover lerp
        target = 10 if self.selected else 0
        self.hover_offset += (target - self.hover_offset) * 0.15 * frames

        self.pos.x = self.base_pos.x + self.hover_offset
        self.pos.y = self.base_pos.y + float_y
    
    def draw(self, screen):
        color = self.selectedColor if self.selected else (180, 180, 180)
        text_surf = self.font.render(self.text, True, color)
        screen.blit(text_surf, self.pos)