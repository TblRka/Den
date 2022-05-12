import PyQt5.QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QVBoxLayout, QPushButton)
#from PyQt5.QtGui import QIcon
import sys

from den import den

class BeginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
	
        self.text = QLabel("Привет! Меня зовут Дениска! Готов к работе", self)
        self.text.setFont(PyQt5.QtGui.QFont("Times", 20))
        self.text.setAlignment(Qt.AlignCenter)

        self.beginButton = QPushButton("Начать!")
        self.beginButton.setFont(PyQt5.QtGui.QFont("Times", 20, PyQt5.QtGui.QFont.Bold))
        self.beginButton.clicked.connect(den)

        vbox = QVBoxLayout()
        vbox.addWidget(self.text)
        vbox.addWidget(self.beginButton)

        self.setLayout(vbox)

        self.setGeometry(444, 300, 100, 300)
        self.setWindowTitle('Денис')
        #self.setWindowIcon(QIcon(''))
        self.show()

        return

    def run(self):
        self.close()
        self.destroy()
        app.quit()  
        den()
        
    def closeEvent(self, evnt):
        self.close()
        self.destroy()
        app.quit()
        
        
app = QApplication(sys.argv)
window = BeginWindow()
sys.exit(app.exec_())
