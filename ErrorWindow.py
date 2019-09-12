from PyQt5 import QtWidgets


class ClssDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, text_error=""):
        super(ClssDialog, self).__init__(parent)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_text = QtWidgets.QLabel(self)
        self.label_text.setObjectName("label_text")
        self.verticalLayout.addWidget(self.label_text)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.btnClosed)
        self.verticalLayout.addWidget(self.pushButton)
        self.setWindowTitle("Сообщение об ошибке")
        self.pushButton.setText("ОК")
        self.label_text.setText(text_error)

    def btnClosed(self):
        self.close()
