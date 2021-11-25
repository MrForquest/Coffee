import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QWidget


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.loadTable()
        self.btnAddEdit.clicked.connect(self.open_add_edit)

    def loadTable(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM Coffee""").fetchall()
        con.close()

        title = "ID, название сорта, степень обжарки, молотый/в зернах, описание вкуса, цена, объем упаковки".split(
            ", ")
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)

        for i, row in enumerate(result):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

        self.tableWidget.resizeColumnsToContents()

    def open_add_edit(self):
        self.close()
        self.form = AddEditWidget()
        self.form.show()


class AddEditWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.btn_add.clicked.connect(self.insert_coffee)
        self.comboBox.currentIndexChanged.connect(self.update_edit_table)
        self.pushButton_2.clicked.connect(self.save_changes)
        self.title = "название сорта, степень обжарки, молотый/в зернах, описание вкуса, цена, объем упаковки".split(
            ", ")
        self.init_add_table()
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT id FROM Coffee""").fetchall()
        con.close()
        self.comboBox.clear()
        for i in result:
            self.comboBox.addItem(str(i[0]))

    def init_add_table(self):
        self.tableWidgetAdd.setColumnCount(len(self.title))
        self.tableWidgetAdd.setHorizontalHeaderLabels(self.title)
        self.tableWidgetAdd.setRowCount(1)
        default_data = ("", "", "", "", 0, 0)
        for j, elem in enumerate(default_data):
            self.tableWidgetAdd.setItem(0, j, QTableWidgetItem(str(elem)))
        self.tableWidgetAdd.resizeColumnsToContents()

    def insert_coffee(self):
        info = list()
        for i in range(6):
            info.append(self.tableWidgetAdd.item(0, i).text())
        if info[0] == "":
            self.label_error_add.setText("Кофе должно иметь имя")
            return
        info[5] = int(info[5])
        info[4] = int(info[4])
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        cur.execute("""INSERT INTO Coffee (name, roastDegree, gOrB, descFlavor, price, volume)
                        VALUES (?, ?, ?, ?, ?, ?)""", info)
        con.commit()
        con.close()
        self.label_error_add.setText("Ok")

        self.close()
        self.form = MyWidget()
        self.form.show()

    def update_edit_table(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        id_item = self.comboBox.currentText()
        self.selected_item = cur.execute(f"SELECT * FROM Coffee WHERE id={id_item}").fetchone()
        con.close()
        self.tableWidgetEdit.setColumnCount(len(self.title))
        self.tableWidgetEdit.setHorizontalHeaderLabels(self.title)
        self.tableWidgetEdit.setRowCount(1)
        for j, elem in enumerate(self.selected_item[1:]):
            self.tableWidgetEdit.setItem(0, j, QTableWidgetItem(str(elem)))
        self.tableWidgetEdit.resizeColumnsToContents()

    def save_changes(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        id_item = int(self.selected_item[0])
        info = list()
        for i in range(6):
            info.append(self.tableWidgetEdit.item(0, i).text())
        for i, v in enumerate("name, roastDegree, gOrB, descFlavor, price, volume".split(", ")):
            cur.execute(
                f"UPDATE Coffee SET {v}='{info[i]}' WHERE id={id_item}")
            con.commit()
        con.close()
        self.close()
        self.form = MyWidget()
        self.form.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec())
