from pygame import *
#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    #конструктор класса, описываем какие нам нужны аргументы
    #для создания спрайта, нам нужно: имя картинки, координаты х,у и скорость с которой будут перемещатся наши "картинки"
    def __init__(self, nameImage, x, y, speed):
        super().__init__()
        # тут мы создаем объект-картинку
        #transform это объект для преобрабозования объектов-картинок
        #scale - это метод маштабирования первый параметр который нужно передать это объект-картинку, второй список с размерами картинки (длина, ширина)
        #image - это объект для работы с картинками, через его метод load
        self.image = transform.scale(image.load(nameImage), (55, 55))
        #сохраняем свойство скорости, что бы использовать его в дальнейшем
        self.speed = speed
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        # перемещяем наш прямоугольник на нужные нам координаты
        self.rect.x = x
        self.rect.y = y

    # это мето которым мы будем на нашем главном окне(переменная window) рисовать картинку, по координатам
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
    # метод для изменения координат нашего объекта, так делается анимация перемещения
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5: # 5 - это граинца за которую мы не должны уехать, т.е. пока мы можем двигатся в рамках экрана мы двигаемся, когда дойдем до координаты х = 5 программа не даст нам пройди дальше влево
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80: #win_width - это переменная которая хранит ширину нашего окна, 80 - это размер спрайта который мы создадим позже, это нужно что бы вы когда правым краем своего персанажа подходите к правой части экрана то персонаж дальше не вдигается
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

#класс-наследник для спрайта-врага (перемещается сам)
class Enemy(GameSprite):
    side = "left"

    # метод для изменения координат нашего объекта, так делается анимация перемещения
    def update(self):
        if self.rect.x <= 470: #это граница до которой противник будет двигатся вправо
            self.side = "right"
        if self.rect.x >= win_width - 85: #это граница до которой противник будет двигатся влево
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

#класс для спрайтов-препятствий
class Wall(sprite.Sprite):
    def __init__(self, color_rgb, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_rgb = color_rgb
        self.width = wall_width
        self.height = wall_height
 
        # картинка стены - прямоугольник нужных размеров и цвета
        self.image = Surface([self.width, self.height]) #Surface - это объект поверхности/прямоуголинк
        self.image.fill((self.color_rgb))
 
        # каждый спрайт должен хранить свойство rect - прямоугольник
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#Игровая сцена создается как и во всех остальных проектах, тут ни чего нового:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("название")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))
# !!!!!!!!!!!!!!!!ПОМЕНЯЙ ЦВЕТ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
wall_color = (154, 205, 50)

# !!!!!!!!!!!!!!!!ПОМЕНЯЙ ТУТ КООРДИНАТЫ И РАЗМЕРЫ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
w1 = Wall(wall_color, 100, 20, 450, 10)
w2 = Wall(wall_color, 100, 480, 350, 10)
w3 = Wall(wall_color, 100, 20, 10, 380)
w4 = Wall(wall_color, 200, 130, 10, 350)
w5 = Wall(wall_color, 450, 130, 10, 360)
w6 = Wall(wall_color, 300, 20, 10, 350)
w7 = Wall(wall_color, 390, 120, 130, 10)

#Персонажи игры:
# !!!!!!!!!!!!!!!!ПОМЕНЯЙ ТУТ КООРДИНАТЫ ЕСЛИ МЕНЯЛ СТЕНЫ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
packman = Player('hero.png', 5, win_height - 80, 4)
monster = Enemy('cyborg.png', win_width - 80, 280, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

game = True # эта переменная отвечает, что у нас приложение запущено, когда значение этой переменной станет False, то приложение закроется
finish = False # эта переменная отвечает, что у нас происходит отрисовка всех наших объекто на сцене
clock = time.Clock()
FPS = 60

# тут мы создаем объект "перо", что бы им нарисовать текст как картинку, а не просто текст, как строка
font.init()
font = font.Font(None, 70) # None - тут означает системный шрифт по умолчанию, можете поменять на какой то свой
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

#музыка
mixer.init() # mixer - это объект для работы со звуком в библиотеке pygame, что бы с ним работать, его нужно сначала создать, init, этим и занимается
mixer.music.load('jungles.ogg') #music - это объект для фонового воспроизведения звука, т.е. он на повторе воспроизводится пока приложение будет открыто
mixer.music.play() #play собственно запускает фоновую музыку, одновременно можно включать только один фоновый звук, если хотите несколько, нужна очередь метод queue
# если в () ни чего не указывать, то запись воспроизводится 1 раз, если требуется зациклить, то передаем -1, любое положительное число будет означать повторы
# т.е. mixer.music.play(1) воспроизведет звук 2 раза, первый раз просто потому что play, 2 раз потому что передано число повтров

money = mixer.Sound('money.ogg') #Sound напротив нужен для однократного воспроизведения звука
kick = mixer.Sound('kick.ogg')

#основной цикл игры
while game:
    # обход всех событий которые сейчас происходят с нашим окном
    for e in event.get():
        if e.type == QUIT: # если мы нажали на крестик, то мы должны завешрить нашу программу
            game = False
    # тут у нас начинается отрисовка всех объектов
    if finish != True:
        window.blit(background,(0, 0)) # сначала рисуем зайдний фон, что бы все предыдущие рисунки были "удалины"
        packman.update() # update смотри описание метода
        monster.update() # update смотри описание метода
        
        packman.reset() # reset смотри описание метода
        monster.reset()
        final.reset() 
        
        w1.reset()
        w2.reset()
        w3.reset()
        w4.reset()
        w5.reset()
        w6.reset()
        w7.reset()

        #Ситуация "Проигрыш"
        #collide_rect - это функция проверяющая столкновение 2 спрайтов, если она возвращает True, значит эти спрайты столкнулись
        if sprite.collide_rect(packman, monster) \
                or sprite.collide_rect(packman, w1) \
                or sprite.collide_rect(packman, w2)\
                or sprite.collide_rect(packman, w2)\
                or sprite.collide_rect(packman, w3)\
                or sprite.collide_rect(packman, w4)\
                or sprite.collide_rect(packman, w5)\
                or sprite.collide_rect(packman, w6)\
                or sprite.collide_rect(packman, w7):
            finish = True # заканчиваем прорисовку, но приложени продолжит работать
            window.blit(lose, (200, 200)) # отображаем экран проигрыша
            kick.play() # включаем музыку

        #Ситуация "Выигрыш", все тоже самое, только картинка другая и звук
        if sprite.collide_rect(packman, final):
            finish = True
            window.blit(win, (200, 200))
            money.play()

    display.update()
    clock.tick(FPS)
