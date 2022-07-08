from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class LetterTable(QTableWidget):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.move(300, 0)
        self.setColumnCount(5)
        self.setMinimumWidth(700)
        self.setMinimumHeight(500)
        # Set the table headers
        self.setHorizontalHeaderLabels(["Letter", "Damage", "+Word", "+Draw", "Ability Description"])
        self.setColumnWidth(4, 300)

        # scuffed way of unfocusing table rn. not optimal cause locks table
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

    def updateTable(self, hand, letter_info):
        self.setRowCount(len(hand))

        for i in range(len(hand)):
            index = -1
            for j in range(len(letter_info)):

                if str(letter_info[j].letter).upper() == str(hand[i]):
                    index = j
            self.setItem(i, 0, QTableWidgetItem(letter_info[index].letter))
            self.setItem(i, 1, QTableWidgetItem(letter_info[index].damage))
            self.setItem(i, 2, QTableWidgetItem(letter_info[index].word))
            self.setItem(i, 3, QTableWidgetItem(letter_info[index].draw))
            self.setItem(i, 4, QTableWidgetItem(letter_info[index].description))