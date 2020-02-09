import MotionTracker

while 1:
    output = MotionTracker.readIMU(MotionTracker.IMU)
    ACCx = output[0]
    ACCy = output[1]
    ACCz = output[2]
    CFx = output[3]
    CFy = output[4]

    if ACCx > 2500:
        print("Across")
    elif ACCz > 2000:
        print("Right")
    elif ACCy < -1000:
        print("Left")