import MotionTracker

IMU_data = "../IMU_Local/IMU_data.txt"
f = open(IMU_data,'r')

accXmin =  float(f.readline())
accYmin =  float(f.readline())
accZmin =  float(f.readline())
CFXmax =  float(f.readline())
CFYmax =  float(f.readline())

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

    if (ACCy > accYmin) and (ACCx < accXmin) and (ACCz < accZmin):         #Across
        return "A"
    elif (ACCz > accZmin) and (ACCx < accXmin) and (ACCy < accYmin):       #Left
        return "L"
    elif (ACCx > accXmin) and (ACCy < accYmin) and (ACCz < accZmin):      #Right
        return "R"
    else:
        return "X"
    