# -*- coding: utf-8 -*-

import sys  # sys нужен для передачи argv в QApplication
import os
import re
import xml.dom.minidom as minidon
from PyQt5 import QtWidgets, QtCore, QtGui
import MyForm
import ErrorWindow


class AddBasesApp(QtWidgets.QMainWindow, MyForm.Ui_MainWindow):
    # Получение путь к фалу с базами 1С
    path_1C = os.environ["appdata"] + "\\1C\\1CEstart\\ibases.v8i"
    # Создаем словарь для баз и параметров их подключения
    dict_bases = {}
    # Зеленый цвет, если база уже добавлена
    colour_added = QtGui.QColor(175, 255, 163)

    def __init__(self):

        super().__init__()
        self.setupUi(self)

        # Данные для словаря с базами берем из XML файла с настройками
        if os.path.isfile("Settings.xml"):
            file_settings = minidon.parse("Settings.xml")
            rows_bases = file_settings.getElementsByTagName("RowDataBase")

            for row_add_bases in rows_bases:
                server_and_base = row_add_bases.getElementsByTagName("Base")[0].firstChild.data
                caption_base = row_add_bases.getElementsByTagName("Caption")[0].firstChild.data
                client_type = row_add_bases.getElementsByTagName("ClientType")[0].firstChild.data

                AddBasesApp.dict_bases[server_and_base] = [caption_base, False, client_type]
        else:
            dialog = ErrorWindow.ClssDialog(self, "Не найден файл с настройками, добавление баз невозможно!")
            dialog.exec_()

        if os.path.isfile(AddBasesApp.path_1C):

            # Чтение файла ibases.v8i для анализа текущих баз
            with open(AddBasesApp.path_1C, encoding='utf-8-sig') as Bases1C:
                for line in Bases1C:
                    mas_parser = re.findall('".*?"', line.rstrip().lower())

                    if len(mas_parser) == 2:
                        str_parser = "--".join(mas_parser)
                        value_dict = AddBasesApp.dict_bases.get(str_parser)

                        if value_dict != None:
                            value_dict[1] = True

            for item_base in AddBasesApp.dict_bases:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)

                chkBoxItem = QtWidgets.QTableWidgetItem()
                if AddBasesApp.dict_bases[item_base][1]:
                    flags = QtCore.Qt.ItemIsUserCheckable
                    check_state = QtCore.Qt.Checked
                    chkBoxItem.setBackground(AddBasesApp.colour_added)
                else:
                    flags = QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
                    check_state = QtCore.Qt.Unchecked
                chkBoxItem.setFlags(flags)
                chkBoxItem.setCheckState(check_state)
                self.tableWidget.setItem(rowPosition, 0, chkBoxItem)

                text_item_name = QtWidgets.QTableWidgetItem(AddBasesApp.dict_bases[item_base][0])
                text_item_name.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(rowPosition, 1, text_item_name)

                text_item_path = QtWidgets.QTableWidgetItem(item_base)
                text_item_path.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(rowPosition, 2, text_item_path)

            self.confirm.clicked.connect(self.edit_file_bases)
        else:
            dialog = ErrorWindow.ClssDialog(self, "Файл ibases.v8i не обнаружен, проверьте корректность установки 1С!")
            dialog.exec_()

    def edit_file_bases(self):

        mas_add = []

        # Чтение таблицы и по выбраным позициям запись в файл баз 1С
        for i in range(self.tableWidget.rowCount()):
            cur_row_check = self.tableWidget.item(i, 0)
            cur_row_base = self.tableWidget.item(i, 2).text()

            if (cur_row_check.checkState() == QtCore.Qt.Checked
                    and cur_row_check.flags() == QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled):
                mas_add.append([cur_row_base, i])

        try:
            if len(mas_add) > 0:
                with open(AddBasesApp.path_1C, "r+", encoding='utf-8-sig') as file_bases:
                    symbol_new_line = "\n" if len(file_bases.readlines()) > 0 else ""

                    for item_add in mas_add:
                        value_dict = AddBasesApp.dict_bases.get(item_add[0])
                        mas_connect = item_add[0].split("--")
                        str_connect = 'Connect=Srvr=' + mas_connect[0] + ';Ref=' + mas_connect[1] + ';'
                        strin_to_write = (symbol_new_line + "[" + value_dict[0] + "]\n" + str_connect
                                          + "\nClientConnectionSpeed=Normal\n" + value_dict[2] + "\nWA=1")
                        file_bases.write(strin_to_write)
                        symbol_new_line = "\n"
        except:
            dialog = ErrorWindow.ClssDialog(self, "Невозможно добавить базы, ошибка работы с файлом ibases.v8i!")
            dialog.exec_()
        else:
            for item_add in mas_add:
                cur_row_check = self.tableWidget.item(item_add[1], 0)
                cur_row_check.setFlags(QtCore.Qt.ItemIsUserCheckable)
                cur_row_check.setBackground(AddBasesApp.colour_added)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AddBasesApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
