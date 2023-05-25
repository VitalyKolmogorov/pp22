from pygame import *
import time as t_t
from random import randint

#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, imageName, x, y, speed, wight, height):
        super().__init__()
        self.imageName = imageName
        self.image = transform.scale(image.load(imageName), (wight, height))
        self.speed = speed
        self.startTime = t_t.time()
        self.curTime = t_t.time()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.countResize = 0

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        if t_t.time() - self.curTime >= 0.2:
            self.image = transform.scale(image.load(self.imageName), (self.rect.width + self.speed, self.rect.height + self.speed))
            x = self.rect.x
            y = self.rect.y
            self.rect = self.image.get_rect()
            self.rect.x = x - int(self.speed/2)
            self.rect.y = y - int(self.speed/2)
            self.curTime = t_t.time()
            self.countResize += 1
        #  выкидываем из всех групп
        if self.countResize == 10:
            self.kill()

#Игровая сцена:
back = (200, 255, 255) # цвет фона (background)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
window.fill(back)

#флаги отвечающие за состояние игры
game = True
finish = False
clock = time.Clock()
FPS = 60

speed = 4
startSize = 10

def randCreate(groupBalls):
    ok = False
    while not ok:
        x = randint(0 + speed * 10, win_width - speed * 10)
        y = randint(0 + speed * 10, win_height - speed * 10)
        w2 = GameSprite('tenis_ball.png', x, y, speed, startSize, startSize)
        if not sprite.spritecollide(w2, groupBalls, False):
            ok = True
    return w2

balls = sprite.Group()

font.init()
font = font.Font(None, 35)
lose = font.render('PLAYER LOSE!', True, (180, 0, 0))
win = font.render('PLAYER WIN!', True, (180, 0, 0))

startTime = t_t.time()
curTime = t_t.time()
maxBalls = 10
score = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if not finish:
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                for b in balls.sprites():
                    if b.rect.collidepoint(e.pos):
                        b.kill()
                        score += 1

    if len(balls) < maxBalls and t_t.time() - curTime >= 0.4:
        balls.add(randCreate(balls))
        curTime = t_t.time()

    if not finish:
        window.fill(back)
        balls.update()
        balls.draw(window)
        if score == 10:
            window.blit(win, (200, 200))
            finish = True
        if t_t.time() - startTime > 5 and score < 10:
            window.blit(lose, (200, 200))
            finish = True

        window.blit(font.render('Очки: ' + str(score), True, (0, 0, 0)), (0, 0))

    display.update()
    clock.tick(FPS)
