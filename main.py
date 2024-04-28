#Exception handling
#Logging to console to log file or dont show logging
#Benchmark ve brute force remove files after testing
import readchar
import sys
from select_compression import select_compression
from bcm import model_compression
from benchmark import benchmark
from brute_force import brute_force_compression
from create_config import create_config
from util import clear_screen


menu = ["Select compression algorithm",
        "Use BCM (AI) for auto algorithm selection",
        "Find best compression using brute force",
        "Get benchmark results for specific file",
        "Create config for custom compression algorithm"]


def print_menu(selected_row):
    clear_screen()
    print('\n\033[1mXCompress\033[0m is a tool for selecting best text compression algorithm for given input.')
    print('You can choose any algorithm you want, determine the best compression or fastest compression algorithm with BCM AI,')
    print('and select the best compression algorithm with brute force.\n')
    print("Please make selection:\n")
    for idx, row in enumerate(menu):
        if idx == selected_row:
            print("\033[32m->\033[0m", "\033[1m", row, "\033[0m")
        else:
            print("  ", row)
    print("Press q to quit")
    

def main():
    current_row = 0
    print_menu(current_row)
    while True:
        key = readchar.readkey()
        if key == readchar.key.UP and current_row > 0:
            current_row -= 1
        elif key == readchar.key.DOWN and current_row < 4:
            current_row += 1
        elif key == '\r' or key=='\n':
            sys.stdout.write("\033[F")  
            sys.stdout.write("\033[K")  
            if current_row == 0: select_compression()           
            if current_row == 1: select_compression()           
            if current_row == 2: select_compression()           
            if current_row == 3: select_compression()           
            if current_row == 4: select_compression()           
        elif key.lower() == 'q':
            break

        sys.stdout.write("\033[{}A".format(len(menu)))
        print_menu(current_row)

if __name__ == "__main__":
    main()
