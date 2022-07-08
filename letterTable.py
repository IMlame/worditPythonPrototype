from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class LetterTable(QTableWidget):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setColumnCount(5)
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

                if letter_info[j].letter == str(hand[i]):
                    index = j
            self.setItem(i, 0, QTableWidgetItem(letter_info[index].letter))
            self.setItem(i, 1, QTableWidgetItem(letter_info[index].damage))
            self.setItem(i, 2, QTableWidgetItem(letter_info[index].word))
            self.setItem(i, 3, QTableWidgetItem(letter_info[index].draw))
            self.setItem(i, 4, QTableWidgetItem(letter_info[index].description))

    def updateColor(self, hand, cur_word):
        temp_cur_word = cur_word.copy()
        for i in range(len(hand)):
            print(hand[i], "in", str(cur_word))
            if hand[i] in cur_word:
                color = QtGui.QColor(0, 100, 0)
                cur_word.remove(hand[i])
            else:
                color = QtGui.QColor(0, 0, 0)

            for j in range(self.columnCount()):
                self.item(i, j).setBackground(color)

