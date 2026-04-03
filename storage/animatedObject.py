import pygame
import math
from pygame.locals import *

from storage.gameVars import *

class AnimatedObject(pygame.sprite.Sprite):
    def __init__(self, animSet, rectDimensions=None):
        super().__init__()

        self.images = animSet["images"]
        self.image = self.images[0]

        self.rect = self.image.get_bounding_rect()

        self.rotation = animSet.get("rotation", 0)

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

        # calculate the next frame
        if self.frameTimer <= 0:
            self.curImageIndex += 1

            if self.curImageIndex >= len(anim):
                if self.currentAnim == self.defaultAnim:
                    self.curImageIndex = 0
                else:
                    self.changeAnim(self.defaultAnim)
                    return

            self.frameTimer = anim[self.curImageIndex][1]

        currentFrame = self.images[anim[self.curImageIndex][0]]

        if self.rotation != 0:
            currentFrame = pygame.transform.rotate(currentFrame, self.rotation)

        self.image = currentFrame