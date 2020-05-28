#!/usr/bin/python3
from typing import Tuple, List
import argparse
import curses
from web import get_all_definitions, get_page_source_for_word
from screen import Screen, Color, FontEffect

key_binding_entries = [
    ('<escape>', "exit the program"),
    ('q', 'exit the program'),
    ('<enter>', 'Move down one line'),
    ('<down arrow>', 'Move down one line'),
    ('<up arrow>', "Move up one line"),
    ('<page up>', "Move one screen up"),
    ('<page down>', "Move one screen down"),
    ('<home>', "Move to the beginning of the definitions"),
    ('<end>', "Move to the end of the definitions"),
]


def parse_args():
    ap = argparse.ArgumentParser(
        usage='usage: define.py (-h | -k | word [word ...]) [-t]',
        description="A program for defining words in the terminal. "
        "Definitions provided by https://www.wordnik.com/"
    )
    ap.add_argument('word', nargs='*', help='The word you want to define')
    ap.add_argument('-k', '--keybindings', action="store_true",
                    help='Show the keybindings used by the program and exit')
    ap.add_argument('-t', '--traceback', action="store_true", required=False,
                    help=('Instead of using the default message on '
                          'network failure (which is to display "No '
                          'defintions found") instead raise an '
                          'exception with the reason for the network'
                          ' failure'))
    ap.add_argument('-d', '--debug', help='add signal handlers for printing')
    options = ap.parse_args()
    if not options.keybindings and not options.word:
        ap.error("You must specify at least one word "
                 "to define or the -k flag or the -h flag")

    return options


def curses_begin() -> Screen:
    scr = Screen(curses.initscr(), curses.LINES, curses.COLS)
    curses.noecho()
    scr.win.keypad(1)
    curses.start_color()
    Color.init_color_pairs()
    return scr


def curses_create_subscrs(scr: Screen, right_start: int) -> Tuple[Screen, Screen]:
    pos_screen = scr.subwin(curses.LINES-2, right_start, 2, 4)
    defn_screen = scr.subwin(2, 4 + right_start)
    return (Screen(pos_screen, curses.LINES - 2, right_start),
            Screen(defn_screen, curses.LINES - 2, curses.COLS - right_start - 4))


def curses_mainloop(scr: Screen, pos_screen: Screen, defn_screen: Screen):
    while True:
        c = scr.getch()
        if c == 262:
            pos_screen.to_top()
            defn_screen.to_top()
        if c == 360:
            pos_screen.to_bottom()
            defn_screen.to_bottom()
        if c == 338:
            pos_screen.shift_down(pos_screen.lines)
            defn_screen.shift_down(defn_screen.lines)
        if c == 339:
            pos_screen.shift_up(pos_screen.lines)
            defn_screen.shift_up(defn_screen.lines)
        if c == 258 or c == 10:
            pos_screen.shift_down()
            defn_screen.shift_down()
        if c == 259:
            pos_screen.shift_up()
            defn_screen.shift_up()
        if c == ord('q') or c == 27:
            break
        pos_screen.render()
        defn_screen.render()


def show_word_defintion(
    defn: Tuple[str, str],
    pos_screen: Screen,
    defn_screen: Screen
) -> int:

    pos, definition = defn

    pos_lines = 0
    defn_lines = 0

    if pos == '<unknown>':
        pos_screen.set_style(FontEffect.UNDERLINE, Color.named('missing-info'))
    else:
        pos_screen.set_style(FontEffect.UNDERLINE, Color.named('part-of-speech'))

    pos_lines += pos_screen.add_str(pos)

    defn_screen.set_style(Color.named('definition'))
    defn_lines += defn_screen.add_str_wrapped(definition)

    pos_screen.render()
    defn_screen.render()

    return max([pos_lines, defn_lines])


def show_not_found(pos_screen: Screen, defn_screen: Screen):
    pos_screen.set_style(Color.named('error'))
    pos_screen.add_str("Error")

    defn_screen.set_style(Color.named('error'))
    defn_screen.add_str_wrapped(
        "Could not find a defition for the given word!")
    defn_screen.nl()
    defn_screen.set_style(FontEffect.BOLD, Color.named('error'))
    defn_screen.add_str_wrapped("Note that Wordnik is case-sensitive")

    pos_screen.render()
    defn_screen.render()


def show_banner(scr: Screen):
    scr.set_style(FontEffect.INVERT)
    scr.add_str('define2 - Command Line Tool - define a word'.center(scr.cols))


def show_requested_word(scr: Screen, word: str):
    scr.set_style(FontEffect.BOLD)
    scr.add_str(word)


def get_dict_entries(word: str, traceback: bool) -> List[Tuple[str, str]]:
    try:
        html = get_page_source_for_word(word)
        dict_entries = get_all_definitions(html)
    except ConnectionError:
        if traceback:
            raise
        dict_entries = []

    if word == 'potato':
        dict_entries = [('noun', '❤️')] + dict_entries
    return dict_entries


def fix_missing_pos(dict_entries):
    return [i if i[0] != '' else ('<unknown>', i[1]) for i in dict_entries]


def main():
    options = parse_args()
    if options.keybindings:
        word = 'Keybindings'
        dict_entries = key_binding_entries
    else:
        word = ' '.join(options.word)
        dict_entries = get_dict_entries(word, options.traceback)

    scr = curses_begin()
    show_banner(scr)
    show_requested_word(scr, word)
    scr.render()

    if dict_entries == []:
        rs = len('Error') + 2
        (pos_screen, defn_screen) = curses_create_subscrs(scr, right_start=rs)
        show_not_found(pos_screen, defn_screen)
    else:
        # this takes the (part-of-speech, defintion) tuples and replaces
        # empty strings in the part-of-speec with the string <unknown>
        dict_entries = fix_missing_pos(dict_entries)

        # this finds the tuple in dict_entries with the longest length
        # of the string at index 0, then it takes the 0th element of
        # that tuple, gets its length and adds 2
        rs = len(max(dict_entries, key=lambda x: len(x[0]))[0]) + 2
        (pos_screen, defn_screen) = curses_create_subscrs(scr, right_start=rs)
        lines = 0
        for entry in dict_entries:
            entry_lines = show_word_defintion(entry, pos_screen, defn_screen)
            pos_screen.nl(entry_lines + 1)
            defn_screen.nl(2)

            lines += entry_lines

    curses_mainloop(scr, pos_screen, defn_screen)
    curses.endwin()


if __name__ == "__main__":
    main()
