import MotionTracker
import datetime
import time

results = [0, 0]
Ymax = 0.2
Xmin = -0.2 
Xmax = 0.2
HP_factor = 0.95

a = datetime.datetime.now()

def waitForSteady():
    counter = 0
    while counter < 10:
        read()
        if results[0] < 0.1 and results[0] > -0.1 and results[1] < 0.1 and results[1] > -0.1:
            counter = counter + 1
        else:
            counter = 0
    print("Ready")

def read():
    global a
    global results
    global Ymax
    global Xmin 
    global Xmax 
    global HP_factor

    b = datetime.datetime.now() - a
    a = datetime.datetime.now()
    LP = (b.microseconds/(1000000*1.0))**2

    output = MotionTracker.readIMU(MotionTracker.IMU)

    results[0] = (results[0] + output[0] * LP) * HP_factor
    results[1] = (results[1] + output[1] * LP) * HP_factor

    if results[1] > Ymax:         #Across
        return "A"
    elif results[0] < Xmin:       #Left
        return "L"
    elif results[0] > Xmax:      #Right
        return "R"
    else:
        return "X"

def main():
    waitForSteady()
    while(1):
        gesture = read()
        
        if gesture == "A":         #Across
            print("A")
            waitForSteady()
        elif gesture == "L":       #Left
            print("L")
            waitForSteady()
        elif gesture == "R":      #Right
            print("R")
            waitForSteady()

if __name__ == "__main__":
    main()