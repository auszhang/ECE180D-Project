# Lighting scheme for 'U'
cap_UL = [[1,0,0],
          [1,0,0],
          [1,0,0]]
cap_UR = [[0,0,1],
          [0,0,1],
          [0,0,1]]
cap_DL = [[1,0,0],
          [1,0,0],
          [1,1,1]]
cap_DR = [[0,0,1],
          [0,0,1],
          [1,1,1]]
U_ASGN = []
U_ASGN.append(cap_UL)
U_ASGN.append(cap_UR)
U_ASGN.append(cap_DL)
U_ASGN.append(cap_DR)

# Lighting scheme for 'C'
cap_UL = [[1,1,1],
          [1,0,0],
          [1,0,0]]
cap_UR = [[1,1,1],
          [0,0,0],
          [0,0,0]]
cap_DL = [[1,0,0],
          [1,0,0],
          [1,1,1]]
cap_DR = [[0,0,0],
          [0,0,0],
          [1,1,1]]
C_ASGN = []
C_ASGN.append(cap_UL)
C_ASGN.append(cap_UR)
C_ASGN.append(cap_DL)
C_ASGN.append(cap_DR)

# Lighting scheme for 'L'
cap_UL = [[1,0,0],
          [1,0,0],
          [1,0,0]]
cap_UR = [[0,0,0],
          [0,0,0],
          [0,0,0]]
cap_DL = [[1,0,0],
          [1,0,0],
          [1,1,1]]
cap_DR = [[0,0,0],
          [0,0,0],
          [1,1,1]]
L_ASGN = []
L_ASGN.append(cap_UL)
L_ASGN.append(cap_UR)
L_ASGN.append(cap_DL)
L_ASGN.append(cap_DR)

# Lighting scheme for 'A'
cap_UL = [[1,1,1],
          [1,0,0],
          [1,1,1]]
cap_UR = [[1,1,1],
          [0,0,1],
          [1,1,1]]
cap_DL = [[1,0,0],
          [1,0,0],
          [1,0,0]]
cap_DR = [[0,0,1],
          [0,0,1],
          [0,0,1]]
A_ASGN = []
A_ASGN.append(cap_UL)
A_ASGN.append(cap_UR)
A_ASGN.append(cap_DL)
A_ASGN.append(cap_DR)

ALL_ON = [[1,1,1],
          [1,0,1],
          [1,1,1]]

ALL_OFF = [[0,0,0],
          [0,0,0],
          [0,0,0]]

def tell_lighting(client_id, lighting): 
    #currently not accounting for color assignments
    msg = str(client_id) + str(lighting[2][1]) + str(lighting[2][2]) + str(lighting[1][2])\
    + str(lighting[0][2]) + str(lighting[0][1])+str(lighting[0][0])\
    + str(lighting[1][0]) +str(lighting[2][0])+" "
    return msg

def UCLA_light_scheme(grid, cycle):
    msg = ""
    if cycle%4 == 0:
        # U
        msg += tell_lighting(grid[0][0],U_ASGN[0])
        msg += tell_lighting(grid[0][1],U_ASGN[1])
        msg += tell_lighting(grid[1][0],U_ASGN[2])
        msg += tell_lighting(grid[1][1],U_ASGN[3])
    elif cycle%4 == 1:
        # C
        msg += tell_lighting(grid[0][0],C_ASGN[0])
        msg += tell_lighting(grid[0][1],C_ASGN[1])
        msg += tell_lighting(grid[1][0],C_ASGN[2])
        msg += tell_lighting(grid[1][1],C_ASGN[3])
    elif cycle%4 == 2:
        # L
        msg += tell_lighting(grid[0][0],L_ASGN[0])
        msg += tell_lighting(grid[0][1],L_ASGN[1])
        msg += tell_lighting(grid[1][0],L_ASGN[2])
        msg += tell_lighting(grid[1][1],L_ASGN[3])
    else:
        # A
        msg += tell_lighting(grid[0][0],A_ASGN[0])
        msg += tell_lighting(grid[0][1],A_ASGN[1])
        msg += tell_lighting(grid[1][0],A_ASGN[2])
        msg += tell_lighting(grid[1][1],A_ASGN[3])
    return msg

def steady_on(grid, cycle):
    msg = ""
    for row in grid:
        for client_id in row:
            msg += tell_lighting(client_id, ALL_ON)
    return msg

def steady_off(grid, cycle):
    msg = ""
    for row in grid:
        for client_id in row:
            msg += tell_lighting(client_id, ALL_OFF)
    return msg

def flash_slow(grid, cycle):
    msg = ""
    if cycle%3==0:
        msg = steady_on(grid, cycle)
    else:
        msg = steady_off(grid, cycle)
        
def flash_fast(grid, cycle):
    msg = ""
    if cycle%2==0:
        msg = steady_on(grid, cycle)
    else:
        msg = steady_off(grid, cycle)
        
    