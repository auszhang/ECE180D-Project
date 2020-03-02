import MotionTracker

while(1):
    outputarray = MotionTracker.readIMU(MotionTracker.IMU)
    print(str(outputarray[0]) + ", " + str(outputarray[1]) + ", " + str(outputarray[2]))