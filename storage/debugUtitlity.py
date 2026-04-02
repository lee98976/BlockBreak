from storage.gameVars import *

def draw_debug_rect(screen, rect, camera):
    offset = rect.topleft - camera + vec(WIDTH/2, HEIGHT/2)
    debug_rect = pygame.Rect(offset, rect.size)
    pygame.draw.rect(screen, (0, 0, 0), debug_rect, 2)