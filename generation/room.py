import pygame
from storage.gameVars import *

class Room:
    def __init__(self, game, x, y, width, height):
        self.grid_pos = (x, y)

        self.width = width
        self.height = height

        self.world_x = x * width
        self.world_y = y * height

        self.rect = pygame.Rect(self.world_x, self.world_y, width, height)

        self.completed = False

        # events
        self.events = []
        self.event_flags = {}

        self.doors = {
            "up": {"open": True, "entities": []},
            "down": {"open": True, "entities": []},
            "left": {"open": True, "entities": []},
            "right": {"open": True, "entities": []},
        }

        self.door_rects = []
        self.update_door_rects()

        self.tiles = []
        # wall rects is what's used for collision calcs
        self.wall_rects = []
        self.render_cache = {}

    def openDoor(self, direction):
        door_data = self.doors[direction]

        if door_data["open"]:
            return

        door_data["open"] = True

        for door in door_data["entities"]:
            door.opened = True
            door.changeAnim(1)
            door.defaultAnim = 2

        self.update_door_rects()

    def trigger_event(self, event_name):
        self.event_flags[event_name] = True

    def update_tiles(self, tiles):
        self.tiles = tiles
        self.wall_rects = self.get_wall_rects()

    def get_tile_rect(self, x, y):
        return pygame.Rect(
            self.world_x + x * 32,
            self.world_y + y * 32,
            32,
            32
        )
    
    def get_wall_rects(self):
        rects = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile != "empty":
                    rects.append(self.get_tile_rect(x, y))
        return rects

    def update_door_rects(self):
        self.door_rects = []

        DOOR_POS = [7, 8]
        DOOR_DEPTH = 1
        TILE_SIZE = 32

        for direction, data in self.doors.items():
            if data["open"]:
                continue  # no collision if open

            # --- TOP DOOR ---
            if direction == "up":
                for y in range(DOOR_DEPTH):
                    for x in DOOR_POS:
                        rect = pygame.Rect(
                            self.world_x + x * TILE_SIZE,
                            self.world_y + y * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE
                        )
                        self.door_rects.append(rect)

            # --- BOTTOM DOOR ---
            elif direction == "down":
                for y in range(16 - DOOR_DEPTH, 16):
                    for x in DOOR_POS:
                        rect = pygame.Rect(
                            self.world_x + x * TILE_SIZE,
                            self.world_y + y * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE
                        )
                        self.door_rects.append(rect)

            # --- LEFT DOOR ---
            elif direction == "left":
                for x in range(DOOR_DEPTH):
                    for y in DOOR_POS:
                        rect = pygame.Rect(
                            self.world_x + x * TILE_SIZE,
                            self.world_y + y * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE
                        )
                        self.door_rects.append(rect)

            # --- RIGHT DOOR ---
            elif direction == "right":
                for x in range(16 - DOOR_DEPTH, 16):
                    for y in DOOR_POS:
                        rect = pygame.Rect(
                            self.world_x + x * TILE_SIZE,
                            self.world_y + y * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE
                        )
                        self.door_rects.append(rect)
    
    def update(self):
        for event in self.events:
            if event["done"]:
                continue

            if event["type"] == "clear_enemies":
                room_enemies = [e for e in self.game.enemy_sprites if e.room == self]

                if len(room_enemies) == 0:
                    self.open_all_doors()
                    event["done"] = True

            elif event["type"] == "button_pressed":
                if self.event_flags.get("button"):
                    self.openDoor(event["target"])
                    event["done"] = True

                    
    
    def open_all_doors(self):
        for d in self.doors:
            self.doors[d]["open"] = True

        self.update_door_rects()
