import MotionTracker

IMU_data = "../IMU_Local/IMU_data.txt"
f = open(IMU_data,'r')

#some distance = float(f.readline())

accXmin =  float(f.readline())
accYmin =  float(f.readline())
accZmin =  float(f.readline())
CFXmax =  float(f.readline())
CFYmax =  float(f.readline())

def read(): #Xx, Xy, Xz

    #read initial time
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    #read ending time

    ACCx = output[0]
    ACCy = output[1]
    ACCz = output[2]
    CFx = output[3]
    CFy = output[4]

    #dt_squared = (ending time - initial time)**2
    #Xx = ACCx * dt_squared
    #Xy = ACCy * dt_squared
    #Xz = ACCz * dt_squared

    #if (Xx > some distance) and (Xy < some distance) and (Xz < some distance):
    if (ACCy > accYmin) and (ACCx < accXmin) and (ACCz < accZmin):         #Across
        return "A"
    #elif (Xx < some distance) and (Xy > some distance) and (Xz < some distance):
    elif (ACCz > accZmin) and (ACCx < accXmin) and (ACCy < accYmin):       #Left
        return "L"
    #elif (Xx < some distance) and (Xy < some distance) and (Xz > some distance):
    elif (ACCx > accXmin) and (ACCy < accYmin) and (ACCz < accZmin):      #Right
        return "R"
    else:
        return "X"
    