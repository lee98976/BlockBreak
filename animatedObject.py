import pygame
from pygame.locals import *

from gameVars import *

def processImage(path, scale):
    unscaled = pygame.image.load(path).convert_alpha()

    newWidth = int(unscaled.get_width() * scale)
    newHeight = int(unscaled.get_height() * scale)

    return pygame.transform.scale(unscaled, (newWidth, newHeight))

class AnimatedObject(pygame.sprite.Sprite):
    def __init__(self, animSet):
        super().__init__()

        self.pos = vec(animSet["pos"]) # 2D vector

        self.images = [processImage(path, 4) for path in animSet["img_paths"]]
        self.image = self.images[0]
        self.rect = self.image.get_bounding_rect()

        self.anims = animSet["anims"] # dictionary that describes anim states
        self.defaultAnim = 0

        self.currentAnim = 0
        self.curImageIndex = 0
        self.frameTimer = self.anims[self.currentAnim][0][1]

    def changeAnim(self, newAnim):
        if newAnim == self.currentAnim:
            return
        self.currentAnim = newAnim
        self.curImageIndex = 0
        self.frameTimer = self.anims[newAnim][0][1]

    def renderAnim(self):
        anim = self.anims[self.currentAnim]

        self.frameTimer -= 1

        if self.frameTimer <= 0:
            self.curImageIndex += 1

            if self.curImageIndex >= len(anim):
                if self.currentAnim == self.defaultAnim:
                    self.curImageIndex = 0
                else:
                    self.changeAnim(self.defaultAnim)
                    return

            self.frameTimer = anim[self.curImageIndex][1]

        self.image = self.images[anim[self.curImageIndex][0]]