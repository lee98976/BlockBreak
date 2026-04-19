
import pygame
from pygame.locals import *
import sys

from storage.gameVars import *
from game_manager import Game
from storage.debugUtitlity import *
from entities.pickups import HealthPack

pygame.init()
clock = pygame.time.Clock()

realScreen = pygame.display.set_mode((WIDTH * UPSCALE, HEIGHT * UPSCALE), pygame.SRCALPHA)
screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

pygame.display.set_caption("Block Dash")

# CHANGE THIS VARIABLE TO LOAD DIFFERENT LEVELS
CURRENT_LEVEL = 1

game = Game(screen, level=CURRENT_LEVEL)

while True:
    dt = clock.tick(FPS) / 1000.0

    # regular pygame exit check
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game.state == "game":
                    game.capturePauseNextFrame = True
                elif game.state == "pause":
                    game.state = "game"
        
        game.dialogue.handle_input(event)

    if game.state == "menu":
        screen.fill((255, 255, 255))
        game.menu.update(events, dt)
        game.menu.draw(screen)
    elif game.state == "pause":
        screen.fill((255, 255, 255))
        game.pauseMenu.update(events, dt)
        game.pauseMenu.draw(screen)
    elif game.state ==  "game":

        # obselete boss code
        # if game.miniBoss1.dead and game.miniBoss2.dead and not game.has_boss_activated:
        #     game.boss.activate()
        #     game.has_boss_activated = True

        # game.boss.checkDashDamage(game.player)

        # if game.boss.deadCheck():
        #     game.boss.takeDamage(9999)

        # player and enemy interaction...
        hits = pygame.sprite.spritecollide(game.player, game.enemy_sprites, False)

        for enemy in hits:
            if game.player.isDashing:
                enemy.takeDamage(1)
            elif hasattr(enemy, "isHarmful") and enemy.isHarmful:
                game.player.takeDamage(1, 60)

        # player and friendly interaction
        for sprite in game.friendly_sprites:
            if isinstance(sprite, HealthPack):
                if game.player.rect.colliderect(sprite.rect):
                    if game.player.hp < 5:
                        game.player.takeDamage(-1, 0)
                        sprite.kill()
        
        # interaction with interactables
        hits2 = pygame.sprite.spritecollide(game.player, game.interactables, False)
        for obj in hits2:
            if game.player.isDashing:
                obj.takeDamage(1)


        # rudimentary screen shake
        game.update_screen_shake()
        offset = game.screen_shake_offset

        game.update_camera()
        screen.fill((255, 255, 255))
        realScreen.fill((255, 255, 255))

        game.friendly_sprites.update(dt)
        game.enemy_sprites.update(dt)
        game.ui_sprites.update(dt)
        game.interactables.update(dt)

        cam = game.camera
        center = vec(WIDTH / 2, HEIGHT / 2)
        offset = vec(int(offset.x), int(offset.y))  # ensure integer

        # TODO: smart loading AND smart enemy rendering
        for room in game.rooms.values():
            room.update()
            game.tileHandler.draw(room, game.camera, screen)

        for s in game.ui_sprites:
            pos = s.rect.topleft - (vec(s.image.get_size()) - vec(s.rect.size)) // 2 + offset
            draw_pos = (int(pos.x), int(pos.y))
            screen.blit(s.image, draw_pos)
        for s in game.interactables:
            pos = s.rect.topleft - cam + center - (vec(s.image.get_size()) - vec(s.rect.size)) // 2 + offset
            draw_pos = (int(pos.x), int(pos.y))
            screen.blit(s.image, draw_pos)
        for s in game.friendly_sprites:
            pos = s.rect.topleft - cam + center - (vec(s.image.get_size()) - vec(s.rect.size)) // 2 + offset
            draw_pos = (int(pos.x), int(pos.y))
            screen.blit(s.image, draw_pos)
        for s in game.enemy_sprites:
            pos = s.rect.topleft + s.shakeOffset - cam + center - (vec(s.image.get_size()) - vec(s.rect.size)) // 2 + offset
            draw_pos = (int(pos.x), int(pos.y))
            screen.blit(s.image, draw_pos)

        # vfx rendering!
        game.vfxManager.update(dt) # TODO use shaders to disort larger screen


        for p in game.vfxManager.particles:
            p.draw(screen, cam)

        screen.blit(game.vfxManager.apply_shockwaves(screen), (0, 0))


        # TODO draw boss lasers

        game.gameTime += 1

        # room = game.get_current_room()
        
        # print("pos:", game.player.pos)
        # print("rect.center:", game.player.rect.center)
        # print("rect.topleft:", game.player.rect.topleft)

    # fading
    if game.fading:
        game.fade_alpha += (256 - game.fade_alpha) * (game.fade_speed)

        if game.fade_alpha >= 255:
            game.fade_alpha = 0
            game.fading = False

            # switch state AFTER fade completes
            game.state = game.fade_target
            game.fade_target = None
            print(game.state)
    
    if getattr(game, "capturePauseNextFrame", False):
        game.pauseMenu.pauseSurface = screen.copy()
        game.capturePauseNextFrame = False
        game.state = "pause"
    
    if game.fade_alpha > 0:
        fade_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        fade_surface.fill((0, 0, 0, int(game.fade_alpha)))
        screen.blit(fade_surface, (0, 0))
        print(game.fade_alpha)

    scaled = pygame.transform.scale(screen, (WIDTH * UPSCALE, HEIGHT * UPSCALE))
    realScreen.blit(scaled, (0,0))

    # dialogue rendering! (should happen after vfx rendering)
    if game.state == "game":
        game.dialogue.update(dt)
        game.dialogue.draw(realScreen, dt)

    pygame.display.update()