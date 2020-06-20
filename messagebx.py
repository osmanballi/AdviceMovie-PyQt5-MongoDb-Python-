from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap,QIcon
def messagebx(message):  
    msg = QMessageBox()
    msg.setWindowTitle("Warning")
    msg.setText(message)
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowIcon(QIcon("alarm.png"))
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_() 