from pygame import *
from random import randint, choice
import time as t

move = 50

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
    def __init__(self, imageName, x, y, pName):
        super().__init__(imageName, x, y, move, move)
        self.dir = ''
        self.pName = pName
        self.createBoom = 0
        self.lose = False

    def update(self):
        saveX = self.rect.x
        saveY = self.rect.y
        if self.dir == 'up':
            self.rect.y -= move
        if self.dir == 'down':
            self.rect.y += move
        if self.dir == 'right':
            self.rect.x += move
        if self.dir == 'left':
            self.rect.x -= move
        self.dir = ''
        if sprite.groupcollide(p, dontMoveBlock, False, False) or sprite.groupcollide(p, boomBlocks, False, False):
            self.rect.x = saveX
            self.rect.y = saveY
    def boom(self):
        if self.createBoom == 0:
            b = Bomb(self.rect.x, self.rect.y, self.pName)
            bombs.add(b)
            self.createBoom = 1

boom_image = transform.scale(image.load('boom.png'), (move, move))

fires = sprite.Group()
class Bomb(GameSprite):
    def __init__(self, x, y, howCreate):
        self.howCreate = howCreate
        if howCreate == 'p1':
            imageName = 'B.png'
        else:
            imageName = 'R.png'
        super().__init__(imageName, x, y, move, move)
        self.curTime = t.time()

    def update(self):
        if 0.9 > t.time() - self.curTime > 0.8:
            self.image = boom_image

            startX = self.rect.x
            startY = self.rect.y
            if self.rect.colliderect(p1.rect):
                p1.lose = True;
            if self.rect.colliderect(p2.rect):
                p2.lose = True;

            self.rect.x = startX + move
            sprite.spritecollide(self, boomBlocks, True)
            r = sprite.spritecollide(self, dontMoveBlock, False)
            if len(r) == 0:
                f = GameSprite('fire_right.png', self.rect.x, self.rect.y, move, move)
                fires.add(f)

            if self.rect.colliderect(p1.rect):
                p1.lose = True;
            if self.rect.colliderect(p2.rect):
                p2.lose = True;

            self.rect.x = startX - move
            sprite.spritecollide(self, boomBlocks, True)
            r = sprite.spritecollide(self, dontMoveBlock, False)
            if len(r) == 0:
                f = GameSprite('fire_left.png', self.rect.x, self.rect.y, move, move)
                fires.add(f)

            if self.rect.colliderect(p1.rect):
                p1.lose = True;
            if self.rect.colliderect(p2.rect):
                p2.lose = True;

            self.rect.x = startX
            self.rect.y = startY + move
            sprite.spritecollide(self, boomBlocks, True)
            r = sprite.spritecollide(self, dontMoveBlock, False)
            if len(r) == 0:
                f = GameSprite('fire_down.png', self.rect.x, self.rect.y, move, move)
                fires.add(f)

            if self.rect.colliderect(p1.rect):
                p1.lose = True;
            if self.rect.colliderect(p2.rect):
                p2.lose = True;

            self.rect.y = startY - move
            sprite.spritecollide(self, boomBlocks, True)
            r = sprite.spritecollide(self, dontMoveBlock, False)
            if len(r) == 0:
                f = GameSprite('fire_up.png', self.rect.x, self.rect.y, move, move)
                fires.add(f)

            if self.rect.colliderect(p1.rect):
                p1.lose = True;
            if self.rect.colliderect(p2.rect):
                p2.lose = True;

            self.rect.x = startX
            self.rect.y = startY


        if t.time() - self.curTime >= 1:
            self.kill()
            fires.empty()
            if self.howCreate == 'p1':
                p1.createBoom = 0
            else:
                p2.createBoom = 0


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


dontMoveBlock = sprite.Group()

font.init()
font1 = font.Font(None, 75)
lose1 = font1.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = font1.render('PLAYER 2 LOSE!', True, (180, 0, 0))

def createBlock(x, y):
    b = GameSprite('stena.png', x, y, move, move)
    dontMoveBlock.add(b)

list_x_move = []
list_y_move = []
def createDontMoveBlock():
    x = 0
    y = 0
    for x in range(int(win_width / move)):
        list_x_move.append(x * move)
        for y in range(int(win_height / move)):
            list_y_move.append(y * move)
            if (y == 0 or y == int(win_height / move)-1) or (x == 0 or x == int(win_width / move) - 1):
                createBlock(x * move, y * move)
            else:
                if y % 2 != 0 and x % 2 == 0:
                     createBlock(x * move, y * move)

p1 = Player('p1.png', win_width - (move * 2),  win_height- (move * 2), 'p1')
p2 = Player('p2.png', move, move, 'p2')

p = sprite.Group()
p.add(p1)
p.add(p2)

bombs = sprite.Group()
def randCreate():
    ok = False
    while not ok:
        x = choice(list_x_move)
        y = choice(list_y_move)
        print(x, y)
        w2 = GameSprite('box.png', x, y, move, move)

        if not sprite.spritecollide(w2, dontMoveBlock, False) and not sprite.spritecollide(w2, p, False):
            ok = True
    return w2

boomBlocks = sprite.Group()

def createBoomBlock():
    for i in range(40):
        boomBlocks.add(randCreate())

createDontMoveBlock()
createBoomBlock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_UP:
                p1.dir = 'up'
            if e.key == K_DOWN:
                p1.dir = 'down'
            if e.key == K_LEFT:
                p1.dir = 'left'
            if e.key == K_RIGHT:
                p1.dir = 'right'
            if e.key == K_KP_0:
                p1.boom()


            if e.key == K_w:
                p2.dir = 'up'
            if e.key == K_s:
                p2.dir = 'down'
            if e.key == K_a:
                p2.dir = 'left'
            if e.key == K_d:
                p2.dir = 'right'
            if e.key == K_SPACE:
                p2.boom()

    if not finish:
        window.fill(back)
        p.update()
        p.draw(window)
        bombs.update()
        bombs.draw(window)
        dontMoveBlock.draw(window)
        boomBlocks.draw(window)
        fires.draw(window)
        window.blit(font.Font(None, 35).render('Игрок 2', True, (255, 0, 0)), (0, 0))
        window.blit(font.Font(None, 35).render('Игрок 1', True, (0, 0, 250)), (win_width - 100, win_height - 35))
        if p1.lose:
            finish = True
            window.blit(lose1, (150, 200))
        if p2.lose:
            finish = True
            window.blit(lose2, (150, 200))

    display.update()
    clock.tick(FPS)