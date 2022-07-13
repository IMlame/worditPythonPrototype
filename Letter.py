import xlrd
import csv


class Letter:
    letter, description, damage, word, draw, statusTypes = "", "", 0, 0, 0, [""]

    def __init__(self, letter: str, damage: int, word: int, draw: int, status_types: list, description: str):
        self.letter = letter
        self.damage = damage
        self.word = word
        self.draw = draw
        self.status_types = status_types
        self.description = description


# for data handling
def import_letter_data():
    letters_file = open("letters.txt", "r")
    letters_lines = letters_file.read().split('\n')
    letter_info = {}
    for cStr in letters_lines:
        cur_letter=str(cStr.split(':')[0]).upper()
        newStr = [ '"{}"'.format(x) for x in list(csv.reader([cStr.split(':')[1]], delimiter=',', quotechar='"'))[0]]
        letter_info[cur_letter] = Letter(
            cur_letter,
            int(newStr[0].replace('"','')),
            int(newStr[1].replace('"','')),
            int(newStr[2].replace('"','')),
            newStr[3].replace('"','').split(','),
            newStr[4].replace('"',''))
    return letter_info

