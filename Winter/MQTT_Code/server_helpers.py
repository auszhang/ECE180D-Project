import numpy as np

def parse_from_string(s):
    return s.split(";")

def parse_from_strings(S):
    data = []
    # Reverse so that data received later is first.
    S = reversed(S)
    for s in S:
        data.append(parse_from_string(s))
    return data

def parse_from_strings_hash(H):
    data = []
    for key in H:
        data.append(parse_from_string(H[key]))
    return data

def pos_to_row_col(pos):
    if pos==1:
        return 0, 0
    elif pos==2:
        return 0, 1
    elif pos==3:
        return 1, 0
    elif pos==4:
        return 1, 1
    return -1, -1

# localize maps clients to their position in the display grid.
def localize(data, grid, name_grid):
    # Parse data
    pos = int(data[0]) # pos is an integer 1, 2, 3, 4
    name = data[1]
    client_id = data[2]
    row, col = pos_to_row_col(pos)
    
    # Check if invalid position
    if row == -1 or col == -1:
        return grid, name_grid, False
    
    if grid[row][col] != "":
        # unsuccessful if another client is already in this position
        return grid, name_grid, False
    elif (name_grid[row][col] != None) and (name_grid[row][col] != name):
        # unsuccessful if client's name doesn't match with name already in this position
        return grid, name_grid, False
    else:
        # set client to this position
        grid[row][col] = client_id
        name_grid[row][col] = name
    return grid, name_grid, True

# Returns grid (client id to position) and name_grid (client name to position)
def localize_all(data_array):
    # Initialize 2x2 grid
    grid = [["",""],["",""]]
    name_grid = np.empty((2,2), dtype=object)
    to_place = []
    for data in data_array:
        grid, name_grid, successful = localize(data,grid,name_grid)
        if not successful:
            to_place.append(data)
    # Do something with misplaced clients
    return grid, name_grid

# Return row and col number of the client, given client id.
def find_client_in_grid(client_id, grid):
    if grid[0][0] == client_id:
        return 0, 0
    elif grid[0][1] == client_id:
        return 0, 1
    elif grid[1][0] == client_id:
        return 1, 0
    elif grid[1][1] == client_id:
        return 1, 1
    return -1, -1

# Given 0 return 1. Else return 0.
def flip_num(num):
    if num == 0:
        return 1
    else:
        return 0

# Given starting position + direction, return new position
def get_pos_from_dir(row, col, direction):
    new_row = -1
    new_col = -1
    if direction == "RIGHT":
        new_row = flip_num(col)
        new_col = row
    elif direction == "LEFT":
        new_row = col
        new_col = flip_num(row)
    elif direction == "ACROSS":
        new_row = flip_num(row)
        new_col = flip_num(col)
    return new_row, new_col

# Given client statement, game grid, and current potato position
# Return new position of potato and whether move is valid
def parse_pass(statement, game_grid, potato_row, potato_col):
    data = parse_from_string(statement)
    client_id = data[0]
    direction = data[2]
    c_row, c_col = find_client_in_grid(client_id, game_grid)
    
    # Invalid if client is not in the game
    if c_row == -1 or c_col == -1:
        return -1, -1, False
    
    # Invalid if client trying to pass does not have potato
    if c_row != potato_row or c_col != potato_col:
        return -1, -1, False
    
    # Get position of receiver
    new_p_row, new_p_col = get_pos_from_dir(c_row, c_col, direction)
    
    # Invalid if invalid positions
    if new_p_row == -1 or new_p_col == -1:
        return -1, -1, False
    
    # Invalid if no client at receiving position
    if game_grid[new_p_row][new_p_col] == "":
        return -1, -1, False
    
    # Invalid if trying to pass to self
    if new_p_row == potato_row and new_p_col == potato_col:
        return -1, -1, False
    
    return new_p_row, new_p_col, True

# Given a client id and the game grid, remove player from the game.
def remove_player(client_id,game_grid):
    for i in range(2):
        for j in range(2):
            if game_grid[i][j] == client_id:
                game_grid[i][j] = ""
                return game_grid
    return game_grid
    