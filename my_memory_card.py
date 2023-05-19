from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import *
from random import shuffle

class Question():
    def __init__(self, quest, right_answer, wrong1, wrong2, wrong3):
        self.quest = quest
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3


app = QApplication([]) 

main_win = QWidget() 
main_win.setWindowTitle('Конкурс от Crazy People') 

question = QLabel('В каком году канал получил «золотую кнопку» от YouTube?') 
button = QPushButton('asdsa')

#создаем группу
RadioGroupBox = QGroupBox('НАЗАВАНИЕ ГРУППЫ')

# создаем элементы для группы
btn_answer1 = QRadioButton('2005') 
btn_answer2 = QRadioButton('2010') 
btn_answer3 = QRadioButton('2015') 
btn_answer4 = QRadioButton('2020') 

answers = [btn_answer1, btn_answer2, btn_answer3, btn_answer4]


RadioGroup = QButtonGroup()
RadioGroup.addButton(btn_answer1)
RadioGroup.addButton(btn_answer2)
RadioGroup.addButton(btn_answer3)
RadioGroup.addButton(btn_answer4)

def checkedFalse():
    RadioGroup.setExclusive(False)
    btn_answer1.setChecked(False)
    btn_answer2.setChecked(False)
    btn_answer3.setChecked(False)
    btn_answer4.setChecked(False)
    RadioGroup.setExclusive(True)

def viewResult():
    check_answer()
    RadioGroupBox.hide()#скрыть ответы 
    RadioGroupBoxResult.show()#показать результат
    button.setText('Следующий вопрос')#поменять надпись
    checkedFalse()

#переменная отвечающая за текущий вопрос, -1 означает вопрос еще не задавался
main_win.cur_question = -1

def viewAnswer():
    main_win.cur_question += 1
    ask(list_question[main_win.cur_question])
    RadioGroupBox.show()#скрыть ответы 
    RadioGroupBoxResult.hide()#показать результат
    button.setText('Ответ')#поменять надпись

def viewWin():
    if button.text() == 'Ответ':
        viewResult()
    else:
        viewAnswer() 

def ask(obj_quest):
    #мешаем кнопки
    shuffle(answers)
    question.setText(obj_quest.quest)
    answers[0].setText(obj_quest.right_answer)
    answers[1].setText(obj_quest.wrong1)
    answers[2].setText(obj_quest.wrong2)
    answers[3].setText(obj_quest.wrong3)

def check_answer():
    if answers[0].isChecked():
        trueOrFalse.setText('Правильон')
    else:
        trueOrFalse.setText('не правельно')
        rightAnswer.setText('Правильный ответ: ' + answers[0].text()) 



button.clicked.connect(viewWin)

RG_H1 = QHBoxLayout()

RG_V1 = QVBoxLayout()
RG_V2 = QVBoxLayout()

RG_V1.addWidget(btn_answer1, alignment = Qt.AlignCenter) 
RG_V1.addWidget(btn_answer2, alignment = Qt.AlignCenter) 

RG_V2.addWidget(btn_answer3, alignment = Qt.AlignCenter) 
RG_V2.addWidget(btn_answer4, alignment = Qt.AlignCenter) 

RG_H1.addLayout(RG_V1)
RG_H1.addLayout(RG_V2)

RadioGroupBox.setLayout(RG_H1)

layout_main = QVBoxLayout()

RadioGroupBoxResult = QGroupBox('Результат ответа')
Result_Layout = QVBoxLayout()
trueOrFalse = QLabel('Правльно/неправильно')
rightAnswer = QLabel('222')
Result_Layout.addWidget(trueOrFalse)
Result_Layout.addWidget(rightAnswer)
RadioGroupBoxResult.setLayout(Result_Layout)

layout_main.addWidget(question, alignment = Qt.AlignCenter)
layout_main.addWidget(RadioGroupBox, alignment = Qt.AlignCenter)
layout_main.addWidget(RadioGroupBoxResult, alignment = Qt.AlignCenter)
layout_main.addWidget(button, alignment = Qt.AlignCenter)
RadioGroupBoxResult.hide()


main_win.setLayout(layout_main) 
main_win.show() 

#создаем список вопросов
list_question = []
list_question.append(Question('Вопрос 1', '1', '2', '3', '4'))
list_question.append(Question('Вопрос 2', '1', '2', '3', '4'))
list_question.append(Question('Вопрос 3', '1', '2', '3', '4'))
list_question.append(Question('Вопрос 4', '1', '2', '3', '4'))
list_question.append(Question('Вопрос 5', '1', '2', '3', '4'))
list_question.append(Question('Вопрос 6', '1', '2', '3', '4'))

viewAnswer()

app.exec_()