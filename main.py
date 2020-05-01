import time
import mouse
import keyboard
from colorama import Fore, init
init(autoreset=True)

def main():
    start_stop_key = 'ctrl+shift'
    print("Press " + Fore.CYAN + start_stop_key + Fore.RESET + " to toggle clicker")
    while 1:
        print(Fore.RED + "Off")
        keyboard.wait(start_stop_key)
        print(Fore.GREEN + "On")
        time.sleep(0.2)
        while 1:
            mouse.click()
            time.sleep(0.002)
            if keyboard.is_pressed(start_stop_key):
                break
    
if __name__ == "__main__":
    main()
