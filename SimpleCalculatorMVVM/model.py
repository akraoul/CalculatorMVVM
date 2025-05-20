import math


class CalculatorModel:
    def calculate(self, expression: str) -> str:
        try:
            # Нормализация выражения
            expr = expression.replace('×', '*').replace('÷', '/').replace('−', '-')
            expr = expr.replace('sin', 'math.sin').replace('cos', 'math.cos')
            expr = expr.replace('tan', 'math.tan').replace('ln', 'math.log')
            expr = expr.replace('√', 'math.sqrt').replace('π', 'math.pi')
            expr = expr.replace('e', 'math.e').replace('log', 'math.log10')
            expr = expr.replace('^', '**').replace('%', '/100*')

            result = eval(expr, {"math": math, "__builtins__": {}})
            return str(round(result, 8))
        except Exception as e:
            return f"Ошибка: {str(e)}"