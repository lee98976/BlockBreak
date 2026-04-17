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

            if parts[1] == "center":
                material = parts[0]
                shape = "center"
                rotation = None
                variant = int(parts[2])

            elif parts[1] in ["corner", "edge", "straight", "end", "isolated"]:
                material = parts[0]
                shape = parts[1]

                if shape == "isolated":
                    rotation = 0
                    variant = int(parts[2])
                else:
                    rotation = int(parts[2])
                    variant = int(parts[3])

            else:
                continue

            img = processImage(os.path.join(path, file), 1)

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

        material = grid[y][x]

        # spike special case...
        if material in ["shortSpike", "tallSpike"]:
            up = self.is_solid(grid, x, y - 1)
            right = self.is_solid(grid, x + 1, y)
            down = self.is_solid(grid, x, y + 1)
            left = self.is_solid(grid, x - 1, y)

            # spike attaches to the FIRST solid side found
            if down:
                return ("edge", 0)     # facing up
            if right:
                return ("edge", 90)    # facing right
            if up:
                return ("edge", 180)   # facing down
            if left:
                return ("edge", 270)   # facing left

            return ("edge", 0)  # fallback

        up = self.get(material, grid, x, y - 1) == material
        right = self.get(material, grid, x + 1, y) == material
        down = self.get(material, grid, x, y + 1) == material
        left = self.get(material, grid, x - 1, y) == material

        # bitmask
        mask = (up << 0) | (right << 1) | (down << 2) | (left << 3)

        # =====================
        # ISOLATED
        if mask == 0:
            return ("isolated", 0)

        # =====================
        # END (1 connection)
        if mask in [1, 2, 4, 8]:
            rotations = {
                1: 180,    # up
                2: 90,   # right
                4: 0,  # down
                8: 270   # left
            }
            return ("end", rotations[mask])

        # =====================
        # STRAIGHT
        if mask in [1 | 4, 2 | 8]:  # vertical or horizontal
            if mask == (1 | 4):
                return ("straight", 0)   # vertical
            else:
                return ("straight", 90)  # horizontal

        # =====================
        # CORNERS (2 adjacent)
        corner_map = {
            1 | 2: 90,    # up + right
            2 | 4: 0,   # right + down
            4 | 8: 270,  # down + left
            8 | 1: 180   # left + up
        }
        if mask in corner_map:
            return ("corner", corner_map[mask])

        # =====================
        # EDGES (3 connections)
        edge_map = {
            2 | 4 | 8: 0,    # missing up
            1 | 4 | 8: 270,   # missing right
            1 | 2 | 8: 180,  # missing down
            1 | 2 | 4: 90   # missing left
        }
        if mask in edge_map:
            return ("edge", edge_map[mask])

        # =====================
        # FULL (center)
        if mask == 1 | 2 | 4 | 8:
            return ("center", None)

        # fallback (should never happen)
        return ("center", None)

    def get_tile_image(self, room, x, y):
        material = room.tiles[y][x]

        if material == "empty":
            return None

        key = (x, y)

        if key not in room.render_cache or (self.game.gameTime + x * 5 + y * 5) % self.refresh_rate == 0:
            shape, rotation = self.get_tile_type(room.tiles, x, y)

            material_tiles = self.tiles.get(material, {})

            # fallback priority
            if shape not in material_tiles:
                shape = "center"
                rotation = None

            if shape == "center":
                try:
                    img = random.choice(material_tiles["center"]["variants"])
                except:
                    # if tile doesn't exist, default to water center
                    img = self.tiles.get("water", {})["center"]["variants"][0]
            else:
                if rotation not in material_tiles[shape]:
                    rotation = list(material_tiles[shape].keys())[0]

                img = random.choice(material_tiles[shape][rotation])

            room.render_cache[key] = (img, rotation)

        return room.render_cache[key]
    

    def draw(self, room, camera, screen):
        for y, row in enumerate(room.tiles):
            for x, tile in enumerate(row):

                if tile == "empty":
                    continue

                rect = self.get_tile_rect(room.world_x, room.world_y, x, y)

                # full float calculation FIRST
                pos = rect.topleft - camera + pygame.Vector2(WIDTH/2, HEIGHT/2) + self.game.screen_shake_offset

                # THEN snap once at the very end
                draw_pos = (int(pos.x), int(pos.y))

                img, rotation = self.get_tile_image(room, x, y)

                if img:
                    screen.blit(img, draw_pos)


    def get_tile_rect(self, world_x, world_y, x, y):
        return pygame.Rect(
            world_x + x * TILE_SIZE,
            world_y + y * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )
    
    def is_solid(self, grid, x, y):
        if not (0 <= x < 16 and 0 <= y < 16):
            return True  # treat OOB as solid

        tile = grid[y][x]
        if (tile == "shortSpike" or tile == "tallSpike"): return False
        props = self.game.tile_properties.get(tile, {})

        return props.get("collide", False)