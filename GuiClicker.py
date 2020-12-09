import time
import sys
import threading
import keyboard, mouse
from gui import Ui_AutoClicker
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup

success_style_sheet = "QLineEdit{background:#1c1c1c;border: 2px solid #555;}QLineEdit:disabled{background:#666;border:2px solid #888}"
error_style_sheet = "QLineEdit{background:red;border:2px solid #a55;}QLineEdit:disabled{background:#550000;color:#833}"
green_text_style_sheet = "QPushButton{color:green;background:#1c1c1c;border: 2px solid #555;}"
red_text_style_sheet = "QPushButton{color:red;background:#1c1c1c;border: 2px solid #555;}"

class GuiClicker(Ui_AutoClicker, QtCore.QThread):
    """
    Inherit Ui_AutoClicker
    runs an autoclicker program
    """
    toggle_signal = QtCore.pyqtSignal()

    def __init__(self, win):
        """
        Constructor
        """
        QtCore.QThread.__init__(self)
        self.count = 0
        self.setupUi(win) #set up the ui

    def setupUi(self, win):
        """
        Call unctions neccisary to set up Ui
        """
        Ui_AutoClicker.setupUi(self, win) # call set up from inherited class
        self.set_running(False) # set running to false
        self.ToggleButton.clicked.connect(self.toggle_running) # make toggle button toggle running
        self.toggle_key = self.TriggerText.text() # get toggle key
        self.TriggerText.textChanged.connect(self.change_toggle_key) # when trigger text is changed update toggle key
        self.PressText.textChanged.connect(self.change_press_text) # when press text is changed update press text
        self.LeftClick.stateChanged.connect(lambda: self.PseudoExclusive(self.LeftClick, self.RightClick)) # when button state is changed call PseudoExclusive
        self.RightClick.stateChanged.connect(lambda: self.PseudoExclusive(self.RightClick, self.LeftClick)) # button state is changed call PseudoExclusive
        self.PseudoExclusive(self.LeftClick, self.RightClick) # call PseudoExclusive on left and right click button
        self.toggle_signal.connect(self.toggle_running) # when thread is run, call self.toggle_running synchronously
        keyboard.add_hotkey(self.toggle_key, self.toggle_signal.emit, None) # add hotkey to toggle running at run thread
        self.text = self.PressText.text() # get text to print
        self.repeat_forever = self.InfiniteRepetitionsBox.isChecked()
        self.InfiniteRepetitionsBox.stateChanged.connect(self.update_repetitions_box)
        self.repetitions = self.RepetitionsBox.value()
        self.RepetitionsBox.valueChanged.connect(self.update_repetitions)

    def update_repetitions(self):
        self.repetitions = self.RepetitionsBox.value()

    def update_repetitions_box(self):
        self.repeat_forever = self.InfiniteRepetitionsBox.isChecked()
        self.RepetitionsBox.setEnabled(not self.repeat_forever)

    def set_running(self, b): # do not call in a thread or may crash
        """
        Set the running boolean
        """
        self.running = b # set running to b
        if self.running: # qt objects are not thread safe
            self.ToggleButton.setText("ON") # change text in OnOff label
            self.ToggleButton.setStyleSheet(green_text_style_sheet) # set color green
        else:
            self.ToggleButton.setText("OFF") # change text in OnOff label
            self.ToggleButton.setStyleSheet(red_text_style_sheet) # set color red

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
            text = self.PressText.text()
            keyboard.parse_hotkey(text) # fails if text is invalid
            self.text = text
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
                keyboard.add_hotkey(new_toggle_key, self.toggle_signal.emit, None) # add new hotkey
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
            time.sleep(self.DelayBox.value()) # wait
            if self.running: # if the clicker is on
                if self.LeftClick.isChecked(): # if left click is checked
                    mouse.click() # click
                elif self.RightClick.isChecked(): # if right click is checked
                    mouse.right_click() # right click
                else: # if neither of the clicks are enabled
                    keyboard.send(self.text) # try to send the text in PressText
                if not self.repeat_forever:
                    self.count += 1
                    if self.count >= self.repetitions:
                        self.count = 0
                        self.toggle_signal.emit(None)

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
    gui = GuiClicker(win) # get the gui clicker object
    win.show() # show the window
    # a thread is used to not freeze application
    th = threading.Thread(target = gui.run, args=(win,)) # create a thread with program
    th.start() # run thread
    sys.exit(app.exec_()) # exit

if __name__ == "__main__": # if file is run directly
    main() # run driver code
