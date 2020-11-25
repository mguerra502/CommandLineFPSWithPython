from numpy import zeros
from random import randint
import curses

def load_map(map_name: 'string'):
    """This method is use to load maps from a text file.
       Maps must be rectangular to avoid an exception

    Args:
        map_name (string): Name of the map to load

    Returns:
        2D_Numpy_Array: 2D Array representation of the map
        integer: Width of the map
        integer: Height of the map
    """
    map = ''
    with open(f'./maps/{map_name}.txt', 'r') as file:
        map = file.read().rstrip('\n') + '\n'

    h, w = map.count('\n'), len(map.split('\n')[0])
    map_array = zeros((w, h), dtype=int)
    i = 0
    j = 0
    for k in range(len(map)):
        if map[k] == '\n':
            if j == h:
                break

            i = 0
            j += 1
            continue

        if map[k] == "#":
            map_array[i, j] = 1
        else:
            map_array[i, j] = 0

        i += 1

    return map_array, w, h

def draw_map(console: 'Curses_Window', map: '2D_Numpy_Array', px: 'float', py: 'float', depth: 'integer'):
    """This method is used to draw the map, coming from the 2D_Numpy_Array in the console,

    Args:
        console (Curses_Window): A window defined using the curses library
        map (2D_Numpy_Array): 2D Array representation of the map
        px (float): Playe's x position
        py (float): Playe's y position
        depth (integer): Player's depth of vision
    """
    x_min = max(int(px) - depth, 0)
    x_max = min(int(px) + depth, len(map))
    y_min = max(int(py) - depth, 0)
    y_max = min(int(py) + depth, len(map[0]))
    for j in range(y_min, y_max):
        map_str = ''
        for i in range(x_min, x_max):
            if map[i, j] == 1:
                # Draw a wall
                map_str += u'\u2590'
            elif map[i, j] == 2:
                # Draw player
                map_str += u'\u25C8'
            else:
                # Draw empty space
                map_str += ' '

        if j != len(map[0]) - 1:
            map_str += '\n'

        console.addstr(j - y_min, 0, map_str, curses.color_pair(17))

def show_stats(console: 'Curses_Window', fps: 'integer', px: 'float', py: 'float', depth: 'integer'):
    """This method shows player's stats in the console

    Args:
        console (Curses_Window): A window defined using the curses library
        fps (integer): Frames per second
        px (float): Player's x position
        py (float): Player's y position
        depth (integer): Player's depth of vision
    """
    console.addstr(2*depth + 2, 0, f'Fps : {fps}', curses.color_pair(17))
    console.addstr(2*depth + 3, 0, f'x : {px}', curses.color_pair(17))
    console.addstr(2*depth + 4, 0, f'y : {py}', curses.color_pair(17))

def place_player_in_map(map: '2D_Numpy_Array', w: 'integer', h: 'integer', player_location: 'tuple(float, float) or None'):
    """This method place player in the map

    Args:
        map (2D_Numpy_Array): 2D Array representation of the map
        w (integer): Width of the map
        h (integer): Width of the map
        player_location (tuple(float, float) or None): Player's (x, y) position. If None, player is located randomly 

    Returns:
        tuple(float, float) or None: Player's (x, y) position. None when player is placed inside a wall
    """
    if player_location is None:
        px, py = float(randint(1, w - 2)), float(randint(1, h - 2))
        while True:
            if map[int(px), int(py)] != 1:
                return tuple((px, py))
            else:
                px, py = float(randint(1, w - 2)), float(randint(1, h - 2))
    else:
        px, py = float(player_location[0]), float(player_location[1])
        if map[int(px), int(py)] == 1:
            return None
        
        return tuple((px, py))

def handle_keystrokes(key_stroke: 'Key_Event', map: '2D_Numpy_Array', px: 'float', py: 'float'):
    """This Method handles keystrokes by the user

    Args:
        key_stroke (Key_Event): Char representing the keystroke by the user
        map (2D_Numpy_Array): 2D Array representation of the map
        px (float): Player's x position
        py (float): Player's y position

    Returns:
        px (float): Player's x position
        py (float): Player's y position
    """
    # Quit game
    if key_stroke == 'x':
        return

    # move forward
    if key_stroke == 'w':
        if map[int(px), int(py - 1)] != 1:
            map[int(px), int(py)] = 0
            py = py - 1
            map[int(px), int(py)] = 2
            return px, py

    # move backwards
    if key_stroke == 's':
        if map[int(px), int(py + 1)] != 1:
            map[int(px), int(py)] = 0
            py = py + 1
            map[int(px), int(py)] = 2
            return px, py

    # Rotate left
    # This one should be strafe left
    if key_stroke == 'a':
        if map[int(px - 1), int(py)] != 1:
            map[int(px), int(py)] = 0
            px = px - 1
            map[int(px), int(py)] = 2
            return px, py

    # Rotate right
    # This one should be strafe right
    if key_stroke == 'd':
        if map[int(px + 1), int(py)] != 1:
            map[int(px), int(py)] = 0
            px = px + 1
            map[int(px), int(py)] = 2
            return px, py

    # Finally, if not key matched then return same px, py
    return px, py