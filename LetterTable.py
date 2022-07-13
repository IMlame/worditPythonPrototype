from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

NUM_COLS = 6

#test commit comment

class LetterTable(QTableWidget):
    letter_order = []
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setColumnCount(NUM_COLS)
        # Set the table headers
        self.setHorizontalHeaderLabels(["Letter", "Damage", "+Word", "+Draw", "Status Types", "Ability Description"])
        self.setColumnWidth(5, 300)

        # unfocuses table
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

    def updateTable(self, hand: list, letter_info: dict):
        self.setRowCount(len(hand))
        for i in range(len(hand)):
            if hand[i] in letter_info:
                self.setItem(i, 0, QTableWidgetItem(letter_info[hand[i]].letter))
                self.setItem(i, 1, QTableWidgetItem(str(letter_info[hand[i]].damage)))
                self.setItem(i, 2, QTableWidgetItem(str(letter_info[hand[i]].word)))
                self.setItem(i, 3, QTableWidgetItem(str(letter_info[hand[i]].draw)))
                self.setItem(i, 4, QTableWidgetItem(str(letter_info[hand[i]].status_types)))
                self.setItem(i, 5, QTableWidgetItem(letter_info[hand[i]].description))

    def updateColor(self, cur_word):
        letter_arr = " ".join(cur_word).split()
        for i in range(self.rowCount()):
            if self.item(i, 0).text() in letter_arr:
                color = QtGui.QColor(0, 100, 0)
                letter_arr.remove(self.item(i, 0).text())
            else:
                color = QtGui.QColor(0, 0, 0)

            for j in range(self.columnCount()):
                self.item(i, j).setBackground(color)
