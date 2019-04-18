import pygame
import os
import Objects
import ScreenEngine as SE
import Logic
import Service


SCREEN_DIM = (800, 600)
MINIMAP_DIM = (700, 500)
pygame.init()
gameDisplay = pygame.display.set_mode(SCREEN_DIM)
pygame.display.set_caption("MyRPG")
KEYBOARD_CONTROL = True

if not KEYBOARD_CONTROL:
    import numpy as np
    answer = np.zeros(4, dtype=float)

base_stats = {
    "strength": 20,
    "endurance": 20,
    "intelligence": 5,
    "luck": 5
}


def create_game(sprite_size=60):
    new_engine = Logic.GameEngine(sprite_size)
    new_hero = Objects.Hero(base_stats, Service.create_sprite(
        os.path.join("texture", "Hero.png"), sprite_size))
    Service.reload_game(new_engine, new_hero)

    new_drawer = SE.GameSurface((640, 480), pygame.SRCALPHA, (0, 480),
                                SE.ProgressBar((640, 120), (640, 0),
                                SE.InfoWindow((160, 600), (50, 50),
                                SE.MiniMap(MINIMAP_DIM, pygame.SRCALPHA, (0, 0),
                                SE.HelpWindow((700, 500), pygame.SRCALPHA, (0, 0),
                                SE.ScreenHandle((0, 0)))))))
    new_drawer.connect_engine(new_engine)
    return new_engine, new_drawer


def change_scale(add):
    engine.change_scale(add)
    engine.hero.icon = Service.create_sprite(
        os.path.join("texture", "Hero.png"), engine.sprite_size)
    drawer.connect_engine(engine)
    Service.service_init(engine.sprite_size, engine.map_size)


engine, drawer = create_game()

while engine.working:

    if KEYBOARD_CONTROL:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    engine.show_help = not engine.show_help
                if event.key == pygame.K_m:
                    engine.show_minimap = not engine.show_minimap
                if event.key == pygame.K_o:
                    change_scale(1)
                if event.key == pygame.K_i:
                    change_scale(-1)
                if event.key == pygame.K_r:
                    engine, drawer = create_game()
                if event.key == pygame.K_ESCAPE:
                    engine.working = False
                if engine.game_process:
                    if event.key == pygame.K_UP:
                        engine.move_up()
                    elif event.key == pygame.K_DOWN:
                        engine.move_down()
                    elif event.key == pygame.K_LEFT:
                        engine.move_left()
                    elif event.key == pygame.K_RIGHT:
                        engine.move_right()
                else:
                    if event.key == pygame.K_RETURN:
                        create_game()

    gameDisplay.blit(drawer, (0, 0))
    drawer.draw(gameDisplay)
    pygame.display.update()

pygame.display.quit()
pygame.quit()
exit(0)
