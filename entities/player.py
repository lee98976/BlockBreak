import pygame
from pygame.locals import *
import sys

from entity import Entity
from storage.gameVars import *
from vfx.dashTrail import *

class Player(Entity):
    def __init__(self, game, healthBar, pos):
        super().__init__(game, game.playerAnimSet, "Player", 5, pos)
        self.despawnTime = 300

        self.isDashing = False
        self.dashFrames = 0
        self.dashVector = vec(0, 0)
        self.lastInput = K_UP

        self.desiredVel = vec(0,0)
        self.vel = vec(0,0)

        self.healthBar = healthBar
        self.lastRoom = self.game.get_current_room(self)

    def posUpdate(self):
        self.desiredVel = vec(0,0)

        if self.isDashing:
            self.desiredVel = self.dashVector
            self.dashVector *= 0.94
        else:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_LEFT]:
                self.lastInput = K_LEFT
                self.desiredVel.x = -2
            if pressed_keys[K_RIGHT]:
                self.lastInput = K_RIGHT
                self.desiredVel.x = 2
            if pressed_keys[K_UP]:
                self.lastInput = K_UP
                self.desiredVel.y = -2
            if pressed_keys[K_DOWN]:
                self.lastInput = K_DOWN
                self.desiredVel.y = 2


    def dash(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_x] and self.dashFrames < -5 and not self.isDashing:
            self.changeAnim(1)
            self.isDashing = True
            self.dashFrames = 13
            self.dashVector = vec(0,0)
            dashSpeed = 13

            totalPressed = 0
            if pressed_keys[K_LEFT]:
                totalPressed += 1
                self.dashVector.x = -1
            if pressed_keys[K_RIGHT]:
                totalPressed += 1
                self.dashVector.x = 1
            if pressed_keys[K_UP]:
                totalPressed += 1
                self.dashVector.y = -1
            if pressed_keys[K_DOWN]:
                totalPressed += 1
                self.dashVector.y = 1

            # if no keys pressed, just go with the last input
            if not (pressed_keys[K_LEFT] or pressed_keys[K_RIGHT] or pressed_keys[K_UP] or pressed_keys[K_DOWN]):
                if self.lastInput == K_LEFT:
                    totalPressed += 1
                    self.dashVector.x = -1
                if self.lastInput == K_RIGHT:
                    totalPressed += 1
                    self.dashVector.x = 1
                if self.lastInput == K_UP:
                    totalPressed += 1
                    self.dashVector.y = -1
                if self.lastInput == K_DOWN:
                    totalPressed += 1
                    self.dashVector.y = 1
            
            diagonal = True if totalPressed >= 2 else False
            self.dashVector = self.dashVector.normalize() * dashSpeed

            trail = DashTrail(self.game, self, diagonal=diagonal)
            self.game.friendly_sprites.add(trail)

    def onDeath(self):
        self.changeAnim(2)
    
    def updateHealthBar(self):
        self.healthBar.updateHealth(self.hp)
    
    def checkRoomSwitch(self):
        room = self.game.get_current_room(self)
        if room == self.lastRoom: return
        self.lastRoom = room
        
        room.discovered = True
        print("swap")

        # trigger event system (optional but clean)
        room.trigger_event("enter")

        # if this is a combat room → lock doors
        if getattr(room, "kill_all_enemies", False) and not room.completed:
            for d in room.doors:
                room.doors[d]["open"] = False
            room.update_door_rects()

    def update(self):
        self.renderAnim()

        if not self.dead:
            self.posUpdate()
            self.dash()
            self.checkRoomSwitch()

            # update entity depends on self.vel
            mult = 1
            if self.vel.magnitude() > self.desiredVel.magnitude(): mult = 0.2
            else: mult = 0.8
            self.vel += (self.desiredVel - self.vel) * mult
            # print("v", self.vel)

            self.immuneToStatusEffects = self.isDashing
            self.updateEntity()
            self.dashFrames -= 1
        else:
            self.despawnTime -= 1
            if self.despawnTime <= 0:
                pygame.quit()
                sys.exit()

        if self.dashFrames <= 0:
            self.isDashing = False
