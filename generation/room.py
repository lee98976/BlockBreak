import pygame
from storage.gameVars import *

class Room:
    def __init__(self, game, x, y, width, height):
        self.grid_pos = (x, y)
        self.game = game

        self.width = width
        self.height = height

        self.world_x = x * width
        self.world_y = y * height

        self.rect = pygame.Rect(self.world_x, self.world_y, width, height)

        self.completed = False
        self.discovered = False
        self.enemies = []

        # events
        self.events = []
        self.event_flags = {}

        self.event_handlers = {
            "open_door": self._event_open_door,
            "open_all_doors": self._event_open_all_doors,
        }

        self.doors = {
            "up": {"type": "hole", "entities": []},
            "down": {"type": "hole", "entities": []},
            "left": {"type": "hole", "entities": []},
            "right": {"type": "hole", "entities": []},
        }

        self.door_rects = []
        self.update_door_rects()

        self.tiles = []
        # wall rects is what's used for collision calcs
        self.wall_rects = []
        self.render_cache = {}

    def _event_open_door(self, params):
        self.openDoor(params["direction"])

    def _event_open_all_doors(self, params):
        self.open_all_doors()

    def openDoor(self, direction):
        door_data = self.doors[direction]

        if door_data["type"] != "door":
            return

        door_data["type"] = "hole"

        for door in door_data["entities"]:
            door.opened = True
            door.changeAnim(1)
            door.defaultAnim = 2

        self.update_door_rects()

    def trigger_event(self, trigger_name):
        self.event_flags[trigger_name] = True

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
    
    def rotation_to_direction(self, rotation):
        if rotation == 0:
            return "up"
        elif rotation == 90:
            return "left"
        elif rotation == 180:
            return "down"
        elif rotation == 270:
            return "right"
            
    def get_wall_rects(self):
        rects = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                rect = self.get_tile_rect(x, y)
                tile = self.tiles[y][x]
                props = self.game.tile_properties.get(tile, {})

                if tile == "shortSpike" or tile == "tallSpike":
                    depth = props.get("depth", 16)
                    
                    # TODO: make tile metadata instead of js hogging off of render_cache
                    cached = self.render_cache.get((x, y))
                    if cached:
                        img, rotation = cached
                    else:
                        rotation = 0
                    direction = self.rotation_to_direction(rotation)

                    if direction == "up":
                        # anchored to bottom, shrink upward
                        rect = pygame.Rect(
                            rect.x,
                            rect.bottom - depth,
                            rect.width,
                            depth
                        )

                    elif direction == "down":
                        rect = pygame.Rect(
                            rect.x,
                            rect.y,
                            rect.width,
                            depth
                        )

                    elif direction == "left":
                        rect = pygame.Rect(
                            rect.right - depth,
                            rect.y,
                            depth,
                            rect.height
                        )

                    elif direction == "right":
                        rect = pygame.Rect(
                            rect.x,
                            rect.y,
                            depth,
                            rect.height
                        )

                if props.get("collide", False):
                    rects.append(rect)

        return rects

    def update_door_rects(self):
        self.door_rects = []

        DOOR_POS = [7, 8]
        DOOR_DEPTH = 1
        TILE_SIZE = 32

        for direction, data in self.doors.items():
            if data["type"] != "door":
                continue

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
        # --- check if all enemies are dead ---
        if self.enemies and self.discovered:
            # remove dead ones
            self.enemies = [e for e in self.enemies if not e.dead]

            if len(self.enemies) == 0 and not self.completed:
                self.completed = True
                self.trigger_event("all_enemies_dead")


        for event in self.events:
            if event["done"]:
                continue

            trigger = event["trigger"]

            if self.event_flags.get(trigger):
                action = event["action"]
                params = event.get("params", {})

                handler = self.event_handlers.get(action)
                if handler:
                    handler(params)

                event["done"] = True

                    
    
    def open_all_doors(self):
        for d in self.doors:
            self.doors[d]["open"] = True

        self.update_door_rects()

    # for pathfinding, finds all exit tiles that are actually empty
    def get_exit_tiles(self, direction):
        exits = []

        if direction == "up":
            y = 0
            for x in range(16):
                if self.tiles[y][x] == "empty":
                    exits.append((x, y))

        elif direction == "down":
            y = 15
            for x in range(16):
                if self.tiles[y][x] == "empty":
                    exits.append((x, y))

        elif direction == "left":
            x = 0
            for y in range(16):
                if self.tiles[y][x] == "empty":
                    exits.append((x, y))

        elif direction == "right":
            x = 15
            for y in range(16):
                if self.tiles[y][x] == "empty":
                    exits.append((x, y))

        return exits
    
