import pygame
from pygame.locals import *

from storage.animatedObject import AnimatedObject
from storage.gameVars import *

def draw_debug_rect(screen, rect, camera):
    offset = rect.topleft - camera + vec(WIDTH/2, HEIGHT/2)
    debug_rect = pygame.Rect(offset, rect.size)
    pygame.draw.rect(screen, (0, 0, 0), debug_rect, 2)

class Entity(AnimatedObject):
    def __init__(self, game, animSet, name, hp):
        super().__init__(animSet)
        self.hp = hp
        self.game = game
        self.name = name
        self.invFrames = 0
        self.dead = False
        self.vel = vec(0, 0)

    def takeDamage(self, dmg, iFrames=30):
        if (self.invFrames > 0 and dmg > 0) or self.dead:
            return
        print(f"{self.name} hit! HP: {self.hp}")
        self.hp -= dmg
        self.invFrames = iFrames

        self.updateHealthBar()

        if self.hp <= 0:
            self.dead = True
            self.onDeath()

    def onDeath(self):
        pass
    
    def updateHealthBar(self):
        pass

    def updateEntity(self):
        if self.invFrames > 0:
            self.invFrames -= 1

        # X
        self.pos.x += self.vel.x
        self.rect.centerx = self.pos.x
        self.collide("x")

        # Y
        self.pos.y += self.vel.y
        self.rect.centery = self.pos.y
        self.collide("y")

        self.rect.center = self.pos

    def collide(self, axis):
        for wall in self.game.get_current_room(self).wall_rects:
            if not self.rect.colliderect(wall):
                continue

            if axis == "x":
                if self.vel.x > 0:
                    self.rect.right = wall.left
                elif self.vel.x < 0:
                    self.rect.left = wall.right

                self.pos.x = self.rect.centerx
            elif axis == "y":
                if self.vel.y > 0:
                    self.rect.bottom = wall.top
                elif self.vel.y < 0:
                    self.rect.top = wall.bottom

                self.pos.y = self.rect.centery
            
            