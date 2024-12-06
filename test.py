import pytest
from PySide6.QtWidgets import QApplication, QLineEdit, QLabel
from PySide6.QtCore import Qt
from main import Calculator

                                                                    # PYTEST
@pytest.fixture(scope="session")
def app():
    """Создание экземпляра QApplication для всех тестов."""
    app = QApplication.instance() or QApplication([])
    yield app
    app.quit()

@pytest.fixture
def calculator(app, qtbot):
    """Инициализация экземпляра калькулятора."""
    calc = Calculator()
    qtbot.addWidget(calc)
    calc.show()
    return calc


def test_add_digit(calculator, qtbot):
    """Тест добавления цифр."""
    qtbot.mouseClick(calculator.ui.btn_1, Qt.LeftButton)  # Используем Qt.LeftButton
    assert calculator.ui.le_entry.text() == "1"

    qtbot.mouseClick(calculator.ui.btn_2, Qt.LeftButton)  # Используем Qt.LeftButton
    assert calculator.ui.le_entry.text() == "12"


def test_clear_all(calculator, qtbot):
    """Тест очистки всех полей."""
    calculator.ui.le_entry.setText("123")
    calculator.ui.lbl_temp.setText("45 +")
    qtbot.mouseClick(calculator.ui.btn_clear, Qt.LeftButton)

    assert calculator.ui.le_entry.text() == "0"
    assert calculator.ui.lbl_temp.text() == ""


def test_add_point(calculator, qtbot):
    """Тест добавления десятичной точки."""
    qtbot.mouseClick(calculator.ui.btn_3, Qt.LeftButton)
    qtbot.mouseClick(calculator.ui.btn_point, Qt.LeftButton)
    assert calculator.ui.le_entry.text() == "3."

    qtbot.mouseClick(calculator.ui.btn_5, Qt.LeftButton)
    assert calculator.ui.le_entry.text() == "3.5"


def test_calculate_addition(calculator, qtbot):
    """Тест вычисления суммы."""
    qtbot.mouseClick(calculator.ui.btn_7, Qt.LeftButton)
    qtbot.mouseClick(calculator.ui.btn_plus, Qt.LeftButton)
    qtbot.mouseClick(calculator.ui.btn_5, Qt.LeftButton)
    qtbot.mouseClick(calculator.ui.btn_equ, Qt.LeftButton)

    assert calculator.ui.le_entry.text() == "12"


def test_calculate_division_by_zero(calculator, qtbot):
    """Тест деления на ноль."""
    qtbot.mouseClick(calculator.ui.btn_8, Qt.LeftButton)
    qtbot.mouseClick(calculator.ui.btn_div, Qt.LeftButton)
    qtbot.mouseClick(calculator.ui.btn_0, Qt.LeftButton)
    qtbot.mouseClick(calculator.ui.btn_equ, Qt.LeftButton)

    assert calculator.ui.le_entry.text() == "На ноль делить низя!"


def test_negate(calculator, qtbot):
    """Тест смены знака числа."""
    qtbot.mouseClick(calculator.ui.btn_4, Qt.LeftButton)
    qtbot.mouseClick(calculator.ui.btn_change, Qt.LeftButton)

    assert calculator.ui.le_entry.text() == "-4"

    qtbot.mouseClick(calculator.ui.btn_change, Qt.LeftButton)
    assert calculator.ui.le_entry.text() == "4"


def test_backspace(calculator, qtbot):
    """Тест кнопки Backspace."""
    qtbot.mouseClick(calculator.ui.btn_3, Qt.LeftButton)
    qtbot.mouseClick(calculator.ui.btn_2, Qt.LeftButton)
    qtbot.mouseClick(calculator.ui.btn_backspace, Qt.LeftButton)

    assert calculator.ui.le_entry.text() == "3"

    qtbot.mouseClick(calculator.ui.btn_backspace, Qt.LeftButton)
    assert calculator.ui.le_entry.text() == "0"
