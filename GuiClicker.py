import time
import sys
import threading
import keyboard, mouse
from gui import Ui_AutoClicker
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

thread_running = True

class GuiClicker(Ui_AutoClicker):
    def __init__(self):
        self.running = False

    def setupUi(self, win):
        Ui_AutoClicker.setupUi(self, win)
        self.ToggleButton.clicked.connect(self.toggle_running)

    def toggle_running(self):
        self.running = not self.running
        self.OnOff.setText("On" if self.running else "OFF")

    def run(self):
        while thread_running:
            time.sleep(0.002)
            if self.running:
                if self.LeftClick.isChecked():
                    mouse.click()
                elif self.RightClick.isChecked():
                    mouse.right_click()
                else:
                    keyboard.send(self.PressText.text())

class Window(QMainWindow):
    def closeEvent(self, event):
        global thread_running
        thread_running = False

def main():
    app = QApplication(sys.argv)
    win = Window()
    gui = GuiClicker()
    gui.setupUi(win)
    win.show()
    th = threading.Thread(target = gui.run)
    th.start()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
