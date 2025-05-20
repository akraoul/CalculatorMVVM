from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class CalculatorView(QMainWindow):
    calculate_signal = pyqtSignal(str)
    backspace_signal = pyqtSignal()
    clear_signal = pyqtSignal()
    undo_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Calculator MVVM with Command")
        self.setFixedSize(450, 700)

        # Styles (identiques au code fourni)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #dcdcdc;
                border-radius: 8px;
                padding: 10px;
                font-size: 24px;
                color: #2d3436;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #dcdcdc;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #2d3436;
            }
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #dcdcdc;
                border-radius: 8px;
                font-size: 18px;
                color: #2d3436;
                padding: 10px;
                margin: 4px;
            }
            QPushButton:hover {
                background-color: #e8ecef;
            }
            QPushButton:pressed {
                background-color: #dfe4ea;
            }
            QPushButton#operator {
                background-color: #74b9ff;
                color: white;
                border: none;
            }
            QPushButton#operator:hover {
                background-color: #339af0;
            }
            QPushButton#function {
                background-color: #dfe4ea;
                color: #2d3436;
                border: none;
            }
            QPushButton#function:hover {
                background-color: #ced4da;
            }
            QPushButton#equals {
                background-color: #ff7675;
                color: white;
                border: none;
            }
            QPushButton#equals:hover {
                background-color: #ff5e57;
            }
        """)

        # Main widget et layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # Champ d'affichage
        self.display = QLineEdit()
        self.display.setFixedHeight(80)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFont(QFont("Arial", 24))
        self.layout.addWidget(self.display)

        # Champ d'historique
        self.history_display = QTextEdit()
        self.history_display.setFixedHeight(150)
        self.history_display.setReadOnly(True)
        self.history_display.setFont(QFont("Arial", 14))
        self.history_display.setHtml("<b>История:</b><br>")
        self.layout.addWidget(self.history_display)

        # Grille de boutons
        self.button_grid = QGridLayout()
        self.button_grid.setSpacing(8)
        self.layout.addLayout(self.button_grid)

        # Layout des boutons (ajout du bouton Undo)
        button_layout = [
            ('C', 0, 0, 'function'), ('⌫', 0, 1, 'function'), ('(', 0, 2), (')', 0, 3), ('÷', 0, 4, 'operator'),
            ('sin', 1, 0, 'function'), ('cos', 1, 1, 'function'), ('7', 1, 2), ('8', 1, 3), ('9', 1, 4),
            ('tan', 2, 0, 'function'), ('ln', 2, 1, 'function'), ('4', 2, 2), ('5', 2, 3), ('6', 2, 4),
            ('√', 3, 0, 'function'), ('π', 3, 1, 'function'), ('1', 3, 2), ('2', 3, 3), ('3', 3, 4),
            ('e', 4, 0, 'function'), ('^', 4, 1, 'operator'), ('0', 4, 2), ('.', 4, 3), ('=', 4, 4, 'equals'),
            ('log', 5, 0, 'function'), ('%', 5, 1, 'operator'), ('×', 5, 2, 'operator'), ('−', 5, 3, 'operator'), ('+', 5, 4, 'operator'),
            ('Undo', 6, 0, 'function', 5)  # Bouton Undo ajouté
        ]

        # Création des boutons
        self.buttons = {}
        for text, row, col, *style in button_layout:
            button = QPushButton(text)
            button.setFixedSize(80, 60)
            button.setFont(QFont("Arial", 18))
            if style and style[0]:
                button.setObjectName(style[0])
            if text == '√':
                button.setText("√x")
            elif text == '−':
                button.setText("−")
            elif text == '×':
                button.setText("×")
            elif text == '^':
                button.setText("x^y")
            if text == 'Undo' and len(style) > 1:
                button.setFixedWidth(80 * style[1])  # Largeur ajustée pour Undo
            self.button_grid.addWidget(button, row, col)
            self.buttons[text] = button
            button.clicked.connect(lambda _, t=text: self.on_button_click(t))

    def on_button_click(self, char):
        char = char.replace('√x', '√').replace('−', '-').replace('×', '*').replace('x^y', '^')
        if char == '=':
            self.calculate_signal.emit(self.display.text())
        elif char == 'C':
            self.clear_signal.emit()
        elif char == '⌫':
            self.backspace_signal.emit()
        elif char == 'Undo':
            self.undo_signal.emit()
        else:
            current_text = self.display.text()
            self.display.setText(current_text + char.replace('*', '×').replace('-', '−').replace('^', 'x^y'))

    def set_result(self, result: str):
        self.display.setText(result)

    def update_history(self, history: list):
        self.history_display.setHtml("<b>История:</b><br>" + "<br>".join(history[-5:]))

    def clear_display(self):
        self.display.setText("")
        self.history_display.setHtml("<b>История:</b><br>")

    def backspace(self):
        current_text = self.display.text()
        if current_text:
            self.display.setText(current_text[:-1])