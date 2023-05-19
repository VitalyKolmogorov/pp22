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

# класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
        def __init__(self,image_name, x, y, speed, wight, height, side):
            super().__init__(image_name, x, y, speed, wight, height)
            self.side = side
        def update(self):
            keys = key.get_pressed()
            # по умолчанию считаем, что кнопки для правого игрока
            k1 = K_UP
            k2 = K_DOWN
            # если у нас выбрана сторона лева, то мы берем другие кнопки
            if self.side == 'l':
                k1 = K_w
                k2 = K_s
            # алгоритм изменение положения у нас одинаковый для всех
            if keys[k1] and self.rect.y >= 5:
                self.rect.y -= self.speed
            if keys[k2] and self.rect.y <= win_height - 150:
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

#создания мяча и ракетки
racket1 = Player('racket.png', 30, 200, 4, 50, 150, 'l')
racket2 = Player('racket.png', 520, 200, 4, 50, 150, 'r')
ball = GameSprite('tenis_ball.png', 200, 200, 4, 50, 50)


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.fill(back)
        ball.update()
        ball.reset()
        racket1.update()
        racket2.update()
        racket1.reset()
        racket2.reset()

    display.update()
    clock.tick(FPS)