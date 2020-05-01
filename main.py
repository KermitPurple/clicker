import time
import mouse
import keyboard
from colorama import Fore, init
from sys import argv
init(autoreset=True)

def main():
    start_stop_key = 'ctrl+shift'
    if len(argv) > 1:
        arg = " ".join(argv[1:])
        if arg == '-r':
            press = lambda: mouse.right_click()
            print(Fore.CYAN + "right click" + Fore.RESET + " selected")
        else:
            press = lambda: keyboard.send(arg)
            print(Fore.CYAN + arg + Fore.RESET + " selected")
    else:
        press = lambda: mouse.click()
        print(Fore.CYAN + "left click" + Fore.RESET + " selected")
    print("Press " + Fore.CYAN + start_stop_key + Fore.RESET + " to toggle clicker")
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
    
if __name__ == "__main__":
    main()
