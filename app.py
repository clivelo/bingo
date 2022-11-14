import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel, QSizePolicy, QStackedLayout, \
    QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QObject

from card import Card


class BingoSquare(QObject):
    state_changed = pyqtSignal(tuple)

    def __init__(self, row, col, val=0, state=0):
        super(BingoSquare, self).__init__(parent=None)
        self.row = row
        self.col = col
        self.val = val
        self.state = state
        self.win = False

    def display(self) -> (QLabel, QLabel):
        self.state_label = QLabel()
        if self.state == 1:
            self.state_label.setText("⬤")
        self.state_label.setStyleSheet("background-color:white; font-size:56pt; font-weight:700; color:red")
        self.state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.state_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        bingo_label = QLabel(str(self.val))
        bingo_label.setStyleSheet("background-color:rgba(255,255,255,0); font-size:36pt; font-weight:700; color:black")
        bingo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bingo_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        bingo_label.mousePressEvent = self.set_state

        return self.state_label, bingo_label

    def set_state(self, event):
        if self.state != 1 and not self.win:
            self.state = 1
            self.state_label.setText("⬤")
            self.state_changed.emit((self.row, self.col))


class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setGeometry(150, 150, 500, 500)
        self.setWindowTitle("Bingo")
        self.setStyleSheet("background-color:#293242")

        self.card = Card()

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.gridbox = QGridLayout()
        main_layout.addLayout(self.gridbox)

        self.init_card()
        self.display_card()

    def init_card(self):
        self.squares = []
        for i in range(5):
            row = []
            for j in range(5):
                square = BingoSquare(i, j, self.card.grid[i][j], self.card.state[i][j])
                square.state_changed.connect(self.update_card)
                row.append(square)
            self.squares.append(row)

    def display_card(self):
        for i in range(5):
            text_label = QLabel(Card.bingo[i])
            text_label.setStyleSheet("font-size:60pt; font-weight:700; color:#9da2ae")
            text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            self.gridbox.addWidget(text_label, 0, i)

        for i in range(5):
            for j in range(5):
                widgets = self.squares[i][j].display()
                self.gridbox.addWidget(widgets[0], i + 1, j)
                self.gridbox.addWidget(widgets[1], i + 1, j)

    @pyqtSlot(tuple)
    def update_card(self, tup):
        self.card.update_card(tup[0], tup[1])
        if self.card.check_win():
            for i in range(5):
                for j in range(5):
                    self.squares[i][j].win = True


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
