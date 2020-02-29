import MotionTracker
import datetime
import time

IMU_data = "../IMU_Local/IMU_data.txt"
f = open(IMU_data,'r')

#some distance = float(f.readline())

a = datetime.datetime.now()

def read(Xx, Xy, Xz): #Xx, Xy, Xz

    global a

    b = datetime.datetime.now() - a
    a = datetime.datetime.now()
    LP = (b.microseconds/(1000000*1.0))**2

    output = MotionTracker.readIMU(MotionTracker.IMU)

    ACCx = output[0]
    ACCy = output[1]
    ACCz = output[2]

    pullFactor = 0.05

    Xx = (Xx + ACCx * LP) * (1 - pullFactor)
    Xy = (Xy + ACCy * LP) * (1 - pullFactor)
    Xz = (Xz + ACCz * LP) * (1 - pullFactor)

    #print(str(Xx) + "," + str(Xy) + "," + str(Xz))

    return [Xx, Xy, Xz]

def main():
    results = [0, 0, 0]

    Ymax = 0.1
    Xmin = -0.1 
    Xmax = 0.1

    while(1):
        results = read(results[0], results[1], results[2])
        
        if results[1] > Ymax:         #Across
            print("A")
            for i in range(50):
                results = read(results[0], results[1], results[2])
        elif results[0] < Xmin:       #Left
            print("L")
            for i in range(50):
                results = read(results[0], results[1], results[2])
        elif results[0] > Xmax:      #Right
            print("R")
            for i in range(50):
                results = read(results[0], results[1], results[2])

if __name__ == "__main__":
    main()