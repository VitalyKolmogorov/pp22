from pygame import *
from random import randint

# фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# шрифты и надписи
font.init()
font_statistics = font.SysFont(None, 36)

score = 0  # сбито кораблей
lost = 0  # пропущено кораблей


# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        super().__init__()

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# класс главного игрока
class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        pass  # это без реализации, т.е. мы задумали такой метод, но пока как его сделать не знаем но он нам нужен в дальнейшем


# класс спрайта-врага
class Enemy(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


# Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

# создаем спрайты
ship = Player("rocket.png", 5, win_height - 100, 80, 100, 10)

# создаем противников
monsters = sprite.Group()  # создаем группу в которую будем добавлять новых противников
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
# Основной цикл игры:
run = True  # флаг сбрасывается кнопкой закрытия окна
while run:
    # событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        # обновляем фон
        window.blit(background, (0, 0))

        # пишем текст статистики на экране
        text_score = font_statistics.render("Счет: " + str(score), True, (255, 255, 255))
        window.blit(text_score, (10, 20))

        text_lose = font_statistics.render("Пропущено: " + str(lost), True, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # производим движения спрайтов
        ship.update()  # изменяем координаты корабля
        monsters.update()  # изменяем координаты всех противников в группе

        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()  # отрисовываем корабль
        monsters.draw(window) # отрисовываем всех противников в группе

        display.update()
    # цикл срабатывает каждую 0.05 секунд
    time.delay(50)
