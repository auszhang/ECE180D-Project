import MotionTracker

def read():
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    
    ACCx = output[0]
    ACCy = output[1]
    ACCz = output[2]
    CFx = output[3]
    CFy = output[4]

    if ACCy < -1000:        #Right
        return "R"
    elif ACCx > 2500:         #Across
        return "A"
    elif ACCz > 2000:       #Left
        return "L"
    else:
        return "X"

def mega_read():
    num_A = 0
    num_L = 0
    num_R = 0
    cnt = 0
    while cnt < 4:
        out = read();
        if not out == "X":
            cnt += 1
        if (out == "A"):
            num_A += 1
        elif (out == "L"):
            num_L += 1
        elif (out == "R"):
            num_R += 1
    
    if num_A > num_L and num_A > num_R:
        return "A"
    elif num_L > num_A and num_L > num_R:
        return "L"
    else:
        return "R"

