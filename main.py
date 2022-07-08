import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QTableWidget, QTableWidgetItem)
from PyQt5.Qt import Qt
import xlrd

import letter
from letterTable import LetterTable

# will be drawn for
deck = " ".join("encyclopedia").upper().split()
# currently in deck
tempdeck = deck
# hand
hand = " ".join("aaaabbc").upper().split()
# currently in hand (decreases in size as letters are typed, increases in size when backspace is pressed)
temp_hand = hand.copy()

# letter info from LetterData.xsl
letter_info = letter.import_letter_data()

cur_word = ""


def update_lbl(qlabel: QLabel, text: str):
    qlabel.setText(text)
    qlabel.adjustSize()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)

    def keyPressEvent(self, event):
        global cur_word
        # handle word checking
        if 32 <= event.key() <= 126 and chr(event.key()) in temp_hand:
            # update typed
            cur_word = cur_word + chr(event.key())
            update_lbl(typed, cur_word)
            # update letter bank
            temp_hand.remove(chr(event.key()))
            update_lbl(letterBank, str(temp_hand))
            # change table row color
            table.updateColor(hand, " ".join(cur_word).split())
            # TODO:
            #  1. update damage
        elif event.key() == Qt.Key_Backspace:
            if cur_word:
                # update letter bank
                temp_hand.append(cur_word[-1])
                update_lbl(letterBank, str(temp_hand))
                # update typed
                cur_word = cur_word[0:-1]
                update_lbl(typed, cur_word)
                # change table row color
                table.updateColor(hand, " ".join(cur_word).split())
        elif event.key() == Qt.Key_Return:
            # TODO:
            #  1. check word is valid
            #  2. deal damage + special effects
            #     Lots of work needed to be done here (implementing each letter's unique abilities)
            #  3. set hand to temp_hand
            #  4. draw cards based on +draw cards (don't reshuffle deck)
            #  5. decrement/increment word count

            print("entered")

app = QApplication(sys.argv)
w = MainWindow()
w.setGeometry(0, 0, 1280, 720)

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
table.move(580, 0)
table.setMinimumWidth(700)
table.setMinimumHeight(720)
table.updateTable(hand, letter_info)
table.updateColor(hand, " ".join(cur_word).split())

# TODO:
#  1. Player healthbar
#  2. Boss healthbar
#  3. Damage display (current calculated damage with word that is currently typed)
#  4. word_count display (denotes number of words that stil can be made)
#  5. level up menu (3 panels, option 1: increase word length cap, option 2: increase starting hand size, option 3: increase health)
#  6. shop keeper?
w.show()

sys.exit(app.exec_())
