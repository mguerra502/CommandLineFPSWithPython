from numpy import array, zeros, pi, cos, sin, sqrt, arccos
from time import time
import curses

from fps_utils import load_map, draw_map, place_player_in_map, handle_keystrokes, show_stats, render_world

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
    map, map_width, map_depth = load_map('map2')

    # Place player in map
    # Player can't be place either in a wall nor outside the map
    player_location = place_player_in_map(map, map_width, map_depth, None)
    if player_location is None:
        raise ValueError('Player can\'t be place in a wall')
    else:
        px, py = player_location[0], player_location[1]
    
    # Here update players location in map array
    map[int(px)][int(py)] = 2

    # Screen properties
    world_screen_width = 180
    world_screen_height = 40

    # Vision depth
    # TODO: This is a value that could change
    vision_depth = 8

    pa = pi # Player's angle
    field_of_vision = pi/2.0 # field of view
    speed = 5.0 # speed of movement

    # Initialise elapsed time variables
    time_previous_frame = time()
    time_current_frame = time()

    # Main loop
    while True:
        # Calculate the difference in time between frames
        time_current_frame = time()
        timeframe = time_current_frame - time_previous_frame
        time_previous_frame = time_current_frame
        # Handle Player movement
        try:
            px, py, pa = handle_keystrokes(console.getkey(), map, px, py, pa, speed, timeframe)
        except TypeError:
            # This is to handle x key (exit)
            break
        except:
            # This handles no user input
            pass

        # Clear console
        console.erase()

        # Draw map on console
        draw_map(console, map, px, py, vision_depth)
        show_stats(console, int(1/timeframe), px, py, pa, vision_depth)
        render_world(console, map, world_screen_width, world_screen_height, px, py, pa, field_of_vision, vision_depth, map_width, map_depth)
        
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