import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QProgressBar)
from PyQt5.Qt import Qt
import Letter
from LetterTable import LetterTable
import random


def valid_word(word: str):
    dicFile = open("dictionary.txt", "r")
    lines = dicFile.read().split('\n')
    dicFile.close()
    if word.upper() in lines:
        return True
    return False


def dmg_calculation(word: str):
    global dis_cur_word
    base_dmg = 0
    total_dmg = 0
    total_draw = 0
    total_word = 0
    for count, i in enumerate(word):
        my_dmg = letter_info[i].damage
        my_draw = letter_info[i].draw
        my_word = letter_info[i].word
        modifiers = 1
        # keep track of base damage
        base_dmg += letter_info[i].damage

        if letter_info[i].letter == 'R':
            print("cool")
            my_dmg += 1 * dis_cur_word.count('R', 0, len(word))
        elif letter_info[i].letter == 'O':
            my_dmg += 2 * (list(set(dis_cur_word) & set("AEIU")) == [])
        elif letter_info[i].letter == 'L':
            my_dmg += 2 * (count != 0 and letter_info[dis_cur_word[count - 1]].letter == 'L')
            my_dmg += 2 * (count != len(word) - 1 and letter_info[dis_cur_word[count + 1]].letter == 'L')
        elif letter_info[i].letter == 'S':
            if count == len(word) - 1:
                modifiers -= 0.5
        elif letter_info[i].letter == 'D':
            if count != 0:
                my_word += 1
        elif letter_info[i].letter == 'Y':
            if count != len(word) - 1:
                modifiers += 1
        for i in [item for item in letter_info[i].status_types if item.startswith('DMG')]:
            modifiers += int(i[3:]) / 100
        for i in [item for item in letter_info[i].status_types if item.startswith('END')]:
            my_word -= 100000
        total_dmg += my_dmg * modifiers
        total_draw += my_draw
        total_word += my_word

    return [total_dmg, total_draw, total_word, base_dmg]


def update_lbl(qlabel: QLabel, text: str):
    qlabel.setText(text)
    qlabel.adjustSize()


def discard_hand():
    global hand
    global temp_discard
    temp_discard.extend(hand)
    hand = []
    update_lbl(qlabel=letter_bank_label, text="")


def discard_word():
    global cur_word
    global temp_discard
    global dis_cur_word
    list1 = []
    list1[:0] = cur_word
    temp_discard.extend(list1)
    cur_word = ""
    dis_cur_word = ""
    update_lbl(qlabel=typed_label, text=dis_cur_word)


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


def label_maker2(title: str, initial_value: str):
    global label_num
    label_num += 2
    label_title = QLabel(w)
    label_title.move(0, LABEL_MAKER_Y_OFFSET_DISTANCE * label_num)
    label_title.setText(title)
    label_num += 1

    bar_title = QProgressBar(w)
    bar_title.move(0, LABEL_MAKER_Y_OFFSET_DISTANCE * label_num)
    bar_title.setRange(0, initial_value)
    bar_title.setValue(initial_value)

    label_num += 1

    return bar_title


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)

    def keyPressEvent(self, event):
        global cur_word
        global dis_cur_word
        global hand
        global deck
        global discard
        global temp_discard
        # handle word checking
        if 65 <= event.key() <= 126:
            if chr(event.key()) in hand:
                cur_word = cur_word + chr(event.key())
                dis_cur_word = dis_cur_word + chr(event.key())
                hand.remove(chr(event.key()))
            elif not (chr(event.key()) in hand) and ("?" in hand):
                cur_word = cur_word + "?"
                dis_cur_word = dis_cur_word + chr(event.key())
                hand.remove("?")

        elif event.key() == Qt.Key_Backspace:
            # if current typed word is not null...
            if cur_word:
                # update letter bank (add back last typed letter into temporary hand)
                hand.append(cur_word[-1])
                # update typed (remove last letter typed from
                cur_word = cur_word[0:-1]
                dis_cur_word = dis_cur_word[0:-1]
        elif event.key() == Qt.Key_Return:
            # if enemy is
            if valid_word(dis_cur_word) and not available_words_label.text() == "0":
                dmg, draw, word, base_dmg = dmg_calculation(cur_word)
                word = max(word, 0)
                discard_word()
                print(dmg)
                update_lbl(qlabel=available_words_label, text=str(int(available_words_label.text()) - 1 + word))
                hand.extend([deck.pop(random.randrange(len(deck))) for _ in range(min(draw, len(deck)))])
                update_lbl(qlabel=letter_bank_label, text=str(hand))

                enemy_health.setValue(enemy_health.value() - dmg)

                table.updateTable(hand, letter_info=letter_info)
            elif available_words_label.text() == "0" or dis_cur_word == "":
                update_lbl(qlabel=available_words_label, text="1")
                discard_word()
                discard_hand()
                discard.extend(temp_discard)
                temp_discard = []
                random.shuffle(discard)
                deck.extend(discard)
                discard = []
                hand = deck[:(min(5, len(deck)))]
                del deck[:len(hand)]
                update_lbl(qlabel=letter_bank_label, text=str(hand))
                enemy_health.setValue(enemy_health.value() + 5)
                update_lbl(qlabel=turn, text=str(int(turn.text()) + 1))

                table.updateTable(hand, letter_info=letter_info)

        # update hand and letter bank labels
        update_lbl(qlabel=typed_label, text=dis_cur_word)
        update_lbl(qlabel=letter_bank_label, text=str(hand))

        dmg, draw, word, base_dmg = dmg_calculation(cur_word)
        current_damage_label.setText(str(base_dmg))
        total_damage_label.setText(str(dmg))
        additional_words_label.setText(str(word))
        additional_draws_label.setText(str(draw))
        # change table row color
        table.updateColor(cur_word=cur_word)


LABEL_MAKER_Y_OFFSET_DISTANCE = 25
LABEL_MAKER_TITLE_X_OFFSET = 140
label_num = 0

# will be drawn for
f = open("deck.txt", "r")
tempdeck = f.read()
f.close()
deck = tempdeck.split(",")
# currently in deck
temp_discard = []
discard = []
random.shuffle(deck)
hand = deck[:(min(5, len(deck)))]
del deck[:(len(hand))]
print(hand)
print(deck)

# hand = random.sample(deck, 5)
# currently in hand (decreases in size as letters are typed, increases in size when backspace is pressed)
# letter info from LetterData.xsl
letter_info = Letter.import_letter_data()

cur_word = ""
dis_cur_word = ""

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

# a live display of total damage (adding up "damage" attribute of each letter)
total_damage_label = label_maker("TOTAL DAMAGE:", "0")

# a live display of additional words
additional_words_label = label_maker("+WORDS:", "0")

# a live display of additional draws
additional_draws_label = label_maker("+DRAWS:", "0")

# displays amount of words left that can be made
available_words_label = label_maker("WORDS LEFT:", "1")

turn = label_maker("Turn:", "1")

enemy_health = label_maker2("Enemy Health", 40)

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
