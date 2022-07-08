import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QTableWidget, QTableWidgetItem)
from PyQt5.Qt import Qt
import xlrd

# deck
from PyQt5.uic.properties import QtWidgets

from letter import Letter
from letterTable import LetterTable

deck = " ".join("encyclopedia").upper().split()

# hand
hand = " ".join("abcdefghijklmnopqrstuvwxyz?").upper().split()

# letter info
letter_info = []

tempHand = hand

curWord = ""

# for labels
def update_lbl(QLabel: QLabel, text: str):
    QLabel.setText(text)
    QLabel.adjustSize()

# for data handling
def create_letters():
    wb = xlrd.open_workbook("LetterData.xls")
    sheet = wb.sheet_by_index(0)

    for i in range(1, 28):
        letter_info.append(Letter(sheet.cell_value(i, 0).strip(),
                                 sheet.cell_value(i, 1),
                                 sheet.cell_value(i, 2),
                                 sheet.cell_value(i, 3),
                                 sheet.cell_value(i, 4)))
    print(letter_info[10].damage)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)

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
table = LetterTable(w)
table.updateTable(hand, letter_info)

w.show()

sys.exit(app.exec_())
