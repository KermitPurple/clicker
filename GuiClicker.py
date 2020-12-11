import time
import sys
import threading
import keyboard, mouse
from gui import Ui_AutoClicker
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup

success_style_sheet = "QLineEdit{background:#1c1c1c;border: 2px solid #555;}QLineEdit:disabled{background:#666;border:2px solid #888}" # colors to set QLineEdit to on success
error_style_sheet = "QLineEdit{background:red;border:2px solid #a55;}QLineEdit:disabled{background:#550000;color:#833}" # colors to set QLineEdit to on error
green_text_style_sheet = "QPushButton{color:green;background:#1c1c1c;border: 2px solid #555;}QPushButton:hover{background:#252525}" # colors to set QPushButton when self.running is true
red_text_style_sheet = "QPushButton{color:red;background:#1c1c1c;border: 2px solid #555;}QPushButton:hover{background:#252525}" # colors to set QPushButton when self.running is false

class GuiClicker(Ui_AutoClicker, QtCore.QThread):
    """
    Inherit Ui_AutoClicker
    runs an autoclicker program
    """
    toggle_signal = QtCore.pyqtSignal() # signal to toggle self.running

    def __init__(self, win):
        """
        Constructor
        """
        super().__init__() # call super constructor
        self.count = 0 # how many clicks have happened; only if self.repeat_forever is false
        self.hotkey = None
        self.mouse_hotkey = None
        self.setupUi(win) #set up the ui

    def setupUi(self, win):
        """
        Call unctions neccisary to set up Ui
        """
        Ui_AutoClicker.setupUi(self, win) # call set up from inherited class
        self.set_running(False) # set running to false
        self.ToggleButton.clicked.connect(self.toggle_running) # make toggle button toggle running
        self.TriggerText.textChanged.connect(self.change_toggle_key) # when trigger text is changed update toggle key
        self.PressText.textChanged.connect(self.change_press_text) # when press text is changed update press text
        self.toggle_signal.connect(self.toggle_running) # when thread is run, call self.toggle_running synchronously
        self.change_toggle_key() # set the hotkey
        self.text = self.PressText.text() # get text to print
        self.update_repetitions_box() # repeats forever if box is checked
        self.InfiniteRepetitionsBox.stateChanged.connect(self.update_repetitions_box) # update repeats forever when box is changed
        self.update_repetitions() # get number of repititions
        self.RepetitionsBox.valueChanged.connect(self.update_repetitions) # get the number of repititions when the number changes
        self.update_output_selection() # get output_selection value
        self.OutputBox.currentIndexChanged.connect(self.update_output_selection) # connect getting value with change in index
        self.update_toggle_selection() # get toggle_selection value
        self.ToggleBox.currentTextChanged.connect(self.update_toggle_selection) # connect getting value with change in index
        self.SuppressBox.stateChanged.connect(self.change_toggle_key)

    def update_output_selection(self):
        """
        get output selection
        set enabled states of PressText
        """
        self.output_selection = self.OutputBox.currentText() # get value of output box
        self.PressText.setEnabled(self.output_selection == 'Keyboard') # enable press text if keyboard is selected

    def update_toggle_selection(self):
        """
        get toggle_selection
        update hotkeys
        change enabled status of trigger text
        """
        self.toggle_selection = self.ToggleBox.currentText() # get value of toggle box
        enabled = self.toggle_selection == 'Keyboard'
        self.TriggerText.setEnabled(enabled) # enable trigger text if keyboard is selected
        self.SuppressBox.setEnabled(enabled) # enable SuppressBox if keyboard is selected
        if self.toggle_selection == 'Keyboard': # if keyboard is selected
            self.remove_toggle_mouse() # remove the mouse hook
            self.change_toggle_key() # set the toggle key
        else: # keyboard is not selected
            self.remove_toggle_key() # remove hotkey hook
            self.change_toggle_mouse() # set the mouse hotkey

    def update_repetitions(self):
        """
        save repitions box value
        """
        self.repetitions = self.RepetitionsBox.value() # save value

    def update_repetitions_box(self):
        """
        Get new repeat value from RepetitionsBox
        change enabled status on RepetitionsBox
        restart count
        """
        self.repeat_forever = self.InfiniteRepetitionsBox.isChecked() # get the check box value
        self.RepetitionsBox.setEnabled(not self.repeat_forever) # disable if box is checked
        self.count = 0 # restart count

    def set_running(self, b): # do not call in a thread or may crash
        """
        Set the running boolean
        """
        self.running = b # set running to b
        if self.running: # qt objects are not thread safe
            self.ToggleButton.setText("ON") # change text in OnOff label
            self.ToggleButton.setStyleSheet(green_text_style_sheet) # set color green
        else: # if self.runnning is false
            self.ToggleButton.setText("OFF") # change text in OnOff label
            self.ToggleButton.setStyleSheet(red_text_style_sheet) # set color red

    def toggle_running(self):
        """
        toggle the running boolean and change text
        """
        self.set_running(not self.running) # set running to opposite of running

    def change_press_text(self):
        """
        check if hotkey in PressText is valid and change StyleSheet accordingly
        """
        try:
            text = self.PressText.text() # get text
            keyboard.parse_hotkey(text) # fails if text is invalid
            self.text = text # if the text doesn't fail save it 
            self.PressText.setStyleSheet(success_style_sheet) # set to non fail colorscheme
        except:
            self.PressText.setStyleSheet(error_style_sheet) # set to fail colorscheme

    def remove_toggle_key(self):
        """
        Remove the toggle key if it exists
        """
        if self.hotkey != None:
            try:
                keyboard.remove_hotkey(self.hotkey) # remove previous hotkey
            except: pass
            self.hotkey = None

    def change_toggle_key(self):
        """
        Check if toggle key is valid and update it to a new hotkey
        """
        try:
            self.remove_toggle_key()
            self.hotkey = keyboard.add_hotkey(self.TriggerText.text(), self.toggle_signal.emit, suppress = self.SuppressBox.isChecked()) # add new hotkey
            self.TriggerText.setStyleSheet(success_style_sheet) # set success color
        except:
            self.hotkey = None
            self.TriggerText.setStyleSheet(error_style_sheet) # set failure color

    def remove_toggle_mouse(self):
        """
        Remove the mouse toggle key if it exists
        """
        if self.mouse_hotkey != None:
            mouse.unhook(self.mouse_hotkey)
            self.mouse_hotkey = None

    def change_toggle_mouse(self):
        """
        Change the mouse hotkey
        """
        self.remove_toggle_mouse()
        if self.toggle_selection == 'Left Click':
            button = mouse.LEFT
        elif self.toggle_selection == 'Right Click':
            button = mouse.RIGHT
        elif self.toggle_selection == 'Middle Click':
            button = mouse.MIDDLE
        elif self.toggle_selection == 'Mouse4':
            button = mouse.X
        elif self.toggle_selection == 'Mouse5':
            button = mouse.X2
        self.mouse_hotkey = mouse.on_button(self.toggle_signal.emit, buttons = button, types = mouse.UP) # add mouse hotkey

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
                if self.output_selection == 'Keyboard':
                    keyboard.send(self.text) # try to send the text in PressText
                elif self.output_selection == 'Left Click':
                    mouse.click() # click with the mouse
                elif self.output_selection == 'Right Click':
                    mouse.right_click() # right click with the mouse
                elif self.output_selection == 'Middle Click':
                    mouse.click(mouse.MIDDLE) # middle click
                elif self.output_selection == 'Mouse4':
                    mouse.click(mouse.X) # press mouse4
                elif self.output_selection == 'Mouse5':
                    mouse.click(mouse.X2) # press mouse5
                if not self.repeat_forever: # if it is not an infinite clicking loop
                    self.count += 1 # increment count
                    if self.count >= self.repetitions: # if the count is higher than max count
                        self.count = 0 # reset count
                        self.toggle_signal.emit() # emit signal causing self.running to toggle

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

def new_win():
    win = Window() # get window object
    gui = GuiClicker(win) # get the gui clicker object
    win.show() # show the window
    # a thread is used to not freeze application
    th = threading.Thread(target = gui.run, args=(win,)) # create a thread with program
    th.start() # run thread

def main():
    """
    Driver code
    """
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'): # make application look better on high def screen
        QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'): # make application look better on high def screen
        QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv) # get application object
    new_win()
    new_win()
    sys.exit(app.exec_()) # exit

if __name__ == "__main__": # if file is run directly
    main() # run driver code
