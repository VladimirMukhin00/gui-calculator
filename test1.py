from PySide6.QtTest import QTest
from PySide6.QtCore import Qt
from main import Calculator
import unittest


class TestCalculatorWithQtTest(unittest.TestCase):
    def setUp(self):
        """Инициализация приложения и калькулятора перед каждым тестом."""
        self.calculator = Calculator()
        self.calculator.show()

    def tearDown(self):
        """Закрытие приложения после каждого теста."""
        self.calculator.close()

    def test_add_digit(self):
        """Тест добавления цифр."""
        QTest.mouseClick(self.calculator.ui.btn_1, Qt.LeftButton)
        self.assertEqual(self.calculator.ui.le_entry.text(), "1")

        QTest.mouseClick(self.calculator.ui.btn_2, Qt.LeftButton)
        self.assertEqual(self.calculator.ui.le_entry.text(), "12")

    def test_clear_all(self):
        """Тест очистки всех полей."""
        self.calculator.ui.le_entry.setText("123")
        self.calculator.ui.lbl_temp.setText("45 +")
        QTest.mouseClick(self.calculator.ui.btn_clear, Qt.LeftButton)

        self.assertEqual(self.calculator.ui.le_entry.text(), "0")
        self.assertEqual(self.calculator.ui.lbl_temp.text(), "")

    def test_add_point(self):
        """Тест добавления десятичной точки."""
        QTest.mouseClick(self.calculator.ui.btn_3, Qt.LeftButton)
        QTest.mouseClick(self.calculator.ui.btn_point, Qt.LeftButton)
        self.assertEqual(self.calculator.ui.le_entry.text(), "3.")

        QTest.mouseClick(self.calculator.ui.btn_5, Qt.LeftButton)
        self.assertEqual(self.calculator.ui.le_entry.text(), "3.5")

    def test_calculate_addition(self):
        """Тест вычисления суммы."""
        QTest.mouseClick(self.calculator.ui.btn_7, Qt.LeftButton)
        QTest.mouseClick(self.calculator.ui.btn_plus, Qt.LeftButton)
        QTest.mouseClick(self.calculator.ui.btn_5, Qt.LeftButton)
        QTest.mouseClick(self.calculator.ui.btn_equ, Qt.LeftButton)

        self.assertEqual(self.calculator.ui.le_entry.text(), "12")

    def test_calculate_division_by_zero(self):
        """Тест деления на ноль."""
        QTest.mouseClick(self.calculator.ui.btn_8, Qt.LeftButton)
        QTest.mouseClick(self.calculator.ui.btn_div, Qt.LeftButton)
        QTest.mouseClick(self.calculator.ui.btn_0, Qt.LeftButton)
        QTest.mouseClick(self.calculator.ui.btn_equ, Qt.LeftButton)

        self.assertEqual(self.calculator.ui.le_entry.text(), "На ноль делить низя!")

    def test_negate(self):
        """Тест смены знака числа."""
        QTest.mouseClick(self.calculator.ui.btn_4, Qt.LeftButton)
        QTest.mouseClick(self.calculator.ui.btn_change, Qt.LeftButton)
        self.assertEqual(self.calculator.ui.le_entry.text(), "-4")

        QTest.mouseClick(self.calculator.ui.btn_change, Qt.LeftButton)
        self.assertEqual(self.calculator.ui.le_entry.text(), "4")

    def test_backspace(self):
        """Тест кнопки Backspace."""
        QTest.mouseClick(self.calculator.ui.btn_3, Qt.LeftButton)
        QTest.mouseClick(self.calculator.ui.btn_2, Qt.LeftButton)
        QTest.mouseClick(self.calculator.ui.btn_backspace, Qt.LeftButton)
        self.assertEqual(self.calculator.ui.le_entry.text(), "3")

        QTest.mouseClick(self.calculator.ui.btn_backspace, Qt.LeftButton)
        self.assertEqual(self.calculator.ui.le_entry.text(), "0")
