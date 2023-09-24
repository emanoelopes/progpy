from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import sys
from PyQt5.QtGui import QIcon


a = QApplication(sys.argv)

jan = QMainWindow()
jan.setGeometry(50, 50, 250, 300)
jan.resize(400, 300)
jan.move(500, 50)
jan.setWindowTitle("AnsibleLabs")

jan.show()

sys.exit(a.exec_())
