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

# localize maps clients to their position in the display grid.
def localize(data, grid, name_grid):
    row = int(data[0])
    col = int(data[1])
    name = data[2]
    neighbor = data[3]
    client_id = int(data[4])
    if row > grid.shape[0]:
        padding = np.zeros((row-grid.shape[0], grid.shape[1]))
        grid = np.concatenate((grid,padding), axis=0)
        
        padding = np.empty((row-name_grid.shape[0], name_grid.shape[1]), dtype=object)
        name_grid = np.concatenate((name_grid,padding), axis=0)
    if col > grid.shape[1]:
        padding = np.zeros((grid.shape[0], col-grid.shape[1]))
        grid = np.concatenate((grid,padding), axis=1)
        
        padding = np.empty((name_grid.shape[0], col-name_grid.shape[1]), dtype=object)
        name_grid = np.concatenate((name_grid,padding), axis=1)

    if grid[row-1][col-1] != 0:
        # unsuccessful if another client is already in this position
        return grid, name_grid, False
    elif (name_grid[row-1][col-1] != None) and (name_grid[row-1][col-1] != name):
        # unsuccessful if client's name doesn't match with name already in this position
        return grid, name_grid, False
    else:
        # set client to this position
        grid[row-1][col-1] = client_id
        name_grid[row-1][col-1] = name
        # set client's neighbor's name
        # if (col-1)!=0:
            # name_grid[row-1][col-2] = neighbor
    return grid, name_grid, True

def localize_all(data_array):
    grid = np.zeros((1,1))
    name_grid = np.empty((1,1), dtype=object)
    to_place = []
    for data in data_array:
        grid, name_grid, successful = localize(data,grid,name_grid)
        if not successful:
            to_place.append(data)
    # Do something with misplaced clients
    return grid, name_grid