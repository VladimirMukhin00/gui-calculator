import sys
from operator import add, sub, mul, truediv, pow

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFontDatabase

from design import Ui_MainWindow

operations = {
    '+':add,
    '-':sub,
    '*':mul,
    '/':truediv,
    '^':pow
}

error_zero_div = "На ноль делить низя!"
error_underfined = "И как ЭТО вычислять? (нолик)"

default_font_size = 16
default_entry_font_size = 40


class Calculator(QMainWindow):   
    def __init__(self):
        super(Calculator, self).__init__()   # запуск приложения QtDesign
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.entry_max_len = self.ui.le_entry.maxLength()

        QFontDatabase.addApplicationFont("fonts/Rubik-Regular.ttf")

        #digits
        self.ui.btn_0.clicked.connect(lambda: self.add_digit('0'))
        self.ui.btn_1.clicked.connect(lambda: self.add_digit('1'))
        self.ui.btn_2.clicked.connect(lambda: self.add_digit('2'))
        self.ui.btn_3.clicked.connect(lambda: self.add_digit('3'))
        self.ui.btn_4.clicked.connect(lambda: self.add_digit('4'))
        self.ui.btn_5.clicked.connect(lambda: self.add_digit('5'))
        self.ui.btn_6.clicked.connect(lambda: self.add_digit('6'))
        self.ui.btn_7.clicked.connect(lambda: self.add_digit('7'))
        self.ui.btn_8.clicked.connect(lambda: self.add_digit('8'))
        self.ui.btn_9.clicked.connect(lambda: self.add_digit('9'))

        #actions
        self.ui.btn_clear.clicked.connect(self.clear_all)
        self.ui.btn_ce.clicked.connect(self.clear_entry)
        self.ui.btn_point.clicked.connect(self.add_point)
        self.ui.btn_change.clicked.connect(self.negate)
        self.ui.btn_backspace.clicked.connect(self.backspace)

        #math
        self.ui.btn_equ.clicked.connect(self.calculate)
        self.ui.btn_plus.clicked.connect(lambda: self.add_temp('+'))
        self.ui.btn_sub.clicked.connect(lambda: self.add_temp('-'))
        self.ui.btn_mul.clicked.connect(lambda: self.add_temp('*'))
        self.ui.btn_div.clicked.connect(lambda: self.add_temp('/'))
        self.ui.btn_deg.clicked.connect(lambda: self.add_temp('^'))

    def show_error(self, text: str) -> None:  #показ ошибки
        self.ui.le_entry.setMaxLength(len(text))
        self.ui.le_entry.setText(text)

    def add_digit(self, btn_text: str) -> None: #добав цифр в поле ввода
        self.clear_temp_if_equality()
        if self.ui.le_entry.text() == '0':
            self.ui.le_entry.setText(btn_text)
        else:
            self.ui.le_entry.setText(self.ui.le_entry.text() + btn_text)
    
    def clear_all(self) -> None:  #очистка всех полей
        self.ui.le_entry.setText('0')
        self.ui.lbl_temp.clear()
    
    def clear_entry(self) -> None:  #очистка поля ввода
        self.clear_temp_if_equality()
        self.ui.le_entry.setText('0')

    def clear_temp_if_equality(self) -> None:  #очистка временного выражения при вводе
        if self.get_math_sign() == '=':
            self.ui.lbl_temp.clear()
    
    def add_point(self) -> None:    # точка
        self.clear_temp_if_equality()
        if '.' not in self.ui.le_entry.text():
            self.ui.le_entry.setText(self.ui.le_entry.text() + '.')
    
    @staticmethod
    def remove_trailing_zeros(num: str) -> str:  #обрезка незначащих нулей
        n = str(float(num))
        return n[:-2] if n[-2:] == '.0' else n

    def add_temp(self, math_sign: str):  #временное выражение сверху поля ввода
        if not self.ui.lbl_temp.text() or self.get_math_sign() == '=':
            self.ui.lbl_temp.setText(self.remove_trailing_zeros(self.ui.le_entry.text()) + f' {math_sign} ')
            self.ui.le_entry.setText('0')
    
    def get_entry_num(self) -> int | float:        #получение числа из поля ввода
        entry = self.ui.le_entry.text().strip('.')

        return float(entry) if '.' in entry else int(entry)
    
    def get_temp_num(self) -> int | float | None:  #получение числа из временного выражения
        if self.ui.lbl_temp.text():
            temp = self.ui.lbl_temp.text().strip('.').split()[0]
            return float(temp) if '.' in temp else int(temp)
    
    def get_math_sign(self) -> str | None:          #получение знака из временного выражения
        if self.ui.lbl_temp.text():
            return self.ui.lbl_temp.text().strip('.').split()[-1]
    
    def calculate(self) -> str | None:   # вычисление выражения (равенство)
        entry = self.ui.le_entry.text()
        temp = self.ui.lbl_temp.text()

        if temp:
            try:
                result = self.remove_trailing_zeros(
                    str(operations[self.get_math_sign()](self.get_temp_num(), self.get_entry_num()))
                )
                self.ui.lbl_temp.setText(temp + self.remove_trailing_zeros(entry) + ' =')
                self.ui.le_entry.setText(result)
                return result
            except KeyError:
                pass
            
            except TypeError:
                pass
            
            except ZeroDivisionError:      # при делении на ноль
                if self.get_temp_num() == 0:
                    self.show_error(error_underfined)
                else:
                    self.show_error(error_zero_div)


    def math_operation(self, math_sign: str):  #базовые мат. операции
        temp = self.ui.lbl_temp.text()

        if not temp:
            self.add_temp(math_sign)
        else:
            if self.get_math_sign() != math_sign:
                if self.get_math_sign() == '=':
                    self.add_temp(math_sign)
                else:
                    self.ui.lbl_temp.setText(temp[:-2] + f'{math_sign} ')
            else:
                self.ui.lbl_temp.setText(self.calculate() + f' {math_sign}')

    def negate(self):    # для отрицательных чисел
        self.clear_temp_if_equality()
        entry = self.ui.le_entry.text()

        if '-' not in entry:
            if entry != '0':
                entry = '-' + entry
        else:
            entry = entry[1:]
        
        if len(entry) == self.entry_max_len + 1 and '-' in entry:
            self.ui.le_entry.setMaxLength(self.entry_max_len + 1)
        else:
            self.ui.le_entry.setMaxLength(self.entry_max_len)

        self.ui.le_entry.setText(entry)
    
    def degree(self, math_sign = "^"):  # возведение в степень
        temp = self.ui.lbl_temp.text()

        if not temp:
            self.add_temp(math_sign)
        else:
            if self.get_math_sign() != math_sign:
                if self.get_math_sign() == '=':
                    self.add_temp(math_sign)
                else:
                    self.ui.lbl_temp.setText(temp[:-2] + f'{math_sign} ')
            else:
                self.ui.lbl_temp.setText(self.calculate() + f' {math_sign}')
    

    def backspace(self) -> None:   # кнопка бэкспейс
        self.clear_temp_if_equality()
        entry = self.ui.le_entry.text()

        if len(entry) != 1:
            if len(entry) == 2 and '-' in entry:
                self.ui.le_entry.setText('0')
            else:
                self.ui.le_entry.setText(entry[:-1])
        else:
            self.ui.le_entry.setText('0')



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Calculator()
    window.show()

    sys.exit(app.exec())