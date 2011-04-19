#!/usr/bin/env python
import curses, traceback
import sys
import pickle
import cipher_tools.dictionary

def main(stdscr):
    global screen
    screen = stdscr

    cipher_file = sys.argv[1]
    f = open(cipher_file, 'r')
    cipher = f.readlines()
    f.close()

    f = open('cipher_tools/dictionary.db', 'rb')
    dictionary = pickle.load(f)
    f.close()
   
    x = 0
    while x != ord('9'):
        if x != ord('4'):
            screen.erase()
        
        # Menu
        screen.addstr(0, 1, '1: Replace |')
        screen.addstr(0, 14, '2: Undo |')
        screen.addstr(0, 24, '3: Redo |')
        screen.addstr(0, 34, '4: Dictionary |')
        screen.addstr(0, 50, '8: Save |')
        screen.addstr(0, 60, '9: Quit')

        # Print Cipher blob
        count = 4
        for i in cipher:
            screen.addstr(count, 2, i)
            count += 1
       
        # Draw conntent
        screen.refresh()
        
        # Get Keyboard input
        x = screen.getch()

        if x == ord('1'):
            # Ask question to replace
            curses.echo()
            screen.addstr(count, 2, 'Replace: ')
            screen.refresh()
            replace = chr(screen.getch())

            screen.addstr(count + 1, 2, 'Replace with: ')
            screen.refresh()
            replacewith = chr(screen.getch())
            curses.noecho()

            newcipher = []
            for i in cipher:
                i = i.replace(replace, replacewith)
                newcipher.append(i)

            # Build our undo only if the previous undo
            # doesn't match
            try:
                if cipher != undo:
                    undo = cipher
            except UnboundLocalError:
                undo = cipher

            cipher = newcipher

        if x == ord('2'):

            # If my undo and current cipher match
            # we are last undo
            if undo == cipher:
                continue

            try:
                redo = cipher
                cipher = undo
            except UnboundLocalError:
                continue

        if x == ord('3'):
            try:
                cipher = redo
            except UnboundLocalError:
                continue
        
        if x == ord('4'):
            curses.echo()
            curses.nocbreak()
            # clear line
            screen.addstr(2, 1, ' '*200)
            screen.refresh()

            screen.addstr(2, 1, 'Expression: ')
            user_input = screen.getstr()
            curses.noecho()
            curses.cbreak()
            screen.refresh()

            words = cipher_tools.dictionary.expression(user_input, dictionary)
            wordstring = ''
            for word in words:
                wordstring = wordstring + ' ' +  word
            # clear line
            screen.addstr(2, 1, ' '*200)
            screen.refresh()

            screen.addstr(2, 1, wordstring)
            screen.refresh()

        if x == ord('8'):
            ciphertext = ''
            for i in cipher:
                ciphertext = ciphertext + i
            f = open(cipher_file, 'w+')
            f.write(ciphertext)
            f.close

if __name__=='__main__':
    try:
        # Initialize curses
        stdscr=curses.initscr()
        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        curses.noecho()
        curses.cbreak()

        # In keypad mode, escape sequences for special keys
        # (like the cursor keys) will be interpreted and
        # a special value like curses.KEY_LEFT will be returned
        stdscr.keypad(1)
        main(stdscr)                    # Enter the main loop
        # Set everything back to normal
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()                 # Terminate curses
    except:
        # In event of error, restore terminal to sane state.
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        traceback.print_exc()           # Print the exception
