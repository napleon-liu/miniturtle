import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QTextEdit
from parser.parser import Parser
from semantics import Semantics


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.semantics = None
        self.parser = None
        self.setWindowTitle("Miniturtle")
        self.setGeometry(100, 100, 300, 200)

        self.label = QLabel("请输入您要执行的绘图语句：", self)
        self.label.setGeometry(50, 50, 200, 30)

        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(50, 80, 500, 500)  # 调整文本框的大小

        self.button = QPushButton("执行绘图语句", self)
        self.button.setGeometry(250, 600, 100, 30)
        self.button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        plot_command = self.textEdit.toPlainText()
        file = open("test.txt", "w")
        file.write(plot_command)
        file.close()

        self.parser = Parser("test.txt")
        self.semantics = Semantics(self.parser)
        self.semantics.parse()
        self.semantics.run()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
