from numpy import array, zeros, pi, cos, sin, sqrt, arccos
import curses

from fps_utils import load_map, draw_map

def curses_properties():
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.resizeterm(200, 200)
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

def main(console: 'Curses_Window'):
    """This is the main method of the 'fps' in the command line

    Args:
        console (Curses_Window): A window defined using the curses library
    """
    # Load map
    map, w, h = load_map('map1')

    # Main loop
    while True:
        # Clear console
        console.erase()

        # Draw map on console
        draw_map(console, map)
        
        # Refresh console
        console.refresh()

    

if __name__ == '__main__':
    # Define console
    console = curses.initscr()
    console.nodelay(True)
    console.clear()
    console.refresh()
    console.scrollok(1)
    # Set curses properties
    curses_properties()
    try:
        main(console)
    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()