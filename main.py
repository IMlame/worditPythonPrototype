import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel)
from PyQt5.Qt import Qt
import Letter
from LetterTable import LetterTable
import random

LABEL_MAKER_Y_OFFSET_DISTANCE = 25
LABEL_MAKER_TITLE_X_OFFSET = 140
label_num = 0

# will be drawn for
f = open("deck.txt", "r")
tempdeck = f.read()
f.close()
deck = tempdeck.split(",")
# currently in deck

hand = random.sample(deck, 5)
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


def label_maker(title: str, initial_value: str):
    global label_num
    label_title = QLabel(w)
    label_title.move(0, LABEL_MAKER_Y_OFFSET_DISTANCE * label_num)
    label_title.setText(title)

    label = QLabel(w)
    label.move(LABEL_MAKER_TITLE_X_OFFSET, LABEL_MAKER_Y_OFFSET_DISTANCE * label_num)
    label.setText(initial_value)

    label_num += 1

    return label

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)

    def keyPressEvent(self, event):
        global cur_word
        global dis_cur_word
        # handle word checking
        if 65 <= event.key() <= 126 and (chr(event.key()) in hand):
            # update typed
            cur_word = cur_word + chr(event.key())
            dis_cur_word = dis_cur_word + chr(event.key())
            update_lbl(qlabel=typed_label, text=dis_cur_word)
            hand.remove(chr(event.key()))
            update_lbl(qlabel=letter_bank_label, text=str(hand))
            # change table row color
            table.updateColor(cur_word=cur_word)
            # TODO:
            #  1. update current damage indicator
        elif 32 <= event.key() <= 126 and not (chr(event.key()) in hand) and ("?" in hand):
            # update typed
            cur_word = cur_word + "?"
            dis_cur_word = dis_cur_word + chr(event.key())
            update_lbl(typed_label, dis_cur_word)
            # update letter bank
            hand.remove("?")
            update_lbl(qlabel=letter_bank_label, text=str(hand))
            # change table row color
            table.updateColor(cur_word=cur_word)
            # TODO:
            #  1. update current damage indicator
        elif event.key() == Qt.Key_Backspace:
            # if current typed word is not null...
            if cur_word:
                # update letter bank (add back last typed letter into temporary hand)
                hand.append(cur_word[-1])
                update_lbl(qlabel=letter_bank_label, text=str(hand))
                # update typed (remove last letter typed from
                cur_word = cur_word[0:-1]
                dis_cur_word = dis_cur_word[0:-1]
                update_lbl(qlabel=typed_label, text=dis_cur_word)
                # change table row color
                table.updateColor(cur_word=cur_word)
        elif event.key() == Qt.Key_Return:
            # TODO:
            valid_word(dis_cur_word)
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

# indicates current word that is being typed
typed_label = label_maker("CURRENT WORD:", "type something")

# a live letter bank of available letters
letter_bank_label = label_maker("LETTER BANK:", str(hand))

# a live display of base damage (adding up "damage" attribute of each letter)
current_damage_label = label_maker("BASE DAMAGE:", "0")

# a live display of additional words
additional_words_label = label_maker("+WORD:", "1")

# a live display of additional draws
additional_draws_label = label_maker("+DRAW:", "1")

# displays amount of words left that can be made
available_words_label = label_maker("AVAILABLE WORDS:", "1")

# table, see LetterTable.py for table code
table = LetterTable(w)
table.move(480, 0)
table.setMinimumWidth(820)
table.setMinimumHeight(720)
table.updateTable(hand=hand, letter_info=letter_info)
table.updateColor(cur_word=cur_word)

# TODO:
#  1. Player healthbar
#  2. Boss healthbar
#  3. Damage display (current calculated damage with word that is currently typed)
#  4. word_count display (denotes number of words that still can be made)
#  5. level up menu (3 panels, option 1: increase word length cap, option 2: increase starting hand size, option 3: increase health)
#  6. shop keeper?
w.show()

sys.exit(app.exec_())
