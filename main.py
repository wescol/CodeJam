import time
import getpass
import os
import sys
from colorama import Fore, Style
from termcolor import cprint
from random import uniform
import subprocess
import numpy as np

class player:
    decisions = np.array([])
    inventory = np.array(["cyberdeck"])
    abilities = np.array([])
    status = np.array([])
    name = "Neural Operative"
    level = 1
    score = 0
    
def read_single_keypress():
    """Waits for a single keypress on stdin.

    This is a silly function to call if you need to do it a lot because it has
    to store stdin's current setup, setup stdin for reading single keystrokes
    then read the single keystroke then revert stdin back after reading the
    keystroke.

    Returns a tuple of characters of the key that was pressed - on Linux, 
    pressing keys like up arrow results in a sequence of characters. Returns 
    ('\x03',) on KeyboardInterrupt which can happen when a signal gets
    handled.

    """
    import termios, fcntl, sys, os
    fd = sys.stdin.fileno()
    # save old state
    flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
    attrs_save = termios.tcgetattr(fd)
    # make raw - the way to do this comes from the termios(3) man page.
    attrs = list(attrs_save) # copy the stored version to update
    # iflag
    attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK
                  | termios.ISTRIP | termios.INLCR | termios. IGNCR
                  | termios.ICRNL | termios.IXON )
    # oflag
    attrs[1] &= ~termios.OPOST
    # cflag
    attrs[2] &= ~(termios.CSIZE | termios. PARENB)
    attrs[2] |= termios.CS8
    # lflag
    attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
                  | termios.ISIG | termios.IEXTEN)
    termios.tcsetattr(fd, termios.TCSANOW, attrs)
    # turn off non-blocking
    fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
    # read a single keystroke
    ret = []
    try:
        ret.append(sys.stdin.read(1)) # returns a single character
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save | os.O_NONBLOCK)
        c = sys.stdin.read(1) # returns a single character
        while len(c) > 0:
            ret.append(c)
            c = sys.stdin.read(1)
    except KeyboardInterrupt:
        ret.append('\x03')
    finally:
        # restore old state
        termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
    return tuple(ret)

def title() -> None:
    print(chr(27) + "[2J")
    time.sleep(1)
    cprint(Fore.LIGHTMAGENTA_EX + "- presenting -".center(os.get_terminal_size().columns), attrs=['dark'])
    for i in range(9):
        print("\n")
    time.sleep(2)
    print(chr(27) + "[2J")
    time.sleep(1)
    cprint(Style.RESET_ALL)

    cprint(Fore.RED + "                                                                                       ".center(os.get_terminal_size().columns), attrs=['blink','dark'])
    cprint(Fore.RED + "                                                                                       ".center(os.get_terminal_size().columns), attrs=['blink','dark'])
    cprint(Fore.RED + "                                                                                       ".center(os.get_terminal_size().columns), attrs=['blink','dark'])
    cprint(Fore.GREEN + " ███▄    █ ▓█████  █    ██  ██▀███   ▄▄▄       ██▓        ██▓     ██▓ ███▄    █  ██ ▄█▀".center(os.get_terminal_size().columns), attrs=['blink','dark'])
    cprint(Fore.GREEN + " ██ ▀█   █ ▓█   ▀  ██  ▓██▒▓██ ▒ ██▒▒████▄    ▓██▒       ▓██▒    ▓██▒ ██ ▀█   █  ██▄█▒ ".center(os.get_terminal_size().columns), attrs=['blink','dark'])
    cprint(Fore.GREEN + "▓██  ▀█ ██▒▒███   ▓██  ▒██░▓██ ░▄█ ▒▒██  ▀█▄  ▒██░       ▒██░    ▒██▒▓██  ▀█ ██▒▓███▄░ ".center(os.get_terminal_size().columns), attrs=['blink','dark'])
    cprint(Fore.GREEN + "▓██▒  ▐▌██▒▒▓█  ▄ ▓▓█  ░██░▒██▀▀█▄  ░██▄▄▄▄██ ▒██░       ▒██░    ░██░▓██▒  ▐▌██▒▓██ █▄ ".center(os.get_terminal_size().columns), attrs=['blink','dark'])
    cprint(Fore.GREEN + "▒██░   ▓██░░▒████▒▒▒█████▓ ░██▓ ▒██▒ ▓█   ▓██▒░██████▒   ░██████▒░██░▒██░   ▓██░▒██▒ █▄".center(os.get_terminal_size().columns), attrs=['blink','dark'])
    cprint(Fore.GREEN + "░ ▒░   ▒ ▒ ░░ ▒░ ░░▒▓▒ ▒ ▒ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ▒░▓  ░   ░ ▒░▓  ░░▓  ░ ▒░   ▒ ▒ ▒ ▒▒ ▓▒".center(os.get_terminal_size().columns), attrs=['blink','dark'])
    cprint(Fore.GREEN + "░ ░░   ░ ▒░ ░ ░  ░░░▒░ ░ ░   ░▒ ░ ▒░  ▒   ▒▒ ░░ ░ ▒  ░   ░ ░ ▒  ░ ▒ ░░ ░░   ░ ▒░░ ░▒ ▒░".center(os.get_terminal_size().columns), attrs=['blink','dark'])
    cprint(Fore.GREEN + "   ░   ░ ░    ░    ░░░ ░ ░   ░░   ░   ░   ▒     ░ ░        ░ ░    ▒ ░   ░   ░ ░ ░ ░░ ░ ".center(os.get_terminal_size().columns), attrs=['blink','dark'])
    cprint(Fore.GREEN + "         ░    ░  ░   ░        ░           ░  ░    ░  ░       ░  ░ ░           ░ ░  ░   ".center(os.get_terminal_size().columns), attrs=['blink','dark'])
    cprint(Fore.RED + "                                                                                       ".center(os.get_terminal_size().columns), attrs=['blink','dark'])
    cprint(Fore.RED + "                                                                                       ".center(os.get_terminal_size().columns), attrs=['blink','dark'])
    for i in range(9):
        print("\n")
    time.sleep(2)
    
    #getpass.getpass(Fore.LIGHTMAGENTA_EX + " press any key to enter the future ".center(os.get_terminal_size().columns))
    print(Fore.LIGHTMAGENTA_EX + "".center(int(os.get_terminal_size().columns/3)), end='')
    for x in ' press any key to enter the future ':
            cprint(Fore.LIGHTMAGENTA_EX + x, end='')
            sys.stdout.flush()
            time.sleep(0.03)
    print('', end='\n')
    read_single_keypress()

def intro(x: player) -> None:
    print(chr(27) + "[2J")
    x.name = input(Fore.LIGHTMAGENTA_EX + "enter player name: " + Fore.RED)
    print(chr(27) + "[2J")
    for x in '2079 A.D.':
            cprint(Fore.GREEN + x, attrs=['dark'], end='')
            sys.stdout.flush()
            time.sleep(uniform(0,0.04))
    print('', end='\n\n')

    time.sleep(1)

    nlines = 2
    # scroll up to make room for output
    print(f"\033[{nlines}S", end="")

    # move cursor back up
    print(f"\033[{nlines}A", end="")

    # save current cursor position
    print("\033[s", end="")

    for t in range(10):
        # restore saved cursor position
        print("\033[u", end="")
        print(f"Line one @ {t}")
        print(f"Line two @ {t}")
        t += 1
        time.sleep(.5)

def level_1():
    def level_start() -> None:    
        print(chr(27) + "[2J")
        for x in 'You find yourself in the center of a room.':
                cprint(Fore.LIGHTMAGENTA_EX + x, attrs=[], end='')
                sys.stdout.flush()
                time.sleep(uniform(0,0.04))
        print('', end='\n\n')
        time.sleep(1)
        for x in 'A single light hangs dimly above you. ':
                cprint(Fore.LIGHTMAGENTA_EX + x, attrs=[], end='')
                sys.stdout.flush()
                time.sleep(uniform(0,0.04))
        time.sleep(1.5)
        for x in 'It\'s dark. ':
                cprint(Fore.LIGHTMAGENTA_EX + x, attrs=[], end='')
                sys.stdout.flush()
                time.sleep(uniform(0,0.04))
        time.sleep(2)
        print('', end='\n')
        for x in '\nAnd cold.':
                cprint(Fore.LIGHTMAGENTA_EX + x, attrs=[], end='')
                sys.stdout.flush()
                time.sleep(uniform(0,0.04))
        print('', end='\n\n')
        time.sleep(1.5)
        print('', end='\n\n')

    level_start()
    print('What will you do?')
    time.sleep(2)
    
    

def play_game()-> int:
    current_player = player
    title()
    intro(player)
    level_1()

    return current_player.score

play_game()
 
#nlines = 2
#    # scroll up to make room for output
#print(f"\033[{nlines}S", end="")
#
#    # move cursor back up
#print(f"\033[{nlines}A", end="")
#
#    # save current cursor position
#print("\033[s", end="")
#
#x = '░'
#for t in range(21):
#    # restore saved cursor position
#    print("\033[u", end="")
#    print(f"Line one @ {x}")
#    print(f"Line two @ {x}")
#    
#    if t%2 == 0:
#        x = '▒'
#    elif t%3 == 0:
#        x = '▓'
#    time.sleep(.1)





