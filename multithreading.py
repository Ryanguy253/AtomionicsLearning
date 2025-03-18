import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtCore import Qt

# Multithreading
from PyQt5.QtCore import QObject, QThread, pyqtSignal

import primeNumberFunction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multithreading GUI")
        self.setGeometry(0, 0, 500, 500)
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        vbox = QVBoxLayout()

        # Write Text On Top
        self.initInstructions(vbox)

        # Display Number 1 and Number 2
        hbox = QHBoxLayout()
        self.initNumberText(hbox)

        # Display Input Box
        inputhbox = QHBoxLayout()
        self.initInputBox(inputhbox)

        self.initButtons()

        vbox.addLayout(hbox)  # Add hbox to vertical layout
        vbox.addLayout(inputhbox)
        vbox.addWidget(self.calcButton)
        vbox.addWidget(self.clickButton)
        central_widget.setLayout(vbox)

    def initInstructions(self, vbox):
        primeText = QLabel("Insert 2 Numbers to find the Primes in between:", self)
        primeText.setFont(QFont("Arial", 15))
        primeText.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        vbox.addWidget(primeText)

    def initNumberText(self, hbox):
        text1 = QLabel("Number 1", self)
        text1.setFont(QFont("Arial", 10))
        text2 = QLabel("Number 2", self)
        text2.setFont(QFont("Arial", 10))
        hbox.addWidget(text1)
        hbox.addWidget(text2)
        hbox.setAlignment(Qt.AlignTop)

    def initInputBox(self, inputhbox):
        self.number1 = QLineEdit()
        self.number1.setPlaceholderText("Insert Number 1")
        self.number1.setValidator(QIntValidator(0, 9999999, self))

        self.number2 = QLineEdit()
        self.number2.setPlaceholderText("Insert Number 2")
        self.number2.setValidator(QIntValidator(0, 9999999, self))

        inputhbox.addWidget(self.number1)
        inputhbox.addWidget(self.number2)
        inputhbox.setAlignment(Qt.AlignTop)

    def initButtons(self):
        self.clickCount = 0
        self.calcButton = QPushButton("Calculate!", self)
        self.clickButton = QPushButton("Clicks : 0", self)

        self.calcButton.setStyleSheet("font-size:10px;")
        self.calcButton.clicked.connect(self.on_calculate)

        self.clickButton.setStyleSheet("font-size:10px;")
        self.clickButton.clicked.connect(self.on_click)

    def on_calculate(self):
        try:
            number1_value = int(self.number1.text())
            number2_value = int(self.number2.text())
        except ValueError:
            print("Insert a valid Int")
            return

        self.thread = QThread()
        self.worker = Worker(number1_value, number2_value)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.finished.connect(lambda: self.calcButton.setDisabled(False)) # Enable Button After Thread Finishes

        print("Thread Started")
        self.thread.start()

        # Disable Button
        self.calcButton.setDisabled(True)

    def on_click(self):
        self.clickCount += 1
        self.clickButton.setText(f"Clicks : {self.clickCount}")


class Worker(QObject):
    finished = pyqtSignal() # Class Variable
    progress = pyqtSignal(int)
    def __init__(self, start, stop):
        super().__init__()
        self.start = start
        self.stop = stop
        print("Worker Created")

    def run(self):
        print("Running Worker Function")
        result = primeNumberFunction.calculatePrimes(self.finished, self.progress, self.start, self.stop)
        print(result)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
