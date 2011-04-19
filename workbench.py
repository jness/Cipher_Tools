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
        # Dont clear on our Dictionary searches
        if x != ord('4') and x != ord('>') and x != ord('<'):
            screen.erase()
        
        # BUILD MY MENU
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

        # REPLACE
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

        # UNDO
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

        # REDO
        if x == ord('3'):
            try:
                cipher = redo
            except UnboundLocalError:
                continue

        # DICTIONARY
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
            
            wordcount = 1
            maxcount = wordcount + 10

            for word in words:
                if wordcount < maxcount:
                    wordstring = wordstring + ' ' +  words[word]
                    wordcount += 1

            # Reset word count for Travel portion
            wordcount = 1

            # clear line
            screen.addstr(2, 1, ' '*200)
            screen.refresh()

            # If we have more words in the list give the option
            # to travel the list
            if len(words) > maxcount:
                screen.addstr(2, 1, wordstring + ' >')
            else:
                screen.addstr(2, 1, wordstring)

            screen.refresh()

        # TRAVEL THE DICTIONARY
        if x == ord('<'):
            
            # If newount isn't set we shouldn't run
            try:
                if newcount:
                    pass
            except UnboundLocalError:
                continue
           
            # Shouldn't shrink the number before 1
            if newcount - 10 < 1:
                continue
            else:
                newcount = newcount - 10


            count = 1

            maxcount = newcount + 10
            wordstring = ''

            for word in words:
                if wordcount < maxcount:
                    if count >= newcount and count <= maxcount:
                        wordstring = wordstring + ' ' +  words[word]
                    count += 1

            # clear line
            screen.addstr(2, 1, ' '*200)
            screen.refresh()

            if newcount == 1:
                screen.addstr(2, 1, wordstring + ' >')
            else:
                screen.addstr(2, 1, '<' + wordstring + ' >')

            screen.refresh()


        # TRAVEL THE DICTIONARY
        if x == ord('>'):

            # No need to run if our list is smaller than count
            if len(words) < maxcount:
                continue

            count = 1

            # If we increased befiore we need to bump the number
            try:
                newcount = newcount + 10
            except UnboundLocalError:
                newcount = wordcount + 10

            maxcount = newcount + 10
            wordstring = ''
            
            for word in words:
                if wordcount < maxcount:
                    if count >= newcount and count <= maxcount: 
                        wordstring = wordstring + ' ' +  words[word]
                    count += 1

            # clear line
            screen.addstr(2, 1, ' '*200)
            screen.refresh()

            # If we have more words in the list give the option
            # to travel the list
            if len(words) > maxcount:
                screen.addstr(2, 1, '<' + wordstring + ' >')
            else:
                screen.addstr(2, 1, '<' + wordstring)

            screen.refresh()

        # SAVE
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
