import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel)
from PyQt5.Qt import Qt
import Letter
from LetterTable import LetterTable
import random

# will be drawn for
f = open("deck.txt", "r")
tempdeck = f.read()
f.close()
deck = tempdeck.split(",")
# currently in deck
# hand
hand = random.sample(deck,5)
# currently in hand (decreases in size as letters are typed, increases in size when backspace is pressed)
# letter info from LetterData.xsl
letter_info = Letter.import_letter_data()

cur_word = ""
dis_cur_word = ""

def valid_word(word: str):
    dicFile = open("dictionary.txt", "r")
    lines = dicFile.read().split('\n')
    dicFile.close()
    if word.upper() in lines:
        print("cool")
        return True
    print("not cool")
    return False

def update_lbl(qlabel: QLabel, text: str):
    qlabel.setText(text)
    qlabel.adjustSize()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)

    def keyPressEvent(self, event):
        global cur_word
        global dis_cur_word
        # handle word checking
        if 32 <= event.key() <= 126 and (chr(event.key()) in hand):
            # update typed
            cur_word = cur_word + chr(event.key())
            dis_cur_word = dis_cur_word + chr(event.key())
            update_lbl(typed, dis_cur_word)
            hand.remove(chr(event.key()))
            update_lbl(letter_bank, str(hand))
            # change table row color
            table.updateColor(hand, " ".join(dis_cur_word).split())
            # TODO:
            #  1. update current damage indicator
        elif 32 <= event.key() <= 126 and not (chr(event.key()) in hand) and ("?" in hand):
            # update typed
            cur_word = cur_word + "?"
            dis_cur_word = dis_cur_word + chr(event.key())
            update_lbl(typed, dis_cur_word)
            # update letter bank
            hand.remove("?")
            update_lbl(letter_bank, str(hand))
            # change table row color
            table.updateColor(hand, " ".join(dis_cur_word).split())
            # TODO:
            #  1. update current damage indicator
        elif event.key() == Qt.Key_Backspace:
            # if current typed word is not null...
            if cur_word:
                # update letter bank (add back last typed letter into temporary hand)
                hand.append(cur_word[-1])
                update_lbl(letter_bank, str(hand))
                # update typed (remove last letter typed from
                cur_word = cur_word[0:-1]
                dis_cur_word = dis_cur_word[0:-1]
                update_lbl(typed, dis_cur_word)
                # change table row color
                table.updateColor(hand, " ".join(dis_cur_word).split())
        elif event.key() == Qt.Key_Return:
            # TODO:
            valid_word(cur_word)
            #  1. check word is valid (see method valid_word, above)
            #  2. deal damage + special effects
            #     Lots of work needed to be done here (implementing each letter's unique abilities)
            #  3. set hand to hand
            #  4. draw cards based on +draw cards (don't reshuffle deck)
            #  5. decrement/increment word count

            print("entered")

app = QApplication(sys.argv)
w = MainWindow()
w.setGeometry(0, 0, 1280, 720)

# LABELS
typed_label = QLabel(w)
typed_label.move(0, 0)
typed_label.setText("CURRENT WORD:")

# indicates current word that is being typed
typed = QLabel(w)
typed.move(125, 0)
typed.setText("type something")


letter_label = QLabel(w)
letter_label.move(0, 25)
letter_label.setText("LETTER BANK: ")

# a live letter bank of available letters
letter_bank = QLabel(w)
letter_bank.move(125, 25)
letter_bank.setText(str(hand))


current_damage_label = QLabel(w)
current_damage_label.move(0, 50)
current_damage_label.setText("BASE DAMAGE:")

# a live display of base damage (adding up "damage" attribute of each letter)
current_damage = QLabel(w)
current_damage.move(125, 50)
current_damage.setText("0")

# table, see LetterTable.py for table code
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
#  4. word_count display (denotes number of words that still can be made)
#  5. level up menu (3 panels, option 1: increase word length cap, option 2: increase starting hand size, option 3: increase health)
#  6. shop keeper?
w.show()

sys.exit(app.exec_())
