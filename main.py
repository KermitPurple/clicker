import time
import mouse
import keyboard
from colorama import Fore, init
import sys
from gui import Ui_AutoClicker
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
init(autoreset=True)

class GuiClicker(Ui_AutoClicker):
    pass

def auto_press(press, start_stop_key):
    """TODO: Docstring for auto_press.

    :press: TODO
    :start_stop_key: TODO
    :returns: None

    """
    while 1:
        print(Fore.RED + "Off")
        keyboard.wait(start_stop_key)
        print(Fore.GREEN + "On")
        time.sleep(0.2)
        while 1:
            press()
            time.sleep(0.002)
            if keyboard.is_pressed(start_stop_key):
                break

def get_data(args):
    """gets the key to repeat and trigger
    :args: argument 1 is the name of key to press and argument two is the name of the trigger
    :returns: key press function and trigger key

    """
    # sys.argv[1] is the key to be repeated and
    # sys.argv[2] is the key that triggers it
    start_stop_key = 'ctrl+shift'
    if len(sys.argv) > 1:
        if sys.argv[1] == '-l':
            press = lambda: mouse.click()
            print(Fore.CYAN + "left click" + Fore.RESET + " selected")
        elif sys.argv[1] == '-r':
            press = lambda: mouse.right_click()
            print(Fore.CYAN + "right click" + Fore.RESET + " selected")
        else:
            press = lambda: keyboard.send(sys.argv[1])
            print(Fore.CYAN + sys.argv[1] + Fore.RESET + " selected")
        if len(sys.argv) > 2:
            start_stop_key = sys.argv[2]
    else:
        press = lambda: mouse.click()
        print(Fore.CYAN + "left click" + Fore.RESET + " selected")
    print("Press " + Fore.CYAN + start_stop_key + Fore.RESET + " to toggle clicker")
    return press, start_stop_key

def main():
    """main function
    :returns: None
    """
    # press, start_stop_key = get_data(sys.argv)
    # auto_press(press, start_stop_key)
    app = QApplication(sys.argv)
    win = QMainWindow()
    gui = GuiClicker()
    gui.setupUi(win)
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
