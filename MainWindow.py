import random

from PyQt5.Qt import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QProgressBar, QLabel, QWidget

import Letter
from Enemy import Enemy
from Healthbar import Healthbar
from LetterTable import LetterTable

LABEL_MAKER_Y_OFFSET_DISTANCE = 25
LABEL_MAKER_TITLE_X_OFFSET = 140


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1280, 720)
        self.setFocusPolicy(Qt.StrongFocus)
        self.max_length_word = 99999
        # will be drawn for
        f = open("deck.txt", "r")
        tempdeck = f.read()
        f.close()
        self.deck = tempdeck.split(",")
        # currently in deck
        self.temp_discard = []
        self.discard = []
        random.shuffle(self.deck)
        self.hand = self.deck[:(min(5, len(self.deck)))]
        del self.deck[:(len(self.hand))]
        print(self.hand)
        print(self.deck)

        # hand = random.sample(deck, 5)
        # currently in hand (decreases in size as letters are typed, increases in size when backspace is pressed)
        # letter info from LetterData.xsl
        self.letter_info = Letter.import_letter_data()

        self.cur_word = ""
        self.dis_cur_word = ""

        # enemy object
        self.enemy = Enemy(window=self, enemy_img="assets/enemy.jpg", img_height=200,
                           healthbar=Healthbar(window=self, x=0, y=self.height()-50, width=480, height=50, initial_health=50, color=Qt.red))

        # LABELS
        self.label_num = 0
        # indicates current word that is being typed
        self.typed_label = self.label_maker("CURRENT WORD:", "type something")

        # a live letter bank of available letters
        self.letter_bank_label = self.label_maker("LETTER BANK:", str(self.hand))

        # a live display of base damage (adding up "damage" attribute of each letter)
        self.current_damage_label = self.label_maker("BASE DAMAGE:", "0")

        # a live display of total damage (adding up "damage" attribute of each letter)
        self.total_damage_label = self.label_maker("TOTAL DAMAGE:", "0")

        # a live display of additional words
        self.additional_words_label = self.label_maker("+WORDS:", "0")

        # a live display of additional draws
        self.additional_draws_label = self.label_maker("+DRAWS:", "0")

        # displays amount of words left that can be made
        self.available_words_label = self.label_maker("WORDS LEFT:", "1")

        self.turn = self.label_maker("Turn:", "1")

        # table, see LetterTable.py for table code
        self.table = LetterTable(self)
        self.table.move(480, 0)
        self.table.setMinimumWidth(820)
        self.table.setMinimumHeight(720)
        self.table.updateTable(hand=self.hand, letter_info=self.letter_info)
        self.table.updateColor(cur_word=self.cur_word)

    def keyPressEvent(self, event):
        # handle word checking
        if 65 <= event.key() <= 126 and len(self.cur_word) <= self.max_length_word:
            if chr(event.key()) in self.hand:
                self.cur_word = self.cur_word + chr(event.key())
                self.dis_cur_word = self.dis_cur_word + chr(event.key())
                self.hand.remove(chr(event.key()))
            elif not (chr(event.key()) in self.hand) and ("?" in self.hand):
                self.cur_word = self.cur_word + "?"
                self.dis_cur_word = self.dis_cur_word + chr(event.key())
                self.hand.remove("?")

        elif event.key() == Qt.Key_Backspace:
            # if current typed word is not null...
            if self.cur_word:
                # update letter bank (add back last typed letter into temporary hand)
                self.hand.append(self.cur_word[-1])
                # update typed (remove last letter typed from
                self.cur_word = self.cur_word[0:-1]
                self.dis_cur_word = self.dis_cur_word[0:-1]
        elif event.key() == Qt.Key_Return:
            # if valid word and you can still make a word
            if self.valid_word(self.dis_cur_word) and not self.available_words_label.text() == "0":
                dmg, draw, word, base_dmg = self.dmg_calculation(self.cur_word)
                word = max(word, 0)
                self.discard_word()
                print(dmg)
                self.update_lbl(qlabel=self.available_words_label, text=str(int(self.available_words_label.text()) - 1 + word))
                self.hand.extend([self.deck.pop(random.randrange(len(self.deck))) for _ in range(min(draw, len(self.deck)))])
                self.update_lbl(qlabel=self.letter_bank_label, text=str(self.hand))

                # apply damage to enemy
                self.enemy.damage(dmg)
                self.update()

                self.table.updateTable(self.hand, letter_info=self.letter_info)
            # if no more words can be made
            elif self.available_words_label.text() == "0" or self.dis_cur_word == "":
                self.update_lbl(qlabel=self.available_words_label, text="1")
                self.discard_word()
                self.discard_hand()
                self.discard.extend(self.temp_discard)
                self.temp_discard = []
                random.shuffle(self.discard)
                self.deck.extend(self.discard)
                self.discard = []
                self.hand = self.deck[:(min(5, len(self.deck)))]
                del self.deck[:len(self.hand)]
                self.update_lbl(qlabel=self.letter_bank_label, text=str(self.hand))

                self.enemy.damage(-5)
                self.update()

                self.update_lbl(qlabel=self.turn, text=str(int(self.turn.text()) + 1))

                self.table.updateTable(self.hand, letter_info=self.letter_info)

        # update hand and letter bank labels
        self.update_lbl(qlabel=self.typed_label, text=self.dis_cur_word)
        self.update_lbl(qlabel=self.letter_bank_label, text=str(self.hand))

        dmg, draw, word, base_dmg = self.dmg_calculation(self.cur_word)
        self.update_lbl(self.current_damage_label, str(base_dmg))
        self.update_lbl(self.total_damage_label, str(dmg))
        self.update_lbl(self.additional_words_label, str(word))
        self.update_lbl(self.additional_draws_label, str(draw))
        # change table row color
        self.table.updateColor(cur_word=self.cur_word)

    def paintEvent(self, e):
        self.enemy.update()

    # HELPER METHODS
    def valid_word(self, word: str):
        dicFile = open("dictionary.txt", "r")
        lines = dicFile.read().split('\n')
        dicFile.close()
        if word.upper() in lines:
            return True
        return False

    def dmg_calculation(self, word: str):
        base_dmg = 0
        total_dmg = 0
        total_draw = 0
        total_word = 0
        for count, i in enumerate(word):
            my_dmg = self.letter_info[i].damage
            my_draw = self.letter_info[i].draw
            my_word = self.letter_info[i].word
            modifiers = 1
            # keep track of base damage
            base_dmg += self.letter_info[i].damage

            if self.letter_info[i].letter == 'R':
                my_dmg += 1 * self.dis_cur_word.count('R', 0, len(word))
            elif self.letter_info[i].letter == 'O':
                my_dmg += 2 * (list(set(self.dis_cur_word) & set("AEIU")) == [])
            elif self.letter_info[i].letter == 'L':
                my_dmg += 2 * (count != 0 and self.letter_info[self.dis_cur_word[count - 1]].letter == 'L')
                my_dmg += 2 * (count != len(word) - 1 and self.letter_info[self.dis_cur_word[count + 1]].letter == 'L')
            elif self.letter_info[i].letter == 'S':
                if count == len(word) - 1:
                    modifiers -= 0.5
            elif self.letter_info[i].letter == 'D':
                if count != 0:
                    my_word += 1
            elif self.letter_info[i].letter == 'Y':
                if count != len(word) - 1:
                    modifiers += 1
            for i in [item for item in self.letter_info[i].status_types if item.startswith('DMG')]:
                modifiers += int(i[3:]) / 100
            for i in [item for item in self.letter_info[i].status_types if item.startswith('END')]:
                my_word -= 100000
            total_dmg += my_dmg * modifiers
            total_draw += my_draw
            total_word += my_word

        return [total_dmg, total_draw, total_word, base_dmg]

    def update_lbl(self, qlabel: QLabel, text: str):
        qlabel.setText(text)
        qlabel.adjustSize()

    def discard_hand(self):
        self.temp_discard.extend(self.hand)
        self.hand = []
        self.update_lbl(qlabel=self.letter_bank_label, text="")

    def discard_word(self):
        list1 = []
        list1[:0] = self.cur_word
        self.temp_discard.extend(list1)
        self.cur_word = ""
        self.dis_cur_word = ""
        self.update_lbl(qlabel=self.typed_label, text=self.dis_cur_word)

    def label_maker(self, title: str, initial_value: str):
        label_title = QLabel(self)
        label_title.move(0, LABEL_MAKER_Y_OFFSET_DISTANCE * self.label_num)
        label_title.setText(title)

        label = QLabel(self)
        label.move(LABEL_MAKER_TITLE_X_OFFSET, LABEL_MAKER_Y_OFFSET_DISTANCE * self.label_num)
        label.setText(initial_value)

        self.label_num += 1

        return label
# TODO:
#  1. Player healthbar
#  2. Boss healthbar
#  3. Damage display (current calculated damage with word that is currently typed)
#  4. word_count display (denotes number of words that still can be made)
#  5. level up menu (3 panels, option 1: increase word length cap, option 2: increase starting hand size, option 3: increase health)
#  6. shop keeper?