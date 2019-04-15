# здесь подключаются модули
import pygame

# здесь определяются константы, классы и функции
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)


# здесь происходит инициация, создание объектов и др.
pygame.init()

screen_size = (600, 400)

r1 = pygame.Rect((150, 20, 100, 75))

sc = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
clock = pygame.time.Clock()

# если надо до цикла отобразить объекты на экране
pygame.draw.rect(sc, (255, 255, 255), (20, 20, 100, 75))
pygame.draw.rect(sc, LIGHT_BLUE, r1, 8)

pygame.draw.lines(sc, WHITE, True, [[10, 10], [140, 70], [280, 20]], 2)
pygame.draw.aalines(sc, WHITE, False, [[10, 100], [140, 170], [280, 110]])
pygame.draw.circle(sc, PINK, (200, 100), 50, 10)
pygame.draw.ellipse(sc, GREEN, (10, 50, 280, 100))


pygame.display.update()

# главный цикл
while True:

    # задержка
    clock.tick(FPS)

    # цикл обработки событий
    for i in pygame.event.get():
        print(i)
        if i.type == pygame.QUIT:
            exit()

    # --------
    # изменение объектов и многое др.
    # pygame.draw.rect(sc, (64, 128, 255), (150, 20, 100, 75), 8)
    # --------

    # обновление экрана
    pygame.display.update()