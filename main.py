import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QTableWidget, QTableWidgetItem)
from PyQt5.Qt import Qt
import xlrd

# deck
from PyQt5.uic.properties import QtWidgets

deck = " ".join("encyclopedia").upper().split()

# hand
hand = " ".join("abcdefghijklmnopqrstuvwxyz?").upper().split()

# letter info
letterInfo = []

tempHand = hand

curWord = ""

# for labels
def update_lbl(QLabel: QLabel, text: str):
    QLabel.setText(text)
    QLabel.adjustSize()

# for table
def updateTable():
    for i in range(len(hand)):
        index = -1
        for j in range(len(letterInfo)):

            if str(letterInfo[j].letter).upper() == str(hand[i]):
                print("found at", j)
                index = j
        table.setItem(i, 0, QTableWidgetItem(letterInfo[index].letter))
        table.setItem(i, 1, QTableWidgetItem(letterInfo[index].damage))
        table.setItem(i, 2, QTableWidgetItem(letterInfo[index].word))
        table.setItem(i, 3, QTableWidgetItem(letterInfo[index].draw))
        table.setItem(i, 4, QTableWidgetItem(letterInfo[index].description))

# for data handling
def create_letters():
    wb = xlrd.open_workbook("LetterData.xls")
    sheet = wb.sheet_by_index(0)

    for i in range(1, 28):
        letterInfo.append(Letter(sheet.cell_value(i, 0).strip(),
                                 sheet.cell_value(i, 1),
                                 sheet.cell_value(i, 2),
                                 sheet.cell_value(i, 3),
                                 sheet.cell_value(i, 4)))
    print(letterInfo[10].damage)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

    def keyPressEvent(self, event):
        global curWord
        # handle word checking
        if 32 <= event.key() <= 126 and chr(event.key()) in hand:
            tempHand.remove(chr(event.key()))
            curWord = curWord + chr(event.key())
            update_lbl(typed, curWord)
            update_lbl(letterBank, str(tempHand))
        elif event.key() == Qt.Key_Backspace:
            if curWord:
                hand.append(curWord[-1])
                update_lbl(letterBank, str(tempHand))
                curWord = curWord[0:-1]
                update_lbl(typed, curWord)
        elif event.key() == Qt.Key_Enter:
            print("entered")
            # do smthn


class Letter:
    letter, description, damage, word, draw = "", "", 0, 0, 0

    def __init__(self, letter: str, damage: int, word: int, draw: int, description: str):
        self.letter = letter
        self.damage = damage
        self.word = word
        self.draw = draw
        self.description = description


create_letters()

app = QApplication(sys.argv)
w = MainWindow()
w.setGeometry(500, 500, 1000, 500)

# labels
typedLabel = QLabel(w)
typedLabel.move(0, 0)
typedLabel.setText("CURRENT WORD:")

typed = QLabel(w)
typed.move(125, 0)
typed.setText("type something")

letterLabel = QLabel(w)
letterLabel.move(0, 25)
letterLabel.setText("LETTER BANK: ")

letterBank = QLabel(w)
letterBank.move(125, 25)
letterBank.setText(str(hand))

# table
table = QTableWidget(w)
table.move(300, 0)
table.setColumnCount(5)
table.setRowCount(len(hand))
table.setMinimumWidth(700)
table.setMinimumHeight(500)
# Set the table headers
table.setHorizontalHeaderLabels(["Letter", "Damage", "+Word", "+Draw", "Ability Description"])
table.setColumnWidth(4, 300)

#scuffed way of unfocusing table rn. not optimal cause locks table
table.setEnabled(False)

updateTable()

w.show()

sys.exit(app.exec_())
