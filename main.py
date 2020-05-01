import time
import mouse
import keyboard
from colorama import Fore, init
from sys import argv
init(autoreset=True)

def auto_press(press, start_stop_key):
    """TODO: Docstring for auto_press.

    :press_fn: TODO
    :trigger: TODO
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
    # argv[1] is the key to be repeated and
    # argv[2] is the key that triggers it
    start_stop_key = 'ctrl+shift'
    if len(argv) > 1:
        if argv[1] == '-l':
            press = lambda: mouse.click()
            print(Fore.CYAN + "left click" + Fore.RESET + " selected")
        elif argv[1] == '-r':
            press = lambda: mouse.right_click()
            print(Fore.CYAN + "right click" + Fore.RESET + " selected")
        else:
            press = lambda: keyboard.send(argv[1])
            print(Fore.CYAN + argv[1] + Fore.RESET + " selected")
        if len(argv) > 2:
            start_stop_key = argv[2]
    else:
        press = lambda: mouse.click()
        print(Fore.CYAN + "left click" + Fore.RESET + " selected")
    print("Press " + Fore.CYAN + start_stop_key + Fore.RESET + " to toggle clicker")
    return press, start_stop_key

def main():
    """main function
    :returns: None
    """
    press, start_stop_key = get_data(argv)
    auto_press(press, start_stop_key)
    
if __name__ == "__main__":
    main()
