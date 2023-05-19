from pygame import *

# класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, image_name, x, y, speed, wight, height):
        super().__init__()

        self.image = transform.scale(image.load(image_name), (wight, height))
        self.speed = speed
 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    # добавляем стандартное движение
    def update(self):
        self.rect.x += self.speed
        self.rect.y += self.speed

# Игровая сцена:
back = (200, 255, 255) # цвет фона (background)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
window.fill(back)

# флаги отвечающие за состояние игры
game = True
finish = False
clock = time.Clock()
FPS = 60

ball = GameSprite('tenis_ball.png', 200, 200, 4, 50, 50)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.fill(back)
        ball.update()
        ball.reset()

    display.update()
    clock.tick(FPS)