from abc import ABC, abstractmethod
from math import sin, cos, tan, log, sqrt, pi, log10
import re


class CalculatorComponent(ABC):
    @abstractmethod
    def calculate(self, expression: str) -> float:
        pass


class BaseCalculator(CalculatorComponent):
    def calculate(self, expression: str) -> float:
        try:
            # Vérification si l'expression contient des mots non mathématiques
            if re.search(r'[a-zA-Z]+', expression) and not any(
                    func in expression for func in ['sin', 'cos', 'tan', 'ln', 'sqrt', 'log', 'pi', 'e']):
                raise ValueError("Expression non valide : contient des mots non reconnus")

            # Préparation de l'expression avec remplacement de √ par sqrt
            expr = expression.replace('√', 'sqrt').replace('×', '*').replace('−', '-').replace('x^y', '**')

            # Environnement sécurisé avec constantes mathématiques
            safe_dict = {
                'sin': sin, 'cos': cos, 'tan': tan, 'ln': log, 'sqrt': sqrt,
                'pi': pi, 'e': 2.718281828459045, 'log': log10
            }
            return eval(expr, {"__builtins__": None}, safe_dict)
        except Exception as e:
            raise ValueError(f"Erreur de calcul : {str(e)}")


class HistoryDecorator(CalculatorComponent):
    def __init__(self, calculator: CalculatorComponent, history: list):
        self.calculator = calculator
        self.history = history

    def calculate(self, expression: str) -> float:
        result = self.calculator.calculate(expression)
        # Ajouter à l'historique uniquement si différent de la dernière entrée
        history_entry = f"{expression} = {result}"
        if not self.history or self.history[-1] != history_entry:
            self.history.append(history_entry)
        return result


class FormattingDecorator(CalculatorComponent):
    def __init__(self, calculator: CalculatorComponent):
        self.calculator = calculator

    def calculate(self, expression: str) -> float:
        result = self.calculator.calculate(expression)
        return round(result, 2)