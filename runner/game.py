from pygame import *
from random import randint, choice
import time as t

#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, imageName, x, y, wight, height):
        super().__init__()
        self.imageName = imageName
        self.image = transform.scale(image.load(imageName), (wight, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, imageName, x, y):
        super().__init__(imageName, x, y, 50, 50)
        self.dir = ''
        self.pos = 0
        self.score = 0

    def update(self):
        if self.dir == 'right' and self.pos <= 0:
            self.rect.x += 150
            self.pos += 1
        if self.dir == 'left' and self.pos >= 0:
            self.rect.x -= 150
            self.pos -= 1
        self.dir = ''
        r = sprite.spritecollide(self, coins, True)
        if len(r) > 0:
            self.score += 1

class AnimSprite(GameSprite):
    def __init__(self, x, y):
        super().__init__('coin.png', x, y, 60* 6, 55)
        self.maxCount = 6
        self.curCount = 0
        self.animList = []
        self.startTime = t.time()
        self.curTime = t.time()
        self.k = 0.2
        for i in range(self.maxCount):
            self.animList.append(transform.scale(self.image.subsurface(Rect(i * 60, 0, 60, 55)), (60*self.k, 55*self.k)))

    def update(self):
        if t.time() - self.curTime > 0.2:
            self.curTime = t.time()
            self.curCount += 1
            if self.curCount == self.maxCount:
                self.curCount = 0
        window.blit(self.animList[self.curCount], (self.rect.x, self.rect.y))

    def changeSize(self):
        if self.k < 1:
            self.k += 0.2
        self.animList.clear()
        self.curCount = 0
        for i in range(self.maxCount):
            self.animList.append(transform.scale(self.image.subsurface(Rect(i * 60, 0, 60, 55)), (60*self.k, 55*self.k)))

#Игровая сцена:
back = (200, 255, 255) # цвет фона (background)
win_width = 700
win_height = 600
window = display.set_mode((win_width, win_height))
window.fill(back)

#флаги отвечающие за состояние игры
game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
font1 = font.Font(None, 75)

def randCreate():
    x = choice((1, 2, 3))
    w2 = AnimSprite(150 * x, 200)
    coins.add(w2)

coins = sprite.Group()

def moveCoin(listCoin):
    for i in listCoin:
        i.changeSize()
        i.rect.y += 50
p1 = Player('box.png', 299 , win_height - 65)

curtime = t.time()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_LEFT:
                p1.dir = 'left'
            if e.key == K_RIGHT:
                p1.dir = 'right'



    if not finish:
        window.fill(back)
        if t.time() - curtime >= 1:
            randCreate()
            moveCoin(coins.sprites())
            curtime = t.time()
        coins.update()
        p1.update()
        p1.reset()
        window.blit(font1.render(str(p1.score), True, (0, 0, 0)), (0, 0))
    display.update()
    clock.tick(FPS)