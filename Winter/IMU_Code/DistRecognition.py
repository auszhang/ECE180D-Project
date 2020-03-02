import MotionTracker
import datetime
import time

accelerometer = [0, 0]
heading = 0
old_heading = 0
CF_velocity = [0, 0]
CF_factor = 0.07     #Larger --> More accelerometery, Smaller --> More magnetometery
heading_gain = 1
accelerometer_gain = 0.1
Ymax = 30
Xmin = -4 
Xmax = 4

a = datetime.datetime.now()

def waitForSteady():
    counter = 0
    while counter < 10:
        read()
        if CF_velocity[0] < 1 and CF_velocity[0] > -1 and CF_velocity[1] < 8 and CF_velocity[1] > -8:
            counter = counter + 1
        else:
            counter = 0
    print("Ready")

def read():
    global a
    global accelerometer
    global heading
    global old_heading
    global CF_velocity
    global CF_factor
    global heading_gain
    global accelerometer_gain
    global Ymax
    global Xmin 
    global Xmax 

    b = datetime.datetime.now() - a
    a = datetime.datetime.now()
    LP = (b.microseconds/(1000000*1.0))**2

    output = MotionTracker.readIMU(MotionTracker.IMU)

    accelerometer[0] = output[0] * accelerometer_gain
    accelerometer[1] = output[1] * accelerometer_gain
    heading = output[2]

    delta_heading = heading_gain * (heading - old_heading)
    old_heading = heading

    CF_velocity[0] = CF_factor * accelerometer[0] - (1-CF_factor) * (delta_heading) # subtract because accelerometer increases when magnetometer decreases
    CF_velocity[1] = accelerometer[1]   #Cant do anything about across rip :(

    #print(str(accelerometer[0]) + ", " + str(accelerometer[1]) + ", " + str(heading) + ", " + str(CF_velocity[0]) + ", " + str(CF_velocity[1]))

    if CF_velocity[1] > Ymax:         #Across
        return "A"
    elif CF_velocity[0] < Xmin:       #Left
        return "L"
    elif CF_velocity[0] > Xmax:      #Right
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