import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QTextEdit

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        # 解析并执行绘图命令
        # 注意：这里需要你自己实现解析和执行绘图命令的逻辑
        # 例如，如果你使用的是 matplotlib，你可能需要做类似以下的操作：
        # exec(f"import matplotlib.pyplot as plt; {plot_command}; plt.show()")
        self.label.setText("Button Clicked!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())