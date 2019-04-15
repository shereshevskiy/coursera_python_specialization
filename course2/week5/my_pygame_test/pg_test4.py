from random import randint
import pygame

pygame.init()
W = 400
H = 400
WHITE = (255, 255, 255)


class Car(pygame.sprite.Sprite):
    def __init__(self, x, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, 0))


sc = pygame.display.set_mode((W, H))

# координата x будет случайна
car1 = Car(randint(1, W), 'car1.png')

while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()

    sc.fill(WHITE)
    sc.blit(car1.image, car1.rect)
    pygame.display.update()
    pygame.time.delay(20)
    # машинка ездит сверху вниз
    if car1.rect.y < H:
        car1.rect.y += 2
    else:
        car1.rect.y = 0