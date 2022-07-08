class Letter:
    letter, description, damage, word, draw = "", "", 0, 0, 0

    def __init__(self, letter: str, damage: int, word: int, draw: int, description: str):
        self.letter = letter
        self.damage = damage
        self.word = word
        self.draw = draw
        self.description = description
