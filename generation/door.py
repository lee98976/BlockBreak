import pygame
from entity import *

class Door(Entity):
    def __init__(self, game, room, pos, direction):
        super().__init__(game, game.doorSet, "door", 999, pos)

        self.room = room
        self.direction = direction

        # register self
        self.room.doors[direction]["entities"].append(self)


    def open(self):
        self.room.openDoor(self.direction)

    def update(self):
        self.renderAnim()