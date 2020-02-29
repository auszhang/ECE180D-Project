import MotionTracker
import datetime
import time

results = [0, 0, 0]
Ymax = 0.2
Xmin = -0.2 
Xmax = 0.2

a = datetime.datetime.now()

def waitForSteady():
    #keep reading until results[0,1,2] are close to 0
    return 0

def read():
    global a
    global results
    global Ymax
    global Xmin 
    global Xmax 

    b = datetime.datetime.now() - a
    a = datetime.datetime.now()
    LP = (b.microseconds/(1000000*1.0))**2

    output = MotionTracker.readIMU(MotionTracker.IMU)

    pullFactor = 0.05

    results[0] = (results[0] + output[0] * LP) * (1 - pullFactor)
    results[1] = (results[1] + output[1] * LP) * (1 - pullFactor)
    results[2] = (results[2] + output[2] * LP) * (1 - pullFactor)

    if results[1] > Ymax:         #Across
        #results = [0,0,0]
        print("A")
        return "A"
    elif results[0] < Xmin:       #Left
        #results = [0,0,0]
        print("L")
        return "L"
    elif results[0] > Xmax:      #Right
        #results = [0,0,0]
        print("R")
        return "R"
    else:
        return "X"

def main():
    global results
    global Ymax
    global Xmin 
    global Xmax 

    while(1):
        results = read()
        
        if results[1] > Ymax:         #Across
            print("A")
            for i in range(50):
                results = read()
        elif results[0] < Xmin:       #Left
            print("L")
            for i in range(50):
                results = read()
        elif results[0] > Xmax:      #Right
            print("R")
            for i in range(50):
                results = read()

if __name__ == "__main__":
    main()