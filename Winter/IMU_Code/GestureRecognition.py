import MotionTracker
import RPi.GPIO as GPIO
import time

IMU_data = "../IMU_Local/IMU_data.txt"

accYmin =  0
accXmin =  0
accXmax =  0

def getData():
    global accYmin
    global accXmin
    global accXmax
    
    f = open(IMU_data,'r')

    accYmin =  float(f.readline())
    accXmin =  float(f.readline())
    accXmax =  float(f.readline())

def iliketrains():
    global accYmin
    global accXmin
    global accXmax

    minY = 0
    maxX = 0
    minX = 0

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.OUT)

    print("Across")
    GPIO.output(12, 1)
    time.sleep(0.2)
    GPIO.output(12, 0)
    for i in range(200):
        output = MotionTracker.readIMU(MotionTracker.IMU)
        if(output[1] < minY):
            minY = output[1]
    accYmin = minY * 0.7

    print("Left")
    GPIO.output(12, 1)
    time.sleep(0.2)
    GPIO.output(12, 0)
    for i in range(200):
        output = MotionTracker.readIMU(MotionTracker.IMU)
        if(output[0] > maxX):
            maxX = output[0]
    accXmax = minY * 0.7

    print("Right")
    GPIO.output(12, 1)
    time.sleep(0.2)
    GPIO.output(12, 0)
    for i in range(200):
        output = MotionTracker.readIMU(MotionTracker.IMU)
        if(output[0] < minX):
            minX = output[0]
    accXmin = minY * 0.7

    writefile = open(IMU_data, 'w')
    writefile.write(str(minY) + "\n")
    writefile.write(str(minX) + "\n")
    writefile.write(str(maxX))

    print("Across: " + str(minY) + " Left: " + str(maxX) + " Right: " + str(minX))

    
def read(): #Xx, Xy, Xz

    global accYmin
    global accXmin
    global accXmax
    
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)
    output = MotionTracker.readIMU(MotionTracker.IMU)

    ACCx = output[0]
    ACCy = output[1]

    #dt_squared = (ending time - initial time)**2
    #Xx = ACCx * dt_squared
    #Xy = ACCy * dt_squared
    #Xz = ACCz * dt_squared

    #if (Xx > some distance) and (Xy < some distance) and (Xz < some distance):
    if (ACCx > accXmin) and (ACCx < accXmax) and (ACCy < accYmin):         #Across
        return "A"
    #elif (Xx < some distance) and (Xy > some distance) and (Xz < some distance):
    elif (ACCx < accXmin) and (ACCx < accXmax) and (ACCy > accYmin):       #Left
        return "R"
    #elif (Xx < some distance) and (Xy < some distance) and (Xz > some distance):
    elif (ACCx > accXmin) and (ACCx > accXmax) and (ACCy > accYmin):      #Right
        return "L"
    else:
        return "X"

def main():
    iliketrains()

if __name__ == "__main__":
    main()