import pygame
import heapq
from pygame.locals import *

from storage.animatedObject import AnimatedObject
from storage.gameVars import *

TILE_SIZE = 32

class Entity(AnimatedObject):
    def __init__(self, game, animSet, name, hp, pos):
        super().__init__(animSet)
        self.hp = hp
        self.game = game
        self.name = name
        self.invFrames = 0
        self.dead = False
        self.vel = vec(0, 0)
        
        self.pos = vec(pos)
        self.rect.center = self.pos
        self.room = game.get_current_room(self)

        self.path = []
        self.pathTimer = 0
        self.throughNode = (0, 0)


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
        room = self.game.get_current_room(self)
        for wall in room.wall_rects + room.door_rects:
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

    def world_to_grid(self, room, pos):
        local_x = pos.x - room.world_x
        local_y = pos.y - room.world_y

        return int(local_x // TILE_SIZE), int(local_y // TILE_SIZE)

    def grid_to_world(self, room, x, y):
        return vec(
            room.world_x + x * TILE_SIZE + TILE_SIZE // 2,
            room.world_y + y * TILE_SIZE + TILE_SIZE // 2
        )

    def is_walkable(self, room, x, y):
        if not (0 <= x < 16 and 0 <= y < 16):
            return False
        return room.tiles[y][x] == "empty"
    
    # pretty simple, just checks 12 points along the line from start to end and check if they
    # are occupied (like a raycast...)
    def has_line_of_sight(self, room, start, end):
        steps = 16
        for i in range(steps):
            t = i / steps
            pos = start.lerp(end, t)
            gx, gy = self.world_to_grid(room, pos)
            if not self.is_walkable(room, gx, gy):
                return False
        return True
    
    import heapq

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan

    def astar(self, room, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        g_score = {start: 0}


        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                # reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            x, y = current
            neighbors = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]

            for nx, ny in neighbors:
                if not self.is_walkable(room, nx, ny):
                    continue

                new_g = g_score[current] + 1

                if (nx, ny) not in g_score or new_g < g_score[(nx, ny)]:
                    g_score[(nx, ny)] = new_g
                    priority = new_g + self.heuristic((nx, ny), goal)
                    heapq.heappush(open_set, (priority, (nx, ny)))
                    came_from[(nx, ny)] = current

        return []
    
    # def get_direction_to_room(self, current_room, target_room):
    #     rx, ry = current_room.grid_pos
    #     px, py = target_room.grid_pos

    #     dx = px - rx
    #     dy = py - ry

    #     if abs(dx) >= abs(dy):
    #         return "right" if dx > 0 else "left"
    #     else:
    #         return "down" if dy > 0 else "up"
    
    # def get_exit_target(self, room, target_room):
    #     direction = self.get_direction_to_room(room, target_room)
    #     exits = room.get_exit_tiles(room, direction)

    #     if not exits:
    #         return self.pos  # fallback

    #     # choose closest exit
    #     best = min(exits, key=lambda t: (self.grid_to_world(room, *t) - self.pos).length())
    #     return self.grid_to_world(room, *best)

    def get_navigation_target(self, target_pos):
        room = self.game.get_current_room(self)

        # default behavior = direct movement
        if self.has_line_of_sight(room, self.pos, target_pos):
            return target_pos, True
        
        # make sure they arent in seperate rooms.
        # if they are, seek door instead.

        inSeperateRooms = False
        player_room = self.game.get_current_room(self.game.player)

        player_room = self.game.get_current_room(self.game.player)

        if room != player_room:
            room_path = self.room_astar(room, player_room)
            inSeperateRooms = True

            if room_path:
                next_room = room_path[0]
                target_pos, direction = self.get_exit_toward_room(room, next_room)
            else:
                # if there is no room path, just stop moving
                return self.pos, True

        # if not in line of sight, pathfind 
        self.pathTimer -= 1

        if self.pathTimer <= 0 or not self.path:
            start = self.world_to_grid(room, self.pos)
            goal = self.world_to_grid(room, target_pos)

            self.path = self.astar(room, start, goal)
            self.pathTimer = 20

            # add adjustment to path to go through door
            if len(self.path) > 0 and inSeperateRooms:
                if direction == "up":
                    newNode = (self.path[-1][0], self.path[-1][1] - 1)
                elif direction == "down":
                    newNode = (self.path[-1][0], self.path[-1][1] + 1)
                elif direction == "left":
                    newNode = (self.path[-1][0] - 1, self.path[-1][1])
                elif direction == "right":
                    newNode = (self.path[-1][0] + 1, self.path[-1][1])
                self.path.append(newNode)
                self.throughNode = newNode
            else:
                self.path.append(self.throughNode)


        if self.path:
            lookahead = min(1, len(self.path) - 1)
            tx, ty = self.path[lookahead]
            return self.grid_to_world(room, tx, ty), False

        return target_pos, False
    
    def draw_debug_path(self, room, screen, camera):
        if not self.path:
            return

        for (x, y) in self.path:
            rect = pygame.Rect(
                room.world_x + x * TILE_SIZE,
                room.world_y + y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )

            # convert to screen space (same way you render entities)
            offset = rect.topleft - camera + vec(WIDTH/2, HEIGHT/2)

            pygame.draw.rect(screen, (0, 255, 0), (*offset, TILE_SIZE, TILE_SIZE), 2)
    
    def get_neighbors(self, room):
        x, y = room.grid_pos
        neighbors = []

        directions = {
            "up": (x, y-1),
            "down": (x, y+1),
            "left": (x-1, y),
            "right": (x+1, y)
        }

        for dir, (nx, ny) in directions.items():
            neighbor = self.game.rooms.get((nx, ny))
            if not neighbor:
                continue

            # 🔥 check if connection exists via tiles
            if room.get_exit_tiles(dir):  # you can implement this via edge tiles
                neighbors.append(neighbor)

        return neighbors

    def room_astar(self, start_room, goal_room):
        open_set = []

        # 🔥 counter to break ties
        if not hasattr(self, "_astar_counter"):
            self._astar_counter = 0

        self._astar_counter += 1
        heapq.heappush(open_set, (0, self._astar_counter, start_room))

        came_from = {}
        g_score = {start_room: 0}

        while open_set:
            _, _, current = heapq.heappop(open_set)

            if current == goal_room:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for neighbor in self.get_neighbors(current):
                new_g = g_score[current] + 1

                if neighbor not in g_score or new_g < g_score[neighbor]:
                    g_score[neighbor] = new_g
                    priority = new_g  # no heuristic needed for rooms

                    self._astar_counter += 1
                    heapq.heappush(open_set, (priority, self._astar_counter, neighbor))

                    came_from[neighbor] = current

        return []
    
    def get_exit_toward_room(self, current_room, next_room):
        cx, cy = current_room.grid_pos
        nx, ny = next_room.grid_pos

        if nx > cx:
            direction = "right"
        elif nx < cx:
            direction = "left"
        elif ny > cy:
            direction = "down"
        else:
            direction = "up"

        exits = current_room.get_exit_tiles(direction)

        if not exits:
            return self.pos, None

        best = min(exits, key=lambda t: (self.grid_to_world(current_room, *t) - self.pos).length())
        return self.grid_to_world(current_room, *best), direction