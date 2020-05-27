import MotionTrackerNN
import RPi.GPIO as GPIO 

#setup vibration motor
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

def main():
    accelerationThreshold = 600
    numSamples = 150; 
    samplesRead = numSamples

    print("aX,aY,aZ,gX,gY,gZ")

    while True:
        while samplesRead == numSamples: 
            GPIO.output(12,1)
            output = MotionTrackerNN.readIMU(MotionTrackerNN.IMU)
            aSum = abs(output[0]) + abs(output[1]) + abs(output[2])
            if aSum >= accelerationThreshold:
                samplesRead = 0
                break
        
        while samplesRead < numSamples:
            GPIO.output(12,0)
            output = MotionTrackerNN.readIMU(MotionTrackerNN.IMU)
            samplesRead = samplesRead + 1          
            print("%f,%f,%f,%f,%f,%f" %(output[0], output[1], output[2], output[3], output[4], output[5]))
            if samplesRead == numSamples:
                print("")


if __name__ == "__main__":
    main()