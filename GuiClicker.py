import time
import sys
import threading
import keyboard, mouse
from gui import Ui_AutoClicker
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup

success_style_sheet = "QLineEdit{background:#1c1c1c;}QLineEdit:disabled{background:#555;color:#888}"
error_style_sheet = "QLineEdit{background:red}QLineEdit:disabled{background:#550000;color:#833}"
green_text_style_sheet = "color:green;"
red_text_style_sheet = "color:red;"

class GuiClicker(Ui_AutoClicker):
    """
    Inherit Ui_AutoClicker
    runs an autoclicker program
    """
    def __init__(self):
        """
        Constructor
        """

    def setupUi(self, win):
        """
        Call unctions neccisary to set up Ui
        """
        Ui_AutoClicker.setupUi(self, win) # call set up from inherited class
        self.set_running(False) # set running to false
        self.ToggleButton.clicked.connect(self.toggle_running) # make toggle button toggle running
        self.toggle_key = self.TriggerText.text() # get toggle key
        keyboard.add_hotkey(self.toggle_key, self.toggle_running) # add hotkey to toggle running at toggle key
        self.TriggerText.textChanged.connect(self.change_toggle_key) # when trigger text is changed update toggle key
        self.PressText.textChanged.connect(self.change_press_text) # when press text is changed update press text
        self.LeftClick.stateChanged.connect(lambda: self.PseudoExclusive(self.LeftClick, self.RightClick)) # when button state is changed call PseudoExclusive
        self.RightClick.stateChanged.connect(lambda: self.PseudoExclusive(self.RightClick, self.LeftClick)) # button state is changed call PseudoExclusive
        self.PseudoExclusive(self.LeftClick, self.RightClick) # call PseudoExclusive on left and right click button

    def set_running(self, b):
        """
        Set the running boolean
        """
        self.running = b # set running to b
        if self.running:
            self.OnOff.setText("ON") # change text in OnOff label
            self.OnOff.setStyleSheet(green_text_style_sheet) # set color green
        else:
            self.OnOff.setText("OFF") # change text in OnOff label
            self.OnOff.setStyleSheet(red_text_style_sheet) # set color red

    def toggle_running(self):
        """
        toggle the running boolean and change text
        """
        self.set_running(not self.running)

    def change_press_text(self):
        """
        check if hotkey in PressText is valid and change StyleSheet accordingly
        """
        try:
            keyboard.parse_hotkey(self.PressText.text()) # fails if text is invalid
            self.PressText.setStyleSheet(success_style_sheet) # set to non fail colorscheme
        except:
            self.PressText.setStyleSheet(error_style_sheet) # set to fail colorscheme


    def change_toggle_key(self):
        """
        Check if toggle key is valid and update it to a new hotkey
        """
        try:
            new_toggle_key = self.TriggerText.text() # read new toggle key
            if(new_toggle_key != self.toggle_key): # if toggle key isnt the same
                keyboard.add_hotkey(new_toggle_key, self.toggle_running) # add new hotkey
                keyboard.remove_hotkey(self.toggle_key) # remove previous hotkey
                self.toggle_key = new_toggle_key # update current hotkey to new hotkey
            self.TriggerText.setStyleSheet(success_style_sheet) # set success color
        except:
            self.TriggerText.setStyleSheet(error_style_sheet) # set failure color

    def PseudoExclusive(self, b1, b2):
        """
        Have the buttons be exclusive and if one is checked, disable PressText
        """
        if b1.checkState(): # if button one is checked
            b2.setCheckState(False) # uncheck button two
            self.PressText.setDisabled(True) # disable PressText
        else: # if button one is unchecked
            self.PressText.setDisabled(False) # enable PressText

    def run(self, win):
        """
        Run the main loop
        """
        while win.thread_running: # while the program is running
            time.sleep(0.002) # wait
            if self.running: # if the clicker is on
                if self.LeftClick.isChecked(): # if left click is checked
                    mouse.click() # click
                elif self.RightClick.isChecked(): # if right click is checked
                    mouse.right_click() # right click
                else: # if neither of the clicks are enabled
                    try:
                        keyboard.send(self.PressText.text()) # try to send the text in PressText
                    except:
                        pass

class Window(QMainWindow):
    """
    This is the window for a program
    """
    def __init__(self):
        """
        constructor
        """
        QMainWindow.__init__(self) # call parent constructor
        self.thread_running = True # if the program is running

    def closeEvent(self, event):
        """
        Make program stop running
        """
        self.thread_running = False # set running to false

def main():
    """
    Driver code
    """
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'): # make application look better on high def screen
        QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'): # make application look better on high def screen
        QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv) # get application object
    win = Window() # get window object
    gui = GuiClicker() # get the gui clicker object
    gui.setupUi(win) # set up the clicker object
    win.show() # show the window
    # a thread is used to not freeze application
    th = threading.Thread(target = gui.run, args=(win,)) # create a thread with program
    th.start() # run thread
    sys.exit(app.exec_()) # exit

if __name__ == "__main__": # if file is run directly
    main() # run driver code
