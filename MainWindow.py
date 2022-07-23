import random

from PyQt5.Qt import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QGraphicsBlurEffect

import Letter
from Enemy import Enemy
from custom_widgets.Healthbar import Healthbar
from custom_widgets.LetterTable import LetterTable
from functools import partial

from Player import Player

HINTS = True

LABEL_MAKER_Y_OFFSET_DISTANCE = 25
LABEL_MAKER_TITLE_X_OFFSET = 140

STATUS_EFFECTS = ["BURN", "FREZ", "GOLD", "HEAL", "PARA", "WEAK"]

UPGRADE_BUTTON_X_SPACING = 200

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.deck, self.temp_discard, self.discard, self.hand, self.letter_info, \
        self.cur_word, self.dis_cur_word, self.player, self.enemy, self.table, \
        self.label_num, self.typed_label, self.letter_bank_label, self.current_damage_label, \
        self.total_damage_label, self.additional_words_label, self.additional_draws_label, \
        self.available_words_label, self.can_words, self.turn, self.endTurn, \
        self.increase_hand, self.hand_label, self.increase_health, self.health_label, \
        self.increase_word_len, self.len_label, self.increase_base_dmg, \
        self.base_dmg_label = (None,) * 29

        # player base stats
        self.max_length_word = 4
        self.base_health = 50
        self.base_damage = 0
        self.starting_hand_count = 5
        self.enemy_num = 1

        self.setGeometry(0, 0, 1280, 720)
        self.setFocusPolicy(Qt.StrongFocus)

        self.setup_round()

    def keyPressEvent(self, event):
        if not self.player.is_dead() and not self.enemy.is_dead():
            # handle word checking
            if 65 <= event.key() <= 126 and len(self.cur_word) < self.max_length_word:
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
                    dmg, draw, word, base_dmg, attributes = self.dmg_calculation(self.cur_word)
                    word = max(word, 0)
                    self.discard_word()
                    self.update_lbl(qlabel=self.available_words_label,
                                    text=str(int(self.available_words_label.text()) - 1 + word))
                    self.hand.extend(
                        [self.deck.pop(random.randrange(len(self.deck))) for _ in range(min(draw, len(self.deck)))])
                    self.update_lbl(qlabel=self.letter_bank_label, text=str(self.hand))

                    # apply damage to enemy
                    self.enemy.damage(self.player.attack(dmg))

                    # apply status effects to enemy/player
                    for attribute in attributes:
                        if "HEAL" in attribute:
                            self.player.damage(-3 * int(attribute[-1]))
                        elif "GOLD" in attribute:
                            print("you got gold. yay!")
                        else:
                            self.enemy.apply_status_effect(attribute)

                    if self.enemy.is_dead():
                        self.show_buttons()

                    self.update()

                    self.table.updateTable(self.hand, letter_info=self.letter_info)

            if len(self.cur_word) == self.max_length_word:
                self.typed_label.setStyleSheet("color: red")
            else:
                self.typed_label.setStyleSheet("")

            if HINTS:
                self.update_lbl(qlabel=self.can_words, text=str(self.valid_word_inverse()[:3]))

            # update hand and letter bank labels
            self.update_lbl(qlabel=self.typed_label, text=self.dis_cur_word)
            self.update_lbl(qlabel=self.letter_bank_label, text=str(self.hand))

            # update stats on current word
            dmg, draw, word, base_dmg, attributes = self.dmg_calculation(self.cur_word)
            self.update_lbl(self.current_damage_label, str(base_dmg))
            self.update_lbl(self.total_damage_label, str(dmg))
            self.update_lbl(self.additional_words_label, str(word))
            self.update_lbl(self.additional_draws_label, str(draw))

            # change table row color
            self.table.updateColor(cur_word=self.cur_word)

    def btnListener(self, button_name):
        if button_name == "End Turn" and not self.player.is_dead() and not self.enemy.is_dead():
            self.update_lbl(qlabel=self.available_words_label, text="1")
            self.discard_word()
            self.discard_hand()
            self.discard.extend(self.temp_discard)
            self.temp_discard = []
            random.shuffle(self.discard)
            self.deck.extend(self.discard)
            self.discard = []
            self.hand = []
            for i in self.multi_turn_effects:
                if i == 'Q':
                    self.hand.extend('Q')
                    self.deck.remove("Q")
                    self.hand.extend(self.deck[:(min(1, len(self.deck)))])
                    del self.deck[:(min(1, len(self.deck)))]
                    self.multi_turn_effects.remove('Q')
            self.hand.extend(self.deck[:(min(self.starting_hand_count, len(self.deck)))])
            del self.deck[:len(self.hand)]
            self.update_lbl(qlabel=self.letter_bank_label, text=str(self.hand))

            self.player.damage(self.enemy.attack())
            # test if burn damage kills enemy
            if self.enemy.is_dead():
                self.show_buttons()

            self.update()

            self.update_lbl(qlabel=self.turn, text=str(int(self.turn.text()) + 1))

            self.table.updateTable(self.hand, letter_info=self.letter_info)

            if HINTS:
                self.update_lbl(qlabel=self.can_words, text=str(self.valid_word_inverse()[:3]))
        elif button_name == "hand_button":
            self.starting_hand_count += 1
            self.deck.append("1")
            self.reset_round()
        elif button_name == "health_button":
            self.base_health += 10 * self.enemy_num
            self.deck.append("2")
            self.reset_round()
        elif button_name == "len_button":
            self.max_length_word += 1
            self.deck.append("3")
            self.reset_round()
        elif button_name == "base_dmg_button":
            self.base_damage += 2 * self.enemy_num
            self.deck.append("4")
            self.reset_round()

    def paintEvent(self, e):
        self.enemy.update()
        self.player.update()

    # HELPER METHODS
    def valid_word(self, word: str):
        dicFile = open("dictionary.txt", "r")
        lines = dicFile.read().split('\n')
        dicFile.close()
        if word.upper() in lines:
            return True
        return False

    def valid_word_inverse(self):
        if HINTS:
            dicFile = open("dictionary.txt", "r")
            lines = dicFile.read().split('\n')
            dicFile.close()
            valid_words = []
            for word in [item for item in lines if item.startswith(self.dis_cur_word)]:
                available_letters = self.hand[:]
                if len(word)>min(len(available_letters),self.max_length_word):
                    continue
                blank_count = available_letters.count('?')

                missed_counter = 0
                for letter in word[len(self.dis_cur_word):]:
                    if letter in available_letters:
                        available_letters.remove(letter)
                    else:
                        missed_counter += 1

                # print word, missed_counter
                if missed_counter <= blank_count:
                    valid_words.append(word)
            return sorted(valid_words, key=len, reverse=True)

    # played should only be true when
    def dmg_calculation(self, word: str):
        base_dmg = self.base_damage
        total_dmg = 0
        total_draw = 0
        total_word = 0
        attributes = []
        modifiers = 1
        for count, i in enumerate(word):
            my_dmg = self.letter_info[i].damage
            my_draw = self.letter_info[i].draw
            my_word = self.letter_info[i].word
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
            elif self.letter_info[i].letter == 'Q':
                self.multi_turn_effects.append("Q")

            for k in [item for item in self.letter_info[i].status_types if item.startswith('DMG')]:
                modifiers += int(k[3:]) / 100
            if 'END' in self.letter_info[i].status_types:
                my_word -= 100000

            for status_effect in self.letter_info[i].status_types:
                if status_effect and status_effect[:-1] in STATUS_EFFECTS:
                    attributes.append(status_effect)

            total_dmg += my_dmg
            total_draw += my_draw
            total_word += my_word

        return [total_dmg * modifiers, total_draw, total_word, base_dmg, attributes]

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

    def button_maker(self, title: str, button_name: str, x: int, y: int, img="", img_height=0, start_value=0):
        button = QPushButton(self)
        button.setText(title)
        button.clicked.connect(partial(self.btnListener, button_name))
        button.move(x, y)

        if img:
            button.adjustSize()
            button.move(int(x + ((UPGRADE_BUTTON_X_SPACING / 2) - (button.width() / 2))), int(y))
            button.hide()

            # image
            pixmap = QPixmap(img)
            image = QLabel(self)
            image.setPixmap(pixmap.scaledToWidth(img_height))
            image.adjustSize()
            image.move(int(x + ((UPGRADE_BUTTON_X_SPACING / 2) - (image.width() / 2))), int(y - 150))

            # stat number label
            qlabel = QLabel(self)
            qlabel.move(image.x() + 4, image.y() + 2)
            qlabel.setText(str(start_value))
            qlabel.setStyleSheet("font-size: 20px")
            qlabel.adjustSize()

            return button, qlabel

        return button

    def show_buttons(self):
        self.increase_hand.show()
        self.increase_health.show()
        self.increase_word_len.show()
        self.increase_base_dmg.show()

    def setup_round(self):
        # will be drawn for
        f = open("deck.txt", "r")
        tempdeck = f.read()
        f.close()
        self.deck = tempdeck.split(",")
        # currently in deck
        self.temp_discard = []
        self.discard = []
        random.shuffle(self.deck)
        self.hand = self.deck[:(min(self.starting_hand_count, len(self.deck)))]
        del self.deck[:(len(self.hand))]

        self.letter_info = Letter.import_letter_data()

        self.cur_word = ""
        self.dis_cur_word = ""

        # player object
        self.player = Player(window=self, enemy_img="assets/player.jpg", img_height=150,
                             healthbar=Healthbar(window=self, x=0, y=self.height() - 300, width=480, height=50,
                                                 initial_health=self.base_health, color=Qt.blue))
        # enemy object
        self.enemy = Enemy(window=self, enemy_img="assets/enemy.png", img_height=150,
                           healthbar=Healthbar(window=self, x=0, y=self.height() - 50, width=480, height=50,
                                               initial_health=1 * self.enemy_num, color=Qt.red), base_dmg = 5 * self.enemy_num)

        # table, see LetterTable.py for table code
        self.table = LetterTable(self)
        self.table.move(480, 0)
        self.table.setMinimumWidth(820)
        self.table.setMinimumHeight(472)
        self.table.updateTable(hand=self.hand, letter_info=self.letter_info)
        self.table.updateColor(cur_word=self.cur_word)

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

        self.can_words = self.label_maker("WORDS YOU CAN DO:", "")

        self.turn = self.label_maker("Turn:", "1")

        self.endTurn = self.button_maker(title="End Turn", button_name="End Turn", x=0, y=LABEL_MAKER_Y_OFFSET_DISTANCE * self.label_num)

        self.increase_hand, self.hand_label = self.button_maker(title="Starting hand +1", button_name="hand_button", x=self.table.x(),
                                                                y=self.height() - 50,
                                                                img="assets/hand.png", img_height=125,
                                                                start_value=self.starting_hand_count)

        self.increase_health, self.health_label = self.button_maker(title="Base health +" + str(10 * self.enemy_num),
                                                                    button_name="health_button", x=self.table.x() + UPGRADE_BUTTON_X_SPACING * 1,
                                                                    y=self.height() - 50,
                                                                    img="assets/health.png", img_height=125,
                                                                    start_value=self.base_health)

        self.increase_word_len, self.len_label = self.button_maker(title="Word len +1",
                                                                   button_name="len_button", x=self.table.x() + UPGRADE_BUTTON_X_SPACING * 2,
                                                                   y=self.height() - 50,
                                                                   img="assets/length.png", img_height=125,
                                                                   start_value=self.max_length_word)

        self.increase_base_dmg, self.base_dmg_label = self.button_maker(title="Base damage +" + str(2 * self.enemy_num),
                                                                        button_name="base_dmg_button", x=self.table.x() + UPGRADE_BUTTON_X_SPACING * 3,
                                                                        y=self.height() - 50,
                                                                        img="assets/damage.png", img_height=125,
                                                                        start_value=self.base_damage)

        self.multi_turn_effects = []

        if HINTS:
            self.update_lbl(qlabel=self.can_words, text=str(self.valid_word_inverse()[:3]))

    def reset_round(self):
        self.enemy_num += 1
        self.update_lbl(qlabel=self.available_words_label, text="1")
        self.discard_word()
        self.discard_hand()
        self.discard.extend(self.temp_discard)
        self.temp_discard = []
        random.shuffle(self.discard)
        self.deck.extend(self.discard)
        self.discard = []
        self.hand = []
        for i in self.multi_turn_effects:
            if i == 'Q':
                self.hand.extend('Q')
                self.deck.remove("Q")
                self.hand.extend(self.deck[:(min(1, len(self.deck)))])
                del self.deck[:(min(1, len(self.deck)))]
                self.multi_turn_effects.remove('Q')
        self.hand.extend(self.deck[:(min(self.starting_hand_count, len(self.deck)))])
        del self.deck[:len(self.hand)]
        self.update_lbl(qlabel=self.letter_bank_label, text=str(self.hand))

        self.player.damage(self.enemy.attack())
        # test if burn damage kills enemy
        if self.enemy.is_dead():
            self.show_buttons()

        self.update()

        self.update_lbl(qlabel=self.turn, text=str(int(self.turn.text()) + 1))

        self.table.updateTable(self.hand, letter_info=self.letter_info)

        if HINTS:
            self.update_lbl(qlabel=self.can_words, text=str(self.valid_word_inverse()[:3]))

        self.cur_word = ""
        self.dis_cur_word = ""

        self.table.updateTable(hand=self.hand, letter_info=self.letter_info)
        self.table.updateColor(cur_word=self.cur_word)

        self.player.reset(self.base_health)
        self.enemy.reset(new_max_health=25 * self.enemy_num, new_base_damage=5 * self.enemy_num)

        # update things that change when the round resets
        self.update_lbl(self.current_damage_label, str(self.base_damage))
        self.update_lbl(self.letter_bank_label, str(self.hand))
        self.update_lbl(self.available_words_label, str(1))

        # update display numbers
        self.update_lbl(self.hand_label, str(self.starting_hand_count))
        self.update_lbl(self.health_label, str(self.base_health))
        self.update_lbl(self.len_label, str(self.max_length_word))
        self.update_lbl(self.base_dmg_label, str(self.base_damage))

        # update buttons
        self.increase_hand.setText("Starting hand +" + str(1))
        self.increase_hand.adjustSize()
        self.increase_word_len.setText("Word len +" + str(1))
        self.increase_word_len.adjustSize()
        self.increase_health.setText("Base health +" + str(10 * self.enemy_num))
        self.increase_health.adjustSize()
        self.increase_base_dmg.setText("Base damage +" + str(2 * self.enemy_num))
        self.increase_base_dmg.adjustSize()

        if HINTS:
            self.update_lbl(qlabel=self.can_words, text=str(self.valid_word_inverse()[:3]))

        self.increase_hand.hide()
        self.increase_health.hide()
        self.increase_word_len.hide()
        self.increase_base_dmg.hide()

        self.update()

# TODO:
#  1. Player healthbar
#  2. Boss healthbar
#  3. Damage display (current calculated damage with word that is currently typed)
#  4. word_count display (denotes number of words that still can be made)
#  5. level up menu (3 panels, option 1: increase word length cap, option 2: increase starting hand size, option 3: increase health)
#  6. shop keeper?
