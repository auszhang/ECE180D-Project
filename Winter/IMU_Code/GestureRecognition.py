import MotionTracker

def read():
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    
    ACCx = output[0]
    ACCy = output[1]
    ACCz = output[2]
    CFx = output[3]
    CFy = output[4]

    if ACCx > 2500:         #Across
        return "A"
    elif ACCz > 2000:       #Left
        return "L"
    elif ACCy < -1000:      #Right
        return "R"
    else:
        return "X"
    