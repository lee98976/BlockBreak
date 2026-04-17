import pygame
from pygame.locals import *
import random
import math

from entity import Entity
from entities.pickups import HealthPack
from storage.gameVars import *

class Reddie(Entity):
    def __init__(self, game, hp, following, dropChance, pos):
        super().__init__(game, game.enemyAnimSet, "Reddie", hp, pos)

        self.following = following
        self.dropChance = dropChance

        self.isHarmful = True

        self.state = random.choice(["chase", "circle", "ambush"])
        self.stateTimer = random.randint(120, 240)

        self.stunTimer = 0
        self.shakeTimer = 0

        self.deleteTimer = 30

    def updateAI(self, dt=1/DESIGN_FPS):
        if self.following is None:
            return

        frame = dt * DESIGN_FPS
        # use astar algorithm in order to find the target to move to
        target, isDirect = self.get_navigation_target(self.following.pos, dt)
        
        diff = target - self.pos
        if diff.length() == 0:
            return
        direction = diff.normalize()

        desired = vec(0, 0)

        if isDirect:
            if self.state == "chase":
                desired = direction * 0.375
            elif self.state == "circle":
                perp = vec(-direction.y, direction.x)
                desired = direction * 0.2 + perp * 0.45
            elif self.state == "ambush":
                # slow tracking
                desired = direction * 0.1

                self.stateTimer -= frame
                if self.stateTimer <= 65:
                    desired = direction * 1
        else:
            desired = direction * 0.75
            if self.state == "ambush":
                self.changeAnim(3)
                self.defaultAnim = 0

            self.state = "chase"
            self.stateTimer = 20

            # self.draw_debug_path(self.game.get_current_room(self), self.game.screen, self.game.camera)

        self.vel += (desired - self.vel) * 0.15
        self.vel += vec(random.uniform(-0.025, 0.025), random.uniform(-0.025, 0.025))

    def updateState(self, dt=1/DESIGN_FPS):
        frame = dt * DESIGN_FPS
        self.stateTimer -= frame

        if self.stateTimer > 0:
            return

        if self.state == "chase":
            self.state = random.choice(["circle", "ambush"])
            self.stateTimer = random.randint(120, 240)

            if self.state == "ambush":
                self.changeAnim(2)  # transform → ambush
                self.defaultAnim = 1  # ambush idle

        elif self.state == "circle":
            self.state = "chase"
            self.stateTimer = random.randint(100, 160)
        elif self.state == "ambush":
            self.state = "chase"
            self.stateTimer = random.randint(180, 260)

            self.changeAnim(3)
            self.defaultAnim = 0

    def takeDamage(self, dmg, iFrames=30):
        super().takeDamage(dmg, iFrames)

        if self.dead:
            return

        # knockback + stun
        player = self.game.player
        direction = (self.pos - player.pos)

        if direction.length() > 0:
            direction = direction.normalize()
            self.vel += direction * 2

        self.stunTimer = 40
        self.shakeTimer = 0
        self.shakeOffset = vec(0, 0)

    def update_shake(self, dt=1/DESIGN_FPS):
        frame = dt * DESIGN_FPS
        if self.shakeTimer > 0:
            self.shakeTimer -= frame
            # Random shake: ±2 units
            amplitude = 4 * self.shakeTimer / 20  
            self.shakeOffset.x = random.uniform(-amplitude, amplitude)
            self.shakeOffset.y = random.uniform(-amplitude, amplitude)
        else:
            self.shakeOffset = vec(0, 0)

    def onDeath(self):
        self.game.vfxManager.add_particles(
            pos=self.pos,
            count=6,
            start_color=(255, 120, 40),
            end_color=(180, 30, 10),
            size=1,
            gravity=True,
            floaty=False
        )
        self.following = None
        self.isHarmful = False
        self.changeAnim(4)

    def update(self, dt=1/DESIGN_FPS):
        frame = dt * DESIGN_FPS
        if not self.room.discovered or self.game.dialogue.active: return
        self.renderAnim(dt)
        if not self.dead:
            if self.stunTimer > 0:
                self.stunTimer -= frame
                self.vel *= 0.85 ** frame
                self.isHarmful = False  # Not harmful while stunned
                self.update_shake(dt)
            else:
                self.isHarmful = True  # Harmful when not stunned
                self.updateAI(dt)
                self.updateState(dt)

            self.updateEntity(dt)
            
            # If stunned and hit a wall during movement, extend stun and start shake
            if self.stunTimer > 0 and self.contactWall:
                self.stunTimer += 30  # +0.5 seconds at 60 FPS
                self.shakeTimer = 20  # shake for ~0.33 seconds
                self.vel *= -0.7  # Bounce back
            

        else:
            self.deleteTimer -= frame
            if self.deleteTimer <= 0:
                if random.random() < self.dropChance:
                    hp = HealthPack(self.game, self.pos)
                    self.game.friendly_sprites.add(hp)
                self.kill()
