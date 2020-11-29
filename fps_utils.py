from numpy import zeros, cos, sin, pi, arccos, sqrt
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

def show_stats(console: 'Curses_Window', fps: 'integer', px: 'float', py: 'float', pa: 'float', depth: 'integer'):
    """This method shows player's stats in the console

    Args:
        console (Curses_Window): A window defined using the curses library
        fps (integer): Frames per second
        px (float): Player's x position
        py (float): Player's y position
        pa (float): Player's y angle
        depth (integer): Player's depth of vision
    """
    console.addstr(2*depth + 2, 0, f'Fps : {fps}', curses.color_pair(17))
    console.addstr(2*depth + 3, 0, f' x  : {px}', curses.color_pair(17))
    console.addstr(2*depth + 4, 0, f' y  : {py}', curses.color_pair(17))
    console.addstr(2*depth + 5, 0, f' y  : {int(pa*180/pi)%360}', curses.color_pair(17))

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
        px, py = float(randint(1, w - 2)) + 0.1, float(randint(1, h - 2)) + 0.1
        while True:
            if map[int(px), int(py)] != 1:
                return tuple((px, py))
            else:
                px, py = float(randint(1, w - 2)) + 0.1, float(randint(1, h - 2)) + 0.1
    else:
        px, py = float(player_location[0]), float(player_location[1])
        if map[int(px), int(py)] == 1:
            return None
        
        return tuple((px, py))

def handle_keystrokes(key_stroke: 'Key_Event', map: '2D_Numpy_Array', px: 'float', py: 'float', pa: 'float', speed: 'float', frame_time: 'float'):
    """This Method handles keystrokes by the user

    Args:
        key_stroke (Key_Event): Char representing the keystroke by the user
        map (2D_Numpy_Array): 2D Array representation of the map
        px (float): Player's x position
        py (float): Player's y position
        pa (float): Player's angle
        speed (float): Player's speed
        frame_time (float): Time passed between frames
    Returns:
        px (float): Player's x position
        py (float): Player's y position
        pa (float): Player's angle
    """
    # Quit game
    if key_stroke == 'x':
        return

    # move forward
    if key_stroke == 'w':
        if map[int(px + cos(pa) * speed * frame_time), int(py + sin(pa) * speed * frame_time)] != 1:
            map[int(px), int(py)] = 0
            px += cos(pa) * speed * frame_time
            py += sin(pa) * speed * frame_time
            map[int(px), int(py)] = 2

    # move backwards
    if key_stroke == 's':
        if map[int(px - cos(pa) * speed * frame_time), int(py - sin(pa) * speed * frame_time)] != 1:
            map[int(px), int(py)] = 0
            px -= cos(pa) * speed * frame_time
            py -= sin(pa) * speed * frame_time
            map[int(px), int(py)] = 2

    # Rotate left
    # This one should be strafe left
    if key_stroke == 'a':
        pa -= (speed * 0.75)*frame_time

    # Rotate right
    # This one should be strafe right
    if key_stroke == 'd':
        pa += (speed * 0.75)*frame_time

    # Finally, if not key matched then return same px, py
    return px, py, pa

def render_world(
    console: 'Curses_Window',
    map: '2D_Numpy_Array',
    world_screen_width: 'integer',
    world_screen_height: 'integer',
    px: 'float',
    py: 'float',
    pa: 'float',
    field_of_vision: 'float',
    depth: 'integer',
    map_width: 'integer',
    map_depth: 'integer'
):
    # Start parsing columns of the screen
    for i in range(world_screen_width):
        # Get angle of ray for every column in screen
        ray_angle = (pa - field_of_vision/2.0) + (float(i)/float(world_screen_width))*field_of_vision

        # Find distance to closest wall
        step_size = 0.1
        distance_to_wall = 0.0

        # Unit vector for ray in space
        eye_x = cos(ray_angle)
        eye_y = sin(ray_angle)

        # Increment ray from player, along ray angle until it hits a wall
        hit_wall_boundary = False
        while True:
            # Increase distance to wall
            distance_to_wall += step_size
            ray_x = int(px + eye_x*distance_to_wall)
            ray_y = int(py + eye_y*distance_to_wall)
            # Check if ray is out of bounds
            if (ray_x < 0 or ray_x >= map_width or ray_y < 0 or ray_y >= map_depth):
                # Ray is out of bounds, set distance_to_wall to depth
                distance_to_wall = depth

                break
            else:
                # Ray is inbound, check if hits a wall
                if map[int(ray_x), int(ray_y)] == 1:
                    # Here we need to highlight block boundaries before break statement
                    p = []
                    for tx in range(2):
                        for ty in range(2):
                            # Angle of corner to eye
                            vx = float(ray_x) + float(tx) - px
                            vy = float(ray_y) + float(ty) - py
                            d = sqrt(vx**2 + vy**2)
                            if d == 0.0:
                                d = 0.0000000001
                            dot = (eye_x*vx/d) + (eye_y*vy/d)
                            p.append(tuple((d, dot)))

                    # Sort pairs from closest to farthest
                    p.sort(key=lambda tup: tup[0])

                    # First 2/3 are the closest. Never 4 at the same time
                    bound = 0.01
                    if arccos(p[0][1]) < bound:
                        hit_wall_boundary = True
                    
                    if arccos(p[1][1]) < bound:
                        hit_wall_boundary = True

                    if arccos(p[2][1]) < bound:
                        hit_wall_boundary = True

                    break

        # Calculate distance to ceiling a floor
        ceiling_dist = world_screen_height/2.0 - world_screen_height/distance_to_wall
        floor_dist = float(world_screen_height) - ceiling_dist

        # Now, start parsing through every row of the screen
        for j in range(world_screen_height):
            if j <= ceiling_dist:
                console.addstr(j, 2*depth + 1 + i, ' ', curses.color_pair(233))
            elif j > ceiling_dist and j <= floor_dist:
                char_value = u'\u2593'
                if hit_wall_boundary:
                    wall_shade = 233
                    char_value = ' '
                else:
                    wall_shade = int((-22/depth)*distance_to_wall + 254)
                    if wall_shade > 254:
                        wall_shade = 254
                    if wall_shade <= 233:
                        wall_shade = 233
                        char_value = ' '

                console.addstr(j, 2*depth + 1 + i, char_value, curses.color_pair(wall_shade))
            else:
                floor_dist = 1.0 - ((float(j) - world_screen_height/2.0)/(world_screen_height/2.0))
                floor_shade = int(-22*floor_dist + 254)
                if floor_shade > 254:
                    floor_shade = 254
                if floor_shade < 233:
                    floor_shade = 233

                console.addstr(j, 2*depth + 1 + i, u'\u2591', curses.color_pair(floor_shade))
                