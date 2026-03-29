import pygame
from pygame.locals import *
import sys
import random
import math

pygame.init()
vec = pygame.math.Vector2
clock = pygame.time.Clock()

_HEIGHT = 450
_WIDTH = 400
_FPS = 60

screen = pygame.display.set_mode((_WIDTH, _HEIGHT))
pygame.display.set_caption("Alyss")

def processImage(path, scale):
    unscaled = pygame.image.load(path).convert_alpha()

    newWidth = int(unscaled.get_width() * scale)
    newHeight = int(unscaled.get_height() * scale)

    return pygame.transform.scale(unscaled, (newWidth, newHeight))

class AnimatedObject(pygame.sprite.Sprite):
    def __init__(self, animSet):
        super().__init__()

        self.pos = vec(animSet["pos"]) 

        self.images = [processImage(path, 4) for path in animSet["img_paths"]]
        self.image = self.images[0]
        self.rect = self.image.get_bounding_rect()

        self.anims = animSet["anims"]
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

class Entity(AnimatedObject):
    def __init__(self, animSet, name, hp):
        super().__init__(animSet)
        self.hp = hp
        self.name = name
        self.invFrames = 0
        self.dead = False

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
        self.clampPosition()
        if self.invFrames > 0:
            self.invFrames -= 1
    
    def clampPosition(self):
        self.pos.x = max(0, min(self.pos.x, _WIDTH - 20))
        self.pos.y = max(0, min(self.pos.y, _HEIGHT - 20))

class Player(Entity):
    def __init__(self, animSet, healthBar):
        super().__init__(animSet, "Player", 5)
        self.pos = vec(200, 200)
        self.despawnTime = 300

        self.isDashing = False
        self.dashFrames = 0
        self.dashVector = vec(0, 0)
        self.lastInput = K_UP

        self.healthBar = healthBar

    def posUpdate(self):
        self.change = vec(0,0)

        if self.isDashing:
            self.change = self.dashVector
            self.dashVector *= 0.94
        else:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_LEFT]:
                self.lastInput = K_LEFT
                self.change.x = -2
            if pressed_keys[K_RIGHT]:
                self.lastInput = K_RIGHT
                self.change.x = 2
            if pressed_keys[K_UP]:
                self.lastInput = K_UP
                self.change.y = -2
            if pressed_keys[K_DOWN]:
                self.lastInput = K_DOWN
                self.change.y = 2

        self.pos += self.change

    def dash(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_x] and self.dashFrames < -5 and not self.isDashing:
            self.changeAnim(1)
            self.isDashing = True
            self.dashFrames = 13
            self.dashVector = vec(0,0)
            dashSpeed = 12

            if pressed_keys[K_LEFT]:
                self.dashVector.x = -dashSpeed
            if pressed_keys[K_RIGHT]:
                self.dashVector.x = dashSpeed
            if pressed_keys[K_UP]:
                self.dashVector.y = -dashSpeed
            if pressed_keys[K_DOWN]:
                self.dashVector.y = dashSpeed

            if pressed_keys[K_LEFT] or pressed_keys[K_RIGHT] or pressed_keys[K_UP] or pressed_keys[K_DOWN]:
                return

            if self.lastInput == K_LEFT:
                self.dashVector.x = -dashSpeed
            if self.lastInput == K_RIGHT:
                self.dashVector.x = dashSpeed
            if self.lastInput == K_UP:
                self.dashVector.y = -dashSpeed
            if self.lastInput == K_DOWN:
                self.dashVector.y = dashSpeed

    def onDeath(self):
        self.changeAnim(2)
    
    def updateHealthBar(self):
        self.healthBar.updateHealth(self.hp)

    def update(self):
        self.renderAnim()

        if not self.dead:
            self.updateEntity()
            self.posUpdate()
            self.dash()
            self.rect.center = self.pos
            self.dashFrames -= 1
        else:
            self.despawnTime -= 1
            if self.despawnTime <= 0:
                pygame.quit()
                sys.exit()

        if self.dashFrames <= 0:
            self.isDashing = False

class HealthPack(AnimatedObject):
    def __init__(self, animSet, pos):
        super().__init__(animSet)
        self.pos = vec(pos)

    def update(self):
        self.renderAnim()
        self.rect.center = self.pos

class Reddie(Entity):
    def __init__(self, animSet, hp, following, attackType, dropChance):
        super().__init__(animSet, "Reddie", hp)
        self.pos = vec(random.randint(50,350), random.randint(200,400))
        self.following = following
        self.attackType = attackType
        self.attackCooldown = 0
        self.switchTimer = 120
        self.deleteTimer = 30
        self.dropChance = dropChance
        self.isHarmful = True

        self.behavior = random.choice(["chase","circle","ambush"])
        self.attackTimer = random.randint(40,320)

    def posUpdate(self):
        if self.following is None:
            return

        dif = self.following.pos - self.pos

        if dif.length() == 0:
            return

        direction = dif.normalize()

        if self.behavior == "chase":
            self.pos += direction * 1.4
            if self.switchTimer < 0:
                if random.random() < 0.5:
                    self.switchTimer = random.randint(120,320)
                    self.behavior = "circle"
                else:
                    self.switchTimer = random.randint(200,400)
                    self.behavior = "ambush"
        elif self.behavior == "circle":
            perp = vec(-direction.y, direction.x)
            self.pos += direction * 1
            self.pos += perp * 2
            if self.switchTimer < 0:
                self.switchTimer = random.randint(100, 150)
                self.behavior = "chase"
        elif self.behavior == "ambush":
            self.pos += direction * 0.3
            self.attackTimer -= 1

            if self.attackTimer <= 0:
                self.pos += direction * 3
                if self.attackTimer < -40:
                    self.attackTimer = random.randint(120,320)
            
            if self.switchTimer < 0:
                self.switchTimer = random.randint(400, 450)
                self.behavior = "chase"
        
        self.pos += vec(random.uniform(-0.3,0.3), random.uniform(-0.3,0.3))

    def attack(self):
        if self.attackCooldown <= 0:
            if self.attackType == "ranged":
                self.attackCooldown = 50

    def onDeath(self):
        self.following = None
        self.dead = True
        self.isHarmful = False
        self.changeAnim(1)

    def update(self):
        self.renderAnim()
        self.updateEntity()

        if not self.dead:
            self.posUpdate()
            self.attack()
        else:
            self.deleteTimer -= 1
            if self.deleteTimer <= 0:
                if random.random() < self.dropChance:
                    hp = HealthPack(healthPackSet, self.pos)
                    friendly_sprites.add(hp)
                self.kill()
        
        self.switchTimer -= 1
        self.attackCooldown -= 1
        self.rect.center = self.pos

class MiniBoss(Entity):
    def __init__(self, animSet, player, enemy_group, x):
        super().__init__(animSet, "MiniBoss", 2)
        self.player = player
        self.enemy_group = enemy_group
        self.pos = vec(x,120)
        self.waveSize = 10
        self.deleteTimer = 120

        self.spawnWave()

    def spawnWave(self):
        for i in range(self.waveSize):
            e = Reddie(enemyAnimSet,1,self.player,"melee", 0.1)
            self.enemy_group.add(e)

    def takeDamage(self, dmg):
        if any(isinstance(e,Reddie) and not e.dead for e in self.enemy_group):
            return
        super().takeDamage(dmg)
        if not self.dead:
            self.spawnWave()
        

    def onDeath(self):
        self.changeAnim(1)

    def update(self):
        if not self.dead:
            self.pos.x += math.sin(pygame.time.get_ticks()/400)*0.3
        else:
            self.deleteTimer -= 1
            if self.deleteTimer <= 0: self.kill()

        self.renderAnim()
        self.updateEntity()
        self.rect.center = self.pos

class Laser:
    def __init__(self, angle):
        self.angle = angle
        self.hp = 3
        self.color = (255,0,0)
        self.cooldown = 0

    def hit(self):
        if self.cooldown > 0:
            return
        if self.hp > 0:
            self.hp -= 1
            self.cooldown = 20
            if self.hp <= 0:
                self.color = (0,0,255)

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

class Boss(Entity):
    def __init__(self, animSet, player, enemy_group):
        super().__init__(animSet, "Bossy", 999)
        self.player = player
        self.pos = vec(200,80)
        self.active = False
        self.angle = 0

        self.switchTimer = 60
        self.CW = 1
        self.mag = 1

        self.goToMag = 1.5

        self.spawnTimer = 0
        self.deleteTimer = 300
        self.enemy_group = enemy_group

        self.lasers = [Laser(0.25 * i * math.pi) for i in range(0, 8)]

    def activate(self):
        self.active = True
        self.defaultAnim = 1
        self.changeAnim(1)

    def onDeath(self):
        self.active = False
        self.changeAnim(2)

    def update(self):
        self.renderAnim()
        self.updateEntity()

        if self.mag < self.goToMag:
            self.mag += 0.02
            if self.mag >= self.goToMag:
                self.goToMag = 0.5
        else:
            self.mag -= 0.02
            if self.mag <= self.goToMag:
                self.goToMag = 1.5

        if self.switchTimer <= 0:
            self.CW *= -1
            self.switchTimer = random.randint(300, 600)

        if not self.dead:
            self.pos.y = 80 + math.sin(pygame.time.get_ticks()/500)*5
        else:
            self.deleteTimer -= 1
            self.switchTimer -= 1
            if self.deleteTimer < 0:
                self.active = False
                self.kill()

        if self.active:
            if self.spawnTimer <= 0:
                e = Reddie(enemyAnimSet,1,self.player,"melee", 0.5)
                self.enemy_group.add(e)
                self.spawnTimer = 90
                
            self.spawnTimer -= 1

            self.angle += 0.005 * self.CW * self.mag
            for l in self.lasers:
                l.angle += 0.005 * self.CW * self.mag
                l.update()

        self.rect.center = self.pos

    def drawLasers(self, screen):
        if not self.active:
            return

        for l in self.lasers:
            length = 600

            end = vec(
                self.pos.x + math.cos(l.angle)*length,
                self.pos.y + math.sin(l.angle)*length
            )

            pygame.draw.line(screen, l.color, self.pos, end, 8)

    def checkDashDamage(self, player):
        if not self.active:
            return

        for l in self.lasers:
            if l.hp <= 0: continue

            start = self.pos
            end = vec(
                self.pos.x + math.cos(l.angle)*600,
                self.pos.y + math.sin(l.angle)*600
            )

            line = end - start
            player_vec = player.pos - start

            t = max(0, min(1, player_vec.dot(line) / line.length_squared()))
            closest = start + line * t

            dist = (player.pos - closest).length()

            if dist < 10:

                if player.isDashing:
                    player.invFrames = 15
                    l.hit()
                else:
                    player.takeDamage(1,60)

    def deadCheck(self):
        return all(l.hp <= 0 for l in self.lasers)

playerAnimSet = {
    "pos": (200, 200),

    "img_paths": [
        "assets/playerBasic.png",
        "assets/playerDash.png",
        *[f"assets/playerDeath{i}.png" for i in range(1, 11)],
        "assets/playerProjectile1.png",
        "assets/playerProjectile2.png"
    ],

    "anims": [

        [(0, 200)],

        [(1, 12)],

        [(i, 8) for i in range(2, 11)] + [(11, 9999)]

    ]
}

enemyAnimSet = {
    "pos": (200, 200),

    "img_paths": [
        "assets/enemyAwakened.png",
        "assets/enemyDeath1.png",
        "assets/enemyDeath2.png",
        "assets/enemyDeath3.png",
        "assets/enemyProjectile1.png",
        "assets/enemyProjectile2.png"
    ],

    "anims": [

        [(0, 200)],

        [(1,10),(2,10),(3,10)],

        [(4,6),(5,6)]

    ]
}

miniBossAnimSet = {
    "pos": (200, 200),

    "img_paths": [
        "assets/miniBossAwakened.png",
        *[f"assets/miniBossDeath{i}.png" for i in range(1, 13)]
    ],

    "anims": [

        [(0, 200)],

        [(i,6) for i in range(1,12)] + [(12, 9999)]

    ]
}

bossAnimSet = {
    "pos": (200, 200),

    "img_paths": [
        "assets/bossAwakened.png",
        "assets/bossIdle.png",
        "assets/bossIdle1.png",
        "assets/bossIdle2.png",
        "assets/bossIdle3.png",
        *[f"assets/bossSummon{i}.png" for i in range(1,4)],
        *[f"assets/bossDeath{i}.png" for i in range(1,12)]
    ],

    "anims": [

        [(1,10),(2,10),(3,10),(4,10)],

        [(5,8),(6,8),(7,8)],

        [(i,6) for i in range(8,18)] + [(18, 9999)] 

    ]
}

heartSet = {
    "pos": (200,200),

    "img_paths": [
        "assets/heartEmpty.png",
        "assets/heartDamage.png",
        "assets/heartHeal1.png",
        "assets/heartHeal2.png",
        "assets/heartHeal3.png",
    ],

    "anims": [
        [(0, 200)],
        [(4, 200)],
        [(1, 30)],
        [(2,15),(3,15),(4,15)],
    ]
}

healthPackSet = {
    "pos": (0,0),

    "img_paths": [
        "assets/healOrb.png"
    ],

    "anims": [
        [(0,200)]
    ]
}

class HealthBar:
    def __init__(self, groupToAdd):
        self.hearts = [Heart(heartSet, (i * 40 + 20, 420)) for i in range(5)]

        for i in self.hearts:
            groupToAdd.add(i)
    
    def updateHealth(self, hp):
        for i in range(1, 5 + 1):
            curHeart = self.hearts[i - 1]
            if hp >= i:
                if not curHeart.on: curHeart.turnOn()
            else:
                if curHeart.on: curHeart.turnOff()

class Heart(AnimatedObject):
    def __init__(self, animSet, pos):
        super().__init__(animSet)
        self.pos = vec(pos)
        self.on = True
        self.defaultAnim = 1
        self.changeAnim(2)
    
    def turnOn(self):
        self.on = True
        self.changeAnim(3)
        self.defaultAnim = 1
    def turnOff(self):
        self.on = False
        self.changeAnim(2)
        self.defaultAnim = 0
    
    def update(self):
        self.renderAnim()
        self.rect.center = self.pos

friendly_sprites = pygame.sprite.Group()
healthBar = HealthBar(friendly_sprites)
player = Player(playerAnimSet, healthBar)
healthBar.updateHealth(player.hp)

friendly_sprites.add(player)

enemy_sprites = pygame.sprite.Group()

miniBoss1 = MiniBoss(miniBossAnimSet, player, enemy_sprites, 120)
miniBoss2 = MiniBoss(miniBossAnimSet, player, enemy_sprites, 280)

enemy_sprites.add(miniBoss1)
enemy_sprites.add(miniBoss2)

boss = Boss(bossAnimSet, player, enemy_sprites)
enemy_sprites.add(boss)

gameTime = 0
hasActivated = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if miniBoss1.dead and miniBoss2.dead and not hasActivated:
        boss.activate()
        hasActivated = True

    boss.checkDashDamage(player)

    if boss.deadCheck():
        boss.takeDamage(9999)

    hits = pygame.sprite.spritecollide(player, enemy_sprites, False)

    for enemy in hits:
        if player.isDashing:
            enemy.takeDamage(1)

        elif hasattr(enemy,"isHarmful") and enemy.isHarmful:
            player.takeDamage(1,60)
    
    for sprite in friendly_sprites:
        if isinstance(sprite, HealthPack):
            if player.rect.colliderect(sprite.rect):
                if player.hp < 5:
                    player.takeDamage(-1, 0)
                    sprite.kill()

    offset = vec(0,0)

    if boss.active:
        offset = vec(random.randint(-2,2), random.randint(-2,2))

    screen.fill((255,255,255))

    friendly_sprites.update()
    enemy_sprites.update()

    for s in friendly_sprites:
        screen.blit(s.image, s.rect.topleft + offset)

    for s in enemy_sprites:
        screen.blit(s.image, s.rect.topleft + offset)
    boss.drawLasers(screen)

    pygame.display.update()

    gameTime += 1
    clock.tick(_FPS)
