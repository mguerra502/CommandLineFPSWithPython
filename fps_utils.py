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

def draw_map(console: 'Curses_Window', map: '2D_Numpy_Array'):
    """This method is used to draw the map, coming from the 2D_Numpy_Array in the console,

    Args:
        console (Curses_Window): A window defined using the curses library
        map (2D_Numpy_Array): 2D Array representation of the map
    """
    for j in range(len(map[0])):
        map_str = ''
        for i in range(len(map)):
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

        console.addstr(j, 0, map_str, curses.color_pair(17))

def place_player_in_map(map: '2D_Numpy_Array', w: 'integer', h: 'integer', player_location: 'tuple(integer, integer) or None'):
    """This method place player in the map

    Args:
        map (2D_Numpy_Array): 2D Array representation of the map
        w (integer): Width of the map
        h (integer): Width of the map
        player_location (tuple or None): Player location. If None, player is located randomly 

    Returns:
        tuple(integer, integer): Player Location
    """
    if player_location is None:
        px, py = randint(1, w - 2), randint(1, h - 2)
        while True:
            if map[px, py] != 1:
                break
            else:
                px, py = randint(1, w - 2), randint(1, h - 2)

        return tuple((px, py))
    else:
        px, py = player_location[0], player_location[1]
        if map[px, py] == 1:
            return None
        
        return tuple((px, py))