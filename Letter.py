import xlrd
import csv


class Letter:
    letter, description, damage, word, draw, statusTypes = "", "", 0, 0, 0, [""]

    def __init__(self, letter: str, damage: int, word: int, draw: int, statusTypes: list[str], description: str):
        self.letter = letter
        self.damage = damage
        self.word = word
        self.draw = draw
        self.statusType = statusTypes
        self.description = description


# for data handling
def import_letter_data():
    """letter_info = {}
    wb = xlrd.open_workbook("LetterData.xls")
    sheet = wb.sheet_by_index(0)

    for i in range(1, sheet.nrows):
        cur_letter = str(sheet.cell_value(i, 0).strip()).upper()
        letter_info[cur_letter] = Letter(
            cur_letter,
            sheet.cell_value(i, 1),
            sheet.cell_value(i, 2),
            sheet.cell_value(i, 3),
            sheet.cell_value(i, 4))
    return letter_info"""
    lettersFile = open("letters.txt", "r")
    letters_lines = lettersFile.read().split('\n')
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

