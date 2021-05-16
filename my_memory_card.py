#создай приложение для запоминания информации
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget,  QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QRadioButton, QGroupBox, QButtonGroup
    )
from random import (shuffle,randint)

class Question():
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3
 
question_list = []
 
question_list.append(Question('Государственный язык Бразилии', 'Португальский', 'Бразильский', 'Испанский', 'Итальянский'))
question_list.append(Question('Какой национальности не существует?', 'Смурфы', 'Энцы', 'Алеуты', 'Чулымцы'))
question_list.append(Question('Какой цвета нет на флаге России?', 'Зелёный', 'Синий', 'Красный', 'Белый'))
question_list.append(Question('Сколько официальных языков в Канаде?', '2', '3', '1', '4'))
question_list.append(Question('Какого цвета ёлка?', 'Зелёного', 'Синего', 'Красного', 'Белого'))

app = QApplication([])
main_win = QWidget()
main_win.resize(400, 400)
main_win.setWindowTitle('MemoryCard')
 
lbl_ans = QLabel("Здесь будет сложный вопрос")
btn_ans = QPushButton("Ответить")

# Группа вариантов ответа на вопрос
RadioGroupBox = QGroupBox("Варианты ответов")
rbtn_1 = QRadioButton('Вариант1')
rbtn_2 = QRadioButton('Вариант2')
rbtn_3 = QRadioButton('Вариант3')
rbtn_4 = QRadioButton('Вариант4')
 
layout_ans1 = QHBoxLayout()
layout_ans2 = QVBoxLayout()
layout_ans3 = QVBoxLayout()
 
layout_ans2.addWidget(rbtn_1)
layout_ans2.addWidget(rbtn_2)
layout_ans3.addWidget(rbtn_3)
layout_ans3.addWidget(rbtn_4)
 
RadioGroup = QButtonGroup() 
RadioGroup.addButton(rbtn_1)
RadioGroup.addButton(rbtn_2)
RadioGroup.addButton(rbtn_3)
RadioGroup.addButton(rbtn_4)
RadioGroup.setExclusive(True)
 
layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3)
 
RadioGroupBox.setLayout(layout_ans1)
RadioGroupBox.show()

# Группа ответ
AnsGroupBox = QGroupBox("Форма ответа")
lbl_IsAnswerRight = QLabel("Правильно/Неправильно")
lbl_RightAnswer = QLabel("Правильный ответ")
 
layout_ans4 = QVBoxLayout()
 
layout_ans4.addWidget(lbl_IsAnswerRight, alignment = (Qt.AlignLeft | Qt.AlignTop))
layout_ans4.addWidget(lbl_RightAnswer, alignment = Qt.AlignCenter)
 
AnsGroupBox.setLayout(layout_ans4)
AnsGroupBox.hide()

# Размещение лейаутов главного окна
layout_main = QVBoxLayout()
layoutH1 = QHBoxLayout()
layoutH2 = QHBoxLayout()
layoutH3 = QHBoxLayout()
 
layoutH1.addWidget(lbl_ans, alignment = Qt.AlignCenter)
layoutH2.addWidget(RadioGroupBox)
layoutH2.addWidget(AnsGroupBox)
layoutH3.addWidget(btn_ans)
 
layout_main.addLayout(layoutH1)
layout_main.addLayout(layoutH2)
layout_main.addLayout(layoutH3)
 
main_win.setLayout(layout_main)
main_win.show()
# закончили описание интерфейса
# начинается функциональная часть


def show_result():
    ''' показать панель ответов '''
    RadioGroupBox.hide()
    AnsGroupBox.show()
    print("Статистика")
    print("- правельных ответов:", main_win.score)
    print("- всего вопросов", main_win.total)
    print("Рейтинг",main_win.score / main_win.total * 100)
    btn_ans.setText("Следующий вопрос")

 
def show_question():
    ''' показать форму вопроса '''
    RadioGroupBox.show()
    AnsGroupBox.hide()
    btn_ans.setText("Ответить")
    # сбросить выбранную радио-кнопку
    RadioGroup.setExclusive(False) # сняли ограничения, чтобы можно было сбросить выбор радиокнопки
    rbtn_1.setChecked(False)
    rbtn_2.setChecked(False)
    rbtn_3.setChecked(False)
    rbtn_4.setChecked(False)
    RadioGroup.setExclusive(True) # вернули ограничения, теперь только одна радиокнопка может быть выбрана
 
def click_OK(): # функция выбора, какую форму показывать
    if btn_ans.text() == "Ответить":
        check_answer()
    elif  btn_ans.text() == "Следующий вопрос":
        next_question()


def next_question():
    curquestion = randint(0, len(question_list) - 1)
    main_win.total += 1
    if main_win.curquestion == len(question_list):
        main_win.curquestion = 0
    ask(question_list[curquestion])
    
 
answers = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]
 
def ask(q):
    ''' функция записывает значения вопроса и ответов в соответствующие виджеты, 
    при этом варианты ответов распределяются случайным образом'''
    lbl_ans.setText(q.question)
    lbl_RightAnswer.setText(q.right_answer)
    shuffle(answers)
    answers[0].setText(q.right_answer)
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)
    show_question()
 
def check_answer():
    '''Функция, проверяющая ответ верный или неверный'''
    if answers[0].isChecked():
        show_correct("Правильно!")
        main_win.score += 1
    else:
        if answers[1].isChecked() or answers[2].isChecked() or answers[3].isChecked():
            show_correct("Неверный ответ!")
 
def show_correct(res):
    res = res + "nСтатистика"
    lbl_IsAnswerRight.setText(res)
    show_result()

main_win.total = 0
main_win.score = 0

main_win.curquestion = -1
 
next_question() 
btn_ans.clicked.connect(click_OK) # подключаем функцию-обработчик
 
# запуск приложения
app.exec_()