import MotionTracker
import datetime
import time

accelerometer = [0, 0]
heading = 0
old_heading = 0
CF_velocity = [0, 0]
CF_factor = 0.06     #Larger --> More accelerometery, Smaller --> More magnetometery
LP_factor = 0
heading_gain = 0.5
accelerometer_gain = 0.1
Ymax = 30
Xmin = -4 
Xmax = 4
counter = 0
counter_cap = 30
is_steady = False

#a = datetime.datetime.now()

def read():
    #global a
    global counter
    global counter_cap
    global is_steady
    global accelerometer
    global heading
    global old_heading
    global CF_velocity
    global CF_factor
    global LP_factor
    global heading_gain
    global accelerometer_gain
    global Ymax
    global Xmin 
    global Xmax 

    #b = datetime.datetime.now() - a
    #a = datetime.datetime.now()
    #LP = (b.microseconds/(1000000*1.0))**2

    output = MotionTracker.readIMU(MotionTracker.IMU)

    accelerometer[0] = output[0] * accelerometer_gain
    accelerometer[1] = output[1] * accelerometer_gain
    heading = output[2]

    delta_heading = heading_gain * (heading - old_heading)
    old_heading = heading

    CF_velocity[0] = CF_factor * accelerometer[0] - (1-CF_factor) * (delta_heading) # subtract because accelerometer increases when magnetometer decreases
    CF_velocity[1] = LP_factor * CF_velocity[1] + (1 - LP_factor) * accelerometer[1]   #Low Pass this bitch into velocity

    #print(str(heading))

    if CF_velocity[1] > Ymax and is_steady:         #Across
        counter = 0
        is_steady = False
        return "A"
    elif CF_velocity[0] < Xmin and is_steady:       #Left
        counter = 0
        is_steady = False
        return "R"
    elif CF_velocity[0] > Xmax and is_steady:      #Right
        counter = 0
        is_steady = False
        return "L"
    elif CF_velocity[0] < 1 and CF_velocity[0] > -1 and CF_velocity[1] < 8 and CF_velocity[1] > -8: #Steady
        if counter < counter_cap:
            counter = counter + 1
            is_steady = False
        else:
            is_steady = True
        return "X"
    else:
        return "X"

def main():
    
    global is_steady

    while(1):
        gesture = read()
        
        if gesture == "A":         #Across
            print("A")
        elif gesture == "R":       #Left
            print("R")
        elif gesture == "L":      #Right
            print("L")

if __name__ == "__main__":
    main()