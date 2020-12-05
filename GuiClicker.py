import time
import sys
import threading
import keyboard, mouse
from gui import Ui_AutoClicker
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup

success_style_sheet = "background:white;color:black;"
error_style_sheet = "background:red;color:white;"

class GuiClicker(Ui_AutoClicker):
    def __init__(self):
        self.running = False

    def setupUi(self, win):
        Ui_AutoClicker.setupUi(self, win)
        self.ToggleButton.clicked.connect(self.toggle_running)
        self.toggle_key = self.TriggerText.text()
        keyboard.add_hotkey(self.toggle_key, self.toggle_running)
        self.TriggerText.textChanged.connect(self.change_toggle_key)
        self.PressText.textChanged.connect(self.change_press_text)
        self.LeftClick.stateChanged.connect(lambda: self.PseudoExclusive(self.LeftClick, self.RightClick))
        self.RightClick.stateChanged.connect(lambda: self.PseudoExclusive(self.RightClick, self.LeftClick))
        self.PseudoExclusive(self.LeftClick, self.RightClick)

    def toggle_running(self):
        self.running = not self.running
        self.OnOff.setText("ON" if self.running else "OFF")

    def change_press_text(self):
        try:
            keyboard.parse_hotkey(self.PressText.text())
            self.PressText.setStyleSheet(success_style_sheet)
        except:
            self.PressText.setStyleSheet(error_style_sheet)


    def change_toggle_key(self):
        try:
            new_toggle_key = self.TriggerText.text()
            if(new_toggle_key != self.toggle_key):
                keyboard.add_hotkey(new_toggle_key, self.toggle_running)
                keyboard.remove_hotkey(self.toggle_key)
                self.toggle_key = new_toggle_key
            self.TriggerText.setStyleSheet(success_style_sheet)
        except:
            self.TriggerText.setStyleSheet(error_style_sheet)

    def PseudoExclusive(self, b1, b2):
        if b1.checkState():
            b2.setCheckState(False)
            self.PressText.setDisabled(True)
        else:
            self.PressText.setDisabled(False)

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
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'): # make application look better on high def screen
        QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'): # make application look better on high def screen
        QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
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
