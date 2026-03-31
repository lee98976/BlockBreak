import pygame

def processImage(path, scale):
    unscaled = pygame.image.load(path).convert_alpha()

    newWidth = int(unscaled.get_width() * scale)
    newHeight = int(unscaled.get_height() * scale)

    return pygame.transform.scale(unscaled, (newWidth, newHeight))