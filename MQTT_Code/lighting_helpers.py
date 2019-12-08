import numpy as np

def one_color_conv(light_mat, color_char):
    #use for 2D matrices
    out_mat = [["0","0","0"],["0","0","0"],["0","0","0"]]
    for i in range(3):
        for j in range(3):
            l = light_mat[i][j]
            if l == 1:
                out_mat[i][j] = color_char
    return out_mat

# Lighting scheme for "U"
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

U_ASGN_blue = []
for i in U_ASGN:
    U_ASGN_blue.append(one_color_conv(i, "b"))


# Lighting scheme for "C"
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

C_ASGN_gold = []
for i in C_ASGN:
    C_ASGN_gold.append(one_color_conv(i, "d"))

# Lighting scheme for "L"
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

L_ASGN_blue = []
for i in L_ASGN:
    L_ASGN_blue.append(one_color_conv(i, "b"))

# Lighting scheme for "A"
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

A_ASGN_gold = []
for i in A_ASGN:
    A_ASGN_gold.append(one_color_conv(i, "d"))

ALL_ON = [[1,1,1],
          [1,0,1],
          [1,1,1]]

ALL_OFF = [[0,0,0],
          [0,0,0],
          [0,0,0]]

ONE_ON = [[1,0,0],
          [0,0,0],
          [0,0,1]]

#THREE CAP STUFF!!!!!!!!!!!
#BOTTOM RIGHT MISSING
cap_UL = [[1,1,1],
          [1,0,0],
          [1,0,1]]
cap_DL = [[1,0,1],
          [1,0,1],
          [1,1,1]]
cap_UR = [[1,1,1],
          [0,0,1],
          [1,1,1]]
BR_missing = []
BR_missing.append(cap_UL)
BR_missing.append(cap_UR)
BR_missing.append(cap_DL)

cap_UL = [[1,2,1],
          [2,0,0],
          [1,0,1]]
cap_DL = [[2,0,2],
          [1,0,1],
          [2,1,2]]
cap_UR = [[2,1,2],
          [0,0,1],
          [2,1,2]]
BR_missing_cycle1 = []
BR_missing_cycle1.append(cap_UL)
BR_missing_cycle1.append(cap_UR)
BR_missing_cycle1.append(cap_DL)

cap_UL = [[2,1,2],
          [1,0,0],
          [2,0,2]]
cap_DL = [[1,0,1],
          [2,0,2],
          [1,2,1]]
cap_UR = [[1,2,1],
          [0,0,2],
          [1,2,1]]
BR_missing_cycle2 = []
BR_missing_cycle2.append(cap_UL)
BR_missing_cycle2.append(cap_UR)
BR_missing_cycle2.append(cap_DL)

#BOTTOM LEFT MISSING
cap_UL = [[1,1,1],
          [1,0,0],
          [1,1,1]]
cap_DR = [[1,0,1],
          [1,0,1],
          [1,1,1]]
cap_UR = [[1,1,1],
          [0,0,1],
          [1,0,1]]
BL_missing = []
BL_missing.append(cap_UL)
BL_missing.append(cap_UR)
BL_missing.append(cap_DR)
cap_UL = [[1,2,1],
          [2,0,0],
          [1,2,1]]
cap_DR = [[1,0,1],
          [2,0,2],
          [1,2,1]]
cap_UR = [[2,1,2],
          [0,0,1],
          [2,0,2]]
BL_missing_cycle1 = []
BL_missing_cycle1.append(cap_UL)
BL_missing_cycle1.append(cap_UR)
BL_missing_cycle1.append(cap_DR)

cap_UL = [[2,1,2],
          [1,0,0],
          [2,1,2]]
cap_DR = [[2,0,2],
          [1,0,1],
          [2,1,2]]
cap_UR = [[1,2,1],
          [0,0,2],
          [1,0,1]]
BL_missing_cycle2 = []
BL_missing_cycle2.append(cap_UL)
BL_missing_cycle2.append(cap_UR)
BL_missing_cycle2.append(cap_DR)

#UPPER RIGHT MISSING
cap_UL = [[1,1,1],
          [1,0,1],
          [1,0,1]]
cap_DL = [[1,0,1],
          [1,0,0],
          [1,1,1]]
cap_DR = [[1,1,1],
          [0,0,1],
          [1,1,1]]
UR_missing= []
UR_missing.append(cap_UL)
UR_missing.append(cap_DL)
UR_missing.append(cap_DR)

cap_UL = [[1,2,1],
          [2,0,2],
          [1,0,1]]
cap_DL = [[2,0,2],
          [1,0,0],
          [2,1,2]]
cap_DR = [[1,2,1],
          [0,0,2],
          [1,2,1]]
UR_missing_cycle1= []
UR_missing_cycle1.append(cap_UL)
UR_missing_cycle1.append(cap_DL)
UR_missing_cycle1.append(cap_DR)

cap_UL = [[2,1,2],
          [1,0,1],
          [2,0,2]]
cap_DL = [[1,0,1],
          [2,0,0],
          [1,2,1]]
cap_DR = [[2,1,2],
          [0,0,1],
          [2,1,2]]
UR_missing_cycle2= []
UR_missing_cycle2.append(cap_UL)
UR_missing_cycle2.append(cap_DL)
UR_missing_cycle2.append(cap_DR)

#UPPER LEFT MISSING
cap_UR = [[1,1,1],
          [1,0,1],
          [1,0,1]]
cap_DL = [[1,1,1],
          [1,0,0],
          [1,1,1]]
cap_DR = [[1,0,1],
          [0,0,1],
          [1,1,1]]
UL_missing= []
UL_missing.append(cap_UR)
UL_missing.append(cap_DL)
UL_missing.append(cap_DR)

cap_UR = [[1,2,1],
          [2,0,2],
          [1,0,1]]
cap_DL = [[1,2,1],
          [2,0,0],
          [1,2,1]]
cap_DR = [[2,0,2],
          [0,0,1],
          [2,1,2]]
UL_missing_cycle2= []
UL_missing_cycle2.append(cap_UR)
UL_missing_cycle2.append(cap_DL)
UL_missing_cycle2.append(cap_DR)

cap_UR = [[2,1,2],
          [1,0,1],
          [2,0,2]]
cap_DL = [[2,1,2],
          [1,0,0],
          [2,1,2]]
cap_DR = [[1,0,1],
          [0,0,2],
          [1,2,1]]

UL_missing_cycle1= []
UL_missing_cycle1.append(cap_UR)
UL_missing_cycle1.append(cap_DL)
UL_missing_cycle1.append(cap_DR)

def tell_lighting(client_id, lighting): 
    #currently not accounting for color assignments
    msg = str(client_id) + str(lighting[2][1]) + str(lighting[2][2]) + str(lighting[1][2])\
    + str(lighting[0][2]) + str(lighting[0][1])+str(lighting[0][0])\
    + str(lighting[1][0]) +str(lighting[2][0])+"#"
    return msg
def two_color_conv(light_mat, c1, c2):
    #use for 2D matrices
    print('at two_color_conv')
    print(light_mat)
    out_mat = [["0","0","0"],["0","0","0"],["0","0","0"]]
    for i in range(3):
        for j in range(3):
            l = light_mat[i][j]
            if l==1:
                print("changed color1")
                out_mat[i][j] = c1
            elif l==2:
                print("changed color2")
                out_mat[i][j] = c2
    return out_mat

def UCLA_light_scheme(grid, cycle):
    msg = ""
    if cycle%4 == 0:
        # U
        msg += tell_lighting(grid[0][0],U_ASGN_blue[0])
        msg += tell_lighting(grid[0][1],U_ASGN_blue[1])
        msg += tell_lighting(grid[1][0],U_ASGN_blue[2])
        msg += tell_lighting(grid[1][1],U_ASGN_blue[3])
    elif cycle%4 == 1:
        # C
        msg += tell_lighting(grid[0][0],C_ASGN_gold[0])
        msg += tell_lighting(grid[0][1],C_ASGN_gold[1])
        msg += tell_lighting(grid[1][0],C_ASGN_gold[2])
        msg += tell_lighting(grid[1][1],C_ASGN_gold[3])
    elif cycle%4 == 2:
        # L
        msg += tell_lighting(grid[0][0],L_ASGN_blue[0])
        msg += tell_lighting(grid[0][1],L_ASGN_blue[1])
        msg += tell_lighting(grid[1][0],L_ASGN_blue[2])
        msg += tell_lighting(grid[1][1],L_ASGN_blue[3])
    else:
        # A
        msg += tell_lighting(grid[0][0],A_ASGN_gold[0])
        msg += tell_lighting(grid[0][1],A_ASGN_gold[1])
        msg += tell_lighting(grid[1][0],A_ASGN_gold[2])
        msg += tell_lighting(grid[1][1],A_ASGN_gold[3])
    return msg

def three_connected_basic(grid,cycle):
    msg = ""
    if (grid[0][0]==0): #top left is empty
        msg += tell_lighting(grid[0][1], UL_missing[0])
        msg += tell_lighting(grid[1][0], UL_missing[1])
        msg += tell_lighting(grid[1][1], UL_missing[2])

    elif (grid[0][1]==0):
        msg += tell_lighting(grid[0][0], UR_missing[0])
        msg += tell_lighting(grid[1][0], UR_missing[1])
        msg += tell_lighting(grid[1][1], UR_missing[2])

    elif (grid[1][0]==0):
        msg += tell_lighting(grid[0][0], BL_missing[0])
        msg += tell_lighting(grid[0][1], BL_missing[1])
        msg += tell_lighting(grid[1][1], BL_missing[2])

    elif (grid[1][1]==0):
        msg += tell_lighting(grid[0][0], BR_missing[0])
        msg += tell_lighting(grid[0][1], BR_missing[1])
        msg += tell_lighting(grid[1][0], BR_missing[2])

    else:
        print("MISSING PERSON NEVER FOUND")
    return msg

def three_connected_colors(grid,cycle,color1, color2):
    msg=""
    print(cycle)
    if (grid[0][0]==0):
        if (cycle % 2 == 0):   
            mod = UL_missing_cycle1
        else:
            mod = UL_missing_cycle2 
        msg += tell_lighting(grid[0][1], two_color_conv(mod[0],color1,color2))
        msg += tell_lighting(grid[1][0], two_color_conv(mod[1],color1,color2))
        msg += tell_lighting(grid[1][1], two_color_conv(mod[2],color1,color2))

    elif (grid[0][1]==0):
        if (cycle % 2 == 0):   
            mod = UR_missing_cycle1
        else:
            mod = UR_missing_cycle2   
        msg += tell_lighting(grid[0][0], two_color_conv(mod[0],color1,color2))
        msg += tell_lighting(grid[1][0], two_color_conv(mod[1],color1,color2))
        msg += tell_lighting(grid[1][1], two_color_conv(mod[2],color1,color2))
    elif (grid[1][0]==0):
        if (cycle % 2 == 0):   
            mod = BL_missing_cycle1
        else:
            mod = BL_missing_cycle2 
        msg += tell_lighting(grid[0][0], two_color_conv(mod[0],color1,color2))
        msg += tell_lighting(grid[0][1], two_color_conv(mod[1],color1,color2))
        msg += tell_lighting(grid[1][1], two_color_conv(mod[2],color1,color2))    
    elif (grid[1][1]==0):
        if (cycle % 2 == 0):   
            mod = BR_missing_cycle1
        else:
            mod = BR_missing_cycle2    
        msg += tell_lighting(grid[0][0], two_color_conv(mod[0],color1,color2))
        msg += tell_lighting(grid[0][1], two_color_conv(mod[1],color1,color2))
        msg += tell_lighting(grid[1][0], two_color_conv(mod[2],color1,color2))        

    return msg

def steady_on(grid, cycle):
    msg = ""
    for row in grid:
        for client_id in row:
            # msg += tell_lighting(client_id, ALL_ON) 
            msg += tell_lighting(client_id, ONE_ON)
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
    return msg
        
def flash_fast(grid, cycle):
    msg = ""
    if cycle%2==0:
        msg = steady_on(grid, cycle)
    else:
        msg = steady_off(grid, cycle)
    return msg