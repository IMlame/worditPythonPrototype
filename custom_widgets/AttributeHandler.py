from PyQt5.QtWidgets import QLabel, QWidget


class AttributeHandler:
    def __init__(self, window: QWidget, x: int, y: int):
        self._attributes = []
        self._attribute_label = QLabel(window)
        self._attribute_label.move(x, y)
        self._attribute_label.setText(str(self._attributes))
        self._attribute_label.adjustSize()

    def add_effect(self, effect: str):
        exists = False
        for i in range(len(self._attributes)):
            if effect[:-1] in self._attributes[i]:
                self._attributes[i] = self._attributes[i][:-1] + str(max(self._attributes[i][-1], effect[-1]))
                exists = True
                break
        if not exists:
            self._attributes.append(effect)

        self._attribute_label.setText(str(self._attributes))
        self._attribute_label.adjustSize()

    def get_attributes(self):
        return self._attributes

    def clear_attributes(self):
        self._attributes.clear()
        self._attribute_label.setText(str(self._attributes))
        self._attribute_label.adjustSize()
