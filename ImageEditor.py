import os # для получения функций операционной системы, получение путей к папкам
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from PyQt5.QtGui import QPixmap # оптимизированная для показа на экране картинка


from PIL import Image #основной класс для открытия и изменения картинок
#набор фильтров которые можно использовать для изменения картинок, что каждое из них делает можно глянуть в интернете
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)


app = QApplication([]) #создаем объект основного приложения
win = QWidget() #создаем основной виджет/окно нашего приложения
win.resize(700, 500) #изменяем размер нашего окна
win.setWindowTitle('Easy Editor') #тут указываем название нашего окошка
lb_image = QLabel("Картинка") #создаем простую надпись с текстом
btn_dir = QPushButton("Папка") #создаем кнопку, через которую будет выбирать папку для картинок
lw_files = QListWidget() #создаем объект в котором будет загружаться список всех файлов в папке

#блок кнопок для применения разных фильтров для картинок
btn_left = QPushButton("Лево")
btn_right = QPushButton("Право")
btn_flip = QPushButton("Зеркало")
btn_sharp = QPushButton("Резкость")
btn_bw = QPushButton("Ч/Б")


row = QHBoxLayout() # Основная строка
col1 = QVBoxLayout() # делится на два столбца
col2 = QVBoxLayout()
col1.addWidget(btn_dir) # в первом - кнопка выбора директории
col1.addWidget(lw_files) # и список файлов
col2.addWidget(lb_image) # вo втором - картинка
row_tools = QHBoxLayout()    # и строка кнопок, помещяем все кнопки на горизонтальную линию
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools) #добавляем нашу линию с кнопками на линию колонки 2

#основная линия
row.addLayout(col1, 20) # числа это процентное соотношение для кажной из линий или виджита который мы будет добавлять
row.addLayout(col2, 80)
win.setLayout(row) # ложим линию на наше основное окно


win.show() #показываем наше окно на котором у нас сейчас есть все линии с объектами


workdir = '' # переменная в которой будем хранить путь к выбранной папке с картинками

#функция которая получает на вход 2 аргумента
#1 - files, это список файлов, среди которых будем искать нужные нам
#2 - extensions, это список доступных расcширений (это то, что идет в конце имени файла "jjj.jpg", .jpg - это рассширение)
def filter(files, extensions):
   result = [] #создаем пустой результирующий список
   for filename in files: #перебераем весь списк файлов
       for ext in extensions: #для каждого имени файла перебераем все доступные расширения
           if filename.endswith(ext): #условие, что наше имя файла заканчивается на одно из расширений
               result.append(filename) #значит это нужный нам файл и добавляем имя этого файла в наш результирующий список
   return result #функция возвращает полученный список, как результат свой работы

#функция которая вызывает диалоговое окно, в котором мы выбираем путь к папке где у нас находятся картинка
def chooseWorkdir():
   global workdir #говорим, что в этой функции это имя переменной означает, что она глобальная, без этой дерективы у нас эта переменная будет локальной
   workdir = QFileDialog.getExistingDirectory() #вызваем диалог и получаем путь к папке

#функция чтения всех картинок из нашей папки и составления списка, который будет отображаться в виджите lw_files
def showFilenamesList():
   extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp'] #заполняем список значенимя доступных расширений, т.е. какого формата картинки мы сможем загружать
   chooseWorkdir() #вызов функции выбора папки
   filenames = filter(os.listdir(workdir), extensions) #вызов функции отбора нужных файлов и получения списка только с нужными файлами


   lw_files.clear() #этот метод очищает все содержимое нашего объекта со списками
   for filename in filenames: #заполняем теперь наш объект только нужными файлами
       lw_files.addItem(filename)


btn_dir.clicked.connect(showFilenamesList) #к кнопке "Папка" подключаем наше событие по выбору и формированию списка файлов

#описываем класс, в котором будет хранится текущая картинка, путь и имя файла и имя папки для сохранения измененых картинок
class ImageProcessor():
    #описываем конструктор
   def __init__(self):
       self.original_image = None #текущая картинка, значение None - это ни чего, т.к. мы пока не знаем какая картинка нам нужна
       self.dir = None #текущая деректория
       self.filename = None #текущее имя файла
       self.save_dir = "Modified/" #папка для сохранения изменненых картинок, значение этой папки меняться не будет

    #описываем функцию загрузки конкретной картинки, на вход передаем имя файла который надо загрузить
   def loadImage(self, filename):
       ''' при загрузке запоминаем путь и имя файла '''
       self.filename = filename #сохраняем внутри объекта имя файла картинки которую нужно загрузить
       fullname = os.path.join(workdir, filename) #os - это модуль для работы с операционной системой, path - это объект для работы с путями, join - это функция объединения
       self.original_image = Image.open(fullname) #через класс Image открываем картинку по полному пути и сохраняем эту картинку внутри нашего объекта

    #описываем функцию для сохранения изменной картинки в папке для измененных картинок
   def saveImage(self):
       ''' сохраняет копию файла в подпапке '''
       path = os.path.join(workdir, self.save_dir) # см 100 строчку, только тут получаем уже имя папки для сохранения измененных картинок
       if not(os.path.exists(path) or os.path.isdir(path)): #exists - это функция которая проверяет существование папки или файла по этому пути, isdir - это функция проверяет является ли этот путь, путем к папке
           os.mkdir(path) #если у нас нету папки, по пути, то мы ее тут создаем через функцию mkdir
       fullname = os.path.join(path, self.filename)

       self.original_image.save(fullname) #обращаемся к нашему сохраненому объекту картинка(создавали на 101 строке) и вызваем метод класса Image.save(путьДляСохранения)

    #описываем функцию для отображения картинки
    #на вход передается полный путь к картинке(path)
   def showImage(self, path):
       lb_image.hide() #скрываем наш виджет с просто текстом "картинка"
       pixmapimage = QPixmap(path) #создаем картинку оптимизированную для показа через виджиты в окнном приложении
       w, h = lb_image.width(), lb_image.height() #получаем нашу длину и ширину нашего виджита, что бы по ним отмаштабировать нашу картинку
       pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio) #маштабируем нашу картинку KeepAspectRatio - это сохранять пропорции картинки с учетом исходных размеров
       lb_image.setPixmap(pixmapimage) #загружаем нашу картинку на виджет где был изначально просто текст "картинка"
       lb_image.show() #показываем скрытый ранее виджет

    #описываем функцию для преобразования картинки в черно белую
   def do_bw(self):
       self.original_image = self.original_image.convert("L") #convert -это метод преобразования картинки, тут передаем "L", что бы она стала черно белой
       self.saveImage() #вызваем функцию сохранения измененной картинки
       image_path = os.path.join(workdir, self.save_dir, self.filename) #собираем полный путь из составляющих
       self.showImage(image_path) #показывем измененную картинку

    #описываем функцию поворота картинки на 90 градусов, поворот против часовой стрелки
   def do_left(self):
       self.original_image = self.original_image.transpose(Image.ROTATE_90)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)

    # описываем функцию поворота картинки на 270 градусов, поворот по часовой стрелки
   def do_right(self):
       self.original_image = self.original_image.transpose(Image.ROTATE_270)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)

    # описываем функцию отзеркаливания картинки
   def do_flip(self):
       self.original_image = self.original_image.transpose(Image.FLIP_LEFT_RIGHT)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)

    # описываем функцию блюра(разытие) картинки
   def do_sharpen(self):
       self.original_image = self.original_image.filter(SHARPEN)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)


#текущая рабочая картинка для работы
workimage = ImageProcessor() #создаем наш объект для работы преобразования конкретной картинки


#описываем функцию не относящуюся к классу
#функция загрузки выбранной картинки из списка доступных картинок, выбираем в виджите lw_files, см как он заполняется в showFilenamesList
def showChosenImage():
   if lw_files.currentRow() >= 0: #если есть вообще элементы списка и мы что то выбрали
       filename = lw_files.currentItem().text() #получаем имя файла из списка
       workimage.loadImage(filename) #загружаем оригинальную картинку
       workimage.showImage(os.path.join(workdir, workimage.filename)) #показываем оригинальную картинку

lw_files.currentRowChanged.connect(showChosenImage) #на событие выбора элемента мы подключаем нашу функцию, она будет срабатывать каждый раз когда вы будите переходить на запись очередную

#подключение к кнопкам преобразования, конкретных методов нашего объекта
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)


app.exec()# запуск самого приложения
