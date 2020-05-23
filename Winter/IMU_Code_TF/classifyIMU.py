import MotionTrackerNN
import tensorflow.lite as tfl
import numpy as np

# Load TFLite model and allocate tensors.
interpreter = tfl.Interpreter(model_path="gesture_model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def main():
    accelerationThreshold = 600
    numSamples = 150 
    samplesRead = numSamples
    dataArray = np.array(np.random.random_sample([1,900]), dtype=np.float32)

    print("aX,aY,aZ,gX,gY,gZ")

    while True:
        while samplesRead == numSamples: 
            output = MotionTrackerNN.readIMU(MotionTrackerNN.IMU)
            aSum = abs(output[0]) + abs(output[1]) + abs(output[2])
            if aSum >= accelerationThreshold:
                samplesRead = 0
                break
        
        while samplesRead < numSamples:
            output = MotionTrackerNN.readIMU(MotionTrackerNN.IMU)          
            #print("%f,%f,%f,%f,%f,%f" %(output[0], output[1], output[2], output[3], output[4], output[5]))
            dataArray[0][samplesRead * 6 + 0] = np.float32(output[0])
            dataArray[0][samplesRead * 6 + 1] = np.float32(output[1])
            dataArray[0][samplesRead * 6 + 2] = np.float32(output[2])
            dataArray[0][samplesRead * 6 + 3] = np.float32(output[3])
            dataArray[0][samplesRead * 6 + 4] = np.float32(output[4])
            dataArray[0][samplesRead * 6 + 5] = np.float32(output[5])
            samplesRead = samplesRead + 1

            if samplesRead == numSamples:
                interpreter.set_tensor(input_details[0]['index'], dataArray)
                interpreter.invoke()
                outputData = interpreter.get_tensor(output_details[0]['index'])
                print("Across: %f" %(outputData[0][0]))
                print("Left: %f" %(outputData[0][1]))
                print("Right: %f" %(outputData[0][2]))

if __name__ == "__main__":
    main()