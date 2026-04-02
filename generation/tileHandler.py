import os
import pygame
import random

from storage.imageUtility import *
from storage.gameVars import *
from storage.debugUtitlity import *

class TileHandler:
    def __init__(self, game):
        self.tiles = self.load_tiles("assets/tiles")
        self.game = game

        self.refresh_rate = 80

    def load_tiles(self, path):
        tiles = {}

        for file in os.listdir(path):
            if not file.endswith(".png"):
                continue

            name = file.replace(".png", "")
            parts = name.split("_")

            if "center" in parts:
                material = parts[0]
                shape = "center"
                variant = int(parts[-1])
                rotation = None
            elif "corner" in parts:
                material = parts[0]
                shape = "corner"
                rotation = int(parts[2])
                variant = int(parts[3])
            elif "edge" in parts:
                material = parts[0]
                shape = "edge"
                rotation = int(parts[2])
                variant = int(parts[3])
            else:
                continue

            img = processImage(os.path.join(path, file), 4)

            tiles.setdefault(material, {})
            tiles[material].setdefault(shape, {})

            if shape == "center":
                tiles[material][shape].setdefault("variants", [])
                tiles[material][shape]["variants"].append(img)
            else:
                tiles[material][shape].setdefault(rotation, [])
                tiles[material][shape][rotation].append(img)

        return tiles

    def get(self, defaultMaterial, grid, x, y):
        if 0 <= x < 16 and 0 <= y < 16:
            return grid[y][x]
        return defaultMaterial

    def get_tile_type(self, grid, x, y):
        material = grid[y][x]

        up = self.get(material, grid, x, y - 1) == material
        down = self.get(material, grid, x, y + 1) == material
        left = self.get(material, grid, x - 1, y) == material
        right = self.get(material, grid, x + 1, y) == material


        # 0   = upper-left
        # 90  = lower-left
        # 180 = lower-right
        # 270 = upper-right

            # --- CORNERS (strict) ---
        if not up and not left:
            return ("corner", 0)
        if not left and not down:
            return ("corner", 90)
        if not down and not right:
            return ("corner", 180)
        if not right and not up:
            return ("corner", 270)

        # --- EDGES ---
        if not up:
            return ("edge", 0)
        if not left:
            return ("edge", 90)
        if not down:
            return ("edge", 180)
        if not right:
            return ("edge", 270)

        # --- CENTER ---
        return ("center", None)

    def get_tile_image(self, room, x, y):
        material = room.tiles[y][x]

        if material == "empty":
            return None

        key = (x, y)

        if key not in room.render_cache or (self.game.gameTime + x * 5 + y * 5) % self.refresh_rate == 0:
            shape, rotation = self.get_tile_type(room.tiles, x, y)

            if shape == "center":
                img = random.choice(self.tiles[material]["center"]["variants"])
            else:
                img = random.choice(self.tiles[material][shape][rotation])

            room.render_cache[key] = img

        return room.render_cache[key]
    

    def draw(self, room, camera):
        for y, row in enumerate(room.tiles):
            for x, tile in enumerate(row):

                if tile == "empty":
                    continue

                rect = self.get_tile_rect(room.world_x, room.world_y, x, y)


                offset = rect.topleft - camera + pygame.Vector2(WIDTH/2, HEIGHT/2)
                screen_pos = (offset.x, offset.y)

                img = self.get_tile_image(room, x, y)

                if img:
                    self.game.screen.blit(img, screen_pos)

                # draw_debug_rect(self.game.screen, rect, self.game.camera)


    def get_tile_rect(self, world_x, world_y, x, y):
        return pygame.Rect(
            world_x + x * 32,
            world_y + y * 32,
            32,
            32
        )