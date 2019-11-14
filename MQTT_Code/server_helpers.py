import numpy as np

def parse_from_string(s):
    return s.split(";")

def parse_from_strings(S):
    data = []
    for s in S:
        data.append(parse_from_string(s))
    return data

def find_max_full_grid(grid): 
    num_rows = len(grid)
    num_cols = len(grid[0]) 
  
    S = [[0 for k in range(num_cols)] for l in range(num_rows)] 

    for i in range(1, num_rows): 
        for j in range(1, num_cols): 
            if (grid[i][j] != 0): 
                S[i][j] = min(S[i][j-1], S[i-1][j], 
                            S[i-1][j-1]) + 1
            else: 
                S[i][j] = 0

    max_of_s = S[0][0] 
    max_i = 0
    max_j = 0
    for i in range(num_rows): 
        for j in range(num_cols): 
            if (max_of_s < S[i][j]): 
                max_of_s = S[i][j] 
                max_i = i 
                max_j = j 
  
    return max_i-max_of_s+1, max_i, max_j-max_of_s+1, max_j

def assign_lighting(grid, cycle):
    if cycle%2 == 0:
        return "Mode 2"
    return "Mode 1"

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
        if (col-1)!=0:
            name_grid[row-1][col-2] = neighbor
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