import sys
from PyQt6.QtWidgets import QApplication
from view import CalculatorView
from viewmodel import CalculatorViewModel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = CalculatorView()
    view_model = CalculatorViewModel()

    # Подключение сигналов
    view.calculate_signal.connect(lambda expr: view.set_result(view_model.calculate(expr)))
    view.calculate_signal.connect(lambda: view.update_history(view_model.get_history()))
    view.clear_signal.connect(lambda: view.clear_display())
    view.clear_signal.connect(lambda: view_model.clear())
    view.backspace_signal.connect(lambda: view.backspace())
    view.backspace_signal.connect(lambda: view.set_result(view_model.backspace()))
    for char in view.buttons:
        if char not in ['=', 'C', '⌫']:
            view.buttons[char].clicked.connect(
                lambda _, c=char: view.set_result(view_model.append_char(c.replace('√x', '√').replace('−', '-').replace('×', '*').replace('x^y', '^')))
            )

    view.show()
    sys.exit(app.exec())