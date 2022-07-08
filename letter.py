import xlrd


class Letter:
    letter, description, damage, word, draw = "", "", 0, 0, 0

    def __init__(self, letter: str, damage: int, word: int, draw: int, description: str):
        self.letter = letter
        self.damage = damage
        self.word = word
        self.draw = draw
        self.description = description

# for data handling
def import_letter_data():
    letter_info = []
    wb = xlrd.open_workbook("LetterData.xls")
    sheet = wb.sheet_by_index(0)

    for i in range(1, sheet.nrows):
        letter_info.append(Letter(str(sheet.cell_value(i, 0).strip()).upper(),
                                 sheet.cell_value(i, 1),
                                 sheet.cell_value(i, 2),
                                 sheet.cell_value(i, 3),
                                 sheet.cell_value(i, 4)))
    return letter_info