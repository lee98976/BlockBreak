import pygame

from room import Room
from storage.gameVars import *
from storage.animSets import *

def processImage(path, scale):
    unscaled = pygame.image.load(path).convert_alpha()

    newWidth = int(unscaled.get_width() * scale)
    newHeight = int(unscaled.get_height() * scale)

    return pygame.transform.scale(unscaled, (newWidth, newHeight))

def build_animset(animSet, scale=4):
    return {
        **animSet,
        "images": [processImage(path, scale) for path in animSet["img_paths"]]
    }

class Game:
    def __init__(self):
        self.gameTime = 0

        # manage entities
        self.friendly_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.healthBar = None
        self.player = None

        # preload all images to save memory
        self.playerAnimSet = playerAnimSet
        self.enemyAnimSet = enemyAnimSet
        self.miniBossAnimSet = miniBossAnimSet
        self.bossAnimSet = bossAnimSet
        self.healthPackSet = healthPackSet
        self.heartSet = heartSet

        self.buildAnimSets()

        # room generation!
        self.rooms = {}
        self.room_width = WIDTH
        self.room_height = HEIGHT

        self.build_rooms()

        # camera!
        self.camera = vec(0, 0)
        self.camera_lerp = 0.1  # smoothing strength
        self.camera_max_offset = 120

    def build_rooms(self):
        for x in range(3):
            for y in range(3):
                room = Room(x, y, self.room_width, self.room_height)
                self.rooms[(x, y)] = room
    
    def get_current_room(self, entity):
        px, py = entity.pos

        room_x = int(px // self.room_width)
        room_y = int(py // self.room_height)

        return self.rooms.get((room_x, room_y))
    
    def get_room_center(self):
        room = self.get_current_room(self.player)
        if not room:
            return pygame.Vector2(0, 0)

        return pygame.Vector2(
            room.world_x + room.width / 2,
            room.world_y + room.height / 2
        )
    
    def get_camera_target(self):
        center = self.get_room_center()
        player_pos = self.player.pos

        offset = player_pos - center

        # clamp offset (this is your "edge push")
        offset.x = max(-self.camera_max_offset, min(self.camera_max_offset, offset.x))
        offset.y = max(-self.camera_max_offset, min(self.camera_max_offset, offset.y))

        return center + offset * 0.25
    
    def update_camera(self):
        target = self.get_camera_target()
        self.camera += (target - self.camera) * self.camera_lerp

    def buildAnimSets(self):
        self.playerAnimSet = build_animset(self.playerAnimSet)
        self.enemyAnimSet = build_animset(self.enemyAnimSet)
        self.miniBossAnimSet = build_animset(self.miniBossAnimSet)
        self.bossAnimSet = build_animset(self.bossAnimSet)
        self.healthPackSet = build_animset(self.healthPackSet)
        self.heartSet = build_animset(self.heartSet)

    def update(self):
        self.friendly_sprites.update()
        self.enemy_sprites.update()

    def draw(self, screen):
        self.friendly_sprites.draw(screen)
        self.enemy_sprites.draw(screen)
