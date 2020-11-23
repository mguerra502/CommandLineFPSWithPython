from numpy import array, zeros, pi, cos, sin, sqrt, arccos
import curses

from fps_utils import load_map, draw_map, place_player_in_map, handle_keystrokes

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

    # Place player in map
    # Player can't be place either in a wall nor outside the map
    player_location = place_player_in_map(map, w, h, None)
    if player_location is None:
        raise ValueError('Player can\'t be place in a wall')
    else:
        px, py = player_location[0], player_location[1]
    
    # Here update players location in map array
    map[int(px)][int(py)] = 2

    # Main loop
    while True:
        # Handle Player movement
        try:
            px, py = handle_keystrokes(console.getkey(), map, px, py)
        except TypeError:
            # This is to handle x key (exit)
            break
        except:
            # This handles no user input
            pass

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