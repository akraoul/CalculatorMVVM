from model import CalculatorModel

class CalculatorViewModel:
    def __init__(self):
        self.model = CalculatorModel()
        self.current_expression = ""
        self.history = []
        self.result_shown = False

    def calculate(self, expression: str):
        if not expression:
            return ""
        try:
            result = self.model.calculate(expression)
            self.history.append(f"{expression.replace('*', '×').replace('-', '−')} = {result}")
            self.current_expression = result if "Ошибка" not in result else ""
            self.result_shown = True
            return result
        except Exception as e:
            return f"Ошибка: {str(e)}"

    def append_char(self, char: str):
        if self.result_shown and char in '0123456789.':
            self.current_expression = ""
            self.result_shown = False
        self.current_expression += char
        return self.current_expression.replace('*', '×').replace('-', '−').replace('^', 'x^y')

    def clear(self):
        self.current_expression = ""
        self.history = []
        self.result_shown = False
        return self.current_expression, self.history

    def backspace(self):
        if self.current_expression:
            self.current_expression = self.current_expression[:-1]
        return self.current_expression.replace('*', '×').replace('-', '−').replace('^', 'x^y')

    def get_history(self):
        return self.history