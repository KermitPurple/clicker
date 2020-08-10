import time
import sys
import threading
import keyboard, mouse
from gui import Ui_AutoClicker
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

class GuiClicker(Ui_AutoClicker):
    def __init__(self):
        self.running = False

    def setupUi(self, win):
        Ui_AutoClicker.setupUi(self, win)
        self.ToggleButton.clicked.connect(self.toggle_running)
        self.toggle_key = keyboard.add_hotkey(self.TriggerText.text(), self.toggle_running)
        self.TriggerText.textChanged.connect(self.change_toggle_key)

    def toggle_running(self):
        self.running = not self.running
        self.OnOff.setText("ON" if self.running else "OFF")

    def change_toggle_key(self):
        try:
            new_toggle_key = keyboard.add_hotkey(self.TriggerText.text(), self.toggle_running)
        except:
            return
        keyboard.remove_hotkey(self.toggle_key)
        self.toggle_key = new_toggle_key

    def run(self, win):
        while win.thread_running:
            time.sleep(0.002)
            if self.running:
                if self.LeftClick.isChecked():
                    mouse.click()
                elif self.RightClick.isChecked():
                    mouse.right_click()
                else:
                    try:
                        keyboard.send(self.PressText.text())
                    except:
                        pass

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.thread_running = True

    def closeEvent(self, event):
        self.thread_running = False

def main():
    app = QApplication(sys.argv)
    win = Window()
    gui = GuiClicker()
    gui.setupUi(win)
    win.show()
    th = threading.Thread(target = gui.run, args=(win,))
    th.start()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
