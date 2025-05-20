import sys
from PyQt6.QtWidgets import QApplication
from view import CalculatorView
from viewmodel import CalculatorViewModel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = CalculatorView()
    view_model = CalculatorViewModel()

    # Connexion des signaux
    view.calculate_signal.connect(view_model.calculate)
    view.calculate_signal.connect(lambda expr: view.set_result(view_model.calculate(expr)))
    view.calculate_signal.connect(lambda _: view.update_history(view_model.history))
    view.backspace_signal.connect(lambda: view.backspace())
    view.backspace_signal.connect(lambda: view.set_result(view_model.backspace(view.display.text())))
    view.clear_signal.connect(lambda: view.clear_display())
    view.clear_signal.connect(lambda: view_model.clear())
    view.undo_signal.connect(lambda: view.set_result(view_model.undo()))
    view.undo_signal.connect(lambda: view.update_history(view_model.history))

    view.show()
    sys.exit(app.exec())