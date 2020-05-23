#!/usr/bin/python

import sys
import time
import math
import IMU
import datetime
import os
import subprocess

IMU_data = "../IMU_Local/IMU_data.txt"
f = open(IMU_data,'r')

magXmin =  float(f.readline())
magYmin =  float(f.readline())
magZmin =  float(f.readline())
magXmax =  float(f.readline())
magYmax =  float(f.readline())
magZmax =  float(f.readline())

# If the IMU is upside down (Skull logo facing up), change this value to 1
IMU_UPSIDE_DOWN = 1	
RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  	# [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      	# Complementary filter constant
MAG_LPF_FACTOR = 0.4 	# Low pass filter constant magnetometer
ACC_LPF_FACTOR = 0.1 	# Low pass filter constant for accelerometer, smaller = stronger
ACC_HPF_FACTOR = 0.9    # High pass filter constant for accelerometer, smaller = stronger
ACC_MEDIANTABLESIZE = 10    # Median filter table size for accelerometer. Higher = smoother but a longer delay
MAG_MEDIANTABLESIZE = 10    	# Median filter table size for magnetometer. Higher = smoother but a longer delay

#Kalman filter variables
Q_angle = 0.02
Q_gyro = 0.0015
R_angle = 0.005
y_bias = 0.0
x_bias = 0.0
XP_00 = 0.0
XP_01 = 0.0
XP_10 = 0.0
XP_11 = 0.0
YP_00 = 0.0
YP_01 = 0.0
YP_10 = 0.0
YP_11 = 0.0
KFangleX = 0.0
KFangleY = 0.0
gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0
CFangleXFiltered = 0.0
CFangleYFiltered = 0.0
kalmanX = 0.0
kalmanY = 0.0
oldXMagRawValue = 0
oldYMagRawValue = 0
oldZMagRawValue = 0
oldXAccRawValue = 0
oldYAccRawValue = 0
oldZAccRawValue = 0

HP_ACCx = 0
HP_ACCy = 0
HP_ACCz = 0
LP_ACCx = 0
LP_ACCy = 0
LP_ACCz = 0
BP_ACCx = 0
BP_ACCy = 0
BP_ACCz = 0

GYRx = 0
GYRy = 0
GYRz = 0

a = datetime.datetime.now()

flipper = [0, 0]
shifter = 0

#Setup the tables for the median filter. Fill them all with '1' so we dont get devide by zero error 
acc_medianTable1X = [1] * ACC_MEDIANTABLESIZE
acc_medianTable1Y = [1] * ACC_MEDIANTABLESIZE
acc_medianTable1Z = [1] * ACC_MEDIANTABLESIZE
acc_medianTable2X = [1] * ACC_MEDIANTABLESIZE
acc_medianTable2Y = [1] * ACC_MEDIANTABLESIZE
acc_medianTable2Z = [1] * ACC_MEDIANTABLESIZE
mag_medianTable1X = [1] * MAG_MEDIANTABLESIZE
mag_medianTable1Y = [1] * MAG_MEDIANTABLESIZE
mag_medianTable1Z = [1] * MAG_MEDIANTABLESIZE
mag_medianTable2X = [1] * MAG_MEDIANTABLESIZE
mag_medianTable2Y = [1] * MAG_MEDIANTABLESIZE
mag_medianTable2Z = [1] * MAG_MEDIANTABLESIZE

IMU.detectIMU()     #Detect if BerryIMUv1 or BerryIMUv2 is connected.
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

def kalmanFilterY ( accAngle, gyroRate, DT):
	y=0.0
	S=0.0

	global KFangleY
	global Q_angle
	global Q_gyro
	global y_bias
	global YP_00
	global YP_01
	global YP_10
	global YP_11

	KFangleY = KFangleY + DT * (gyroRate - y_bias)

	YP_00 = YP_00 + ( - DT * (YP_10 + YP_01) + Q_angle * DT )
	YP_01 = YP_01 + ( - DT * YP_11 )
	YP_10 = YP_10 + ( - DT * YP_11 )
	YP_11 = YP_11 + ( + Q_gyro * DT )

	y = accAngle - KFangleY
	S = YP_00 + R_angle
	K_0 = YP_00 / S
	K_1 = YP_10 / S
	
	KFangleY = KFangleY + ( K_0 * y )
	y_bias = y_bias + ( K_1 * y )
	
	YP_00 = YP_00 - ( K_0 * YP_00 )
	YP_01 = YP_01 - ( K_0 * YP_01 )
	YP_10 = YP_10 - ( K_1 * YP_00 )
	YP_11 = YP_11 - ( K_1 * YP_01 )
	
	return KFangleY

def kalmanFilterX ( accAngle, gyroRate, DT):
	x=0.0
	S=0.0

	global KFangleX
	global Q_angle
	global Q_gyro
	global x_bias
	global XP_00
	global XP_01
	global XP_10
	global XP_11


	KFangleX = KFangleX + DT * (gyroRate - x_bias)

	XP_00 = XP_00 + ( - DT * (XP_10 + XP_01) + Q_angle * DT )
	XP_01 = XP_01 + ( - DT * XP_11 )
	XP_10 = XP_10 + ( - DT * XP_11 )
	XP_11 = XP_11 + ( + Q_gyro * DT )

	x = accAngle - KFangleX
	S = XP_00 + R_angle
	K_0 = XP_00 / S
	K_1 = XP_10 / S
	
	KFangleX = KFangleX + ( K_0 * x )
	x_bias = x_bias + ( K_1 * x )
	
	XP_00 = XP_00 - ( K_0 * XP_00 )
	XP_01 = XP_01 - ( K_0 * XP_01 )
	XP_10 = XP_10 - ( K_1 * XP_00 )
	XP_11 = XP_11 - ( K_1 * XP_01 )
	
	return KFangleX

def readIMU(IMU):

    global magXmin
    global magYmin
    global magZmin
    global magXmax
    global magYmax
    global magZmax

    global IMU_UPSIDE_DOWN
    global RAD_TO_DEG
    global M_PI
    global G_GAIN 	# [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
    global AA     	# Complementary filter constant
    global MAG_LPF_FACTOR 	# Low pass filter constant magnetometer
    global ACC_LPF_FACTOR 	# Low pass filter constant for accelerometer
    global ACC_HPF_FACTOR   # High pass filter constant for accelerometer
    global ACC_MEDIANTABLESIZE    	# Median filter table size for accelerometer. Higher = smoother but a longer delay
    global MAG_MEDIANTABLESIZE    	# Median filter table size for magnetometer. Higher = smoother but a longer delay
   
    global Q_angle
    global Q_gyro
    global R_angle
    global y_bias
    global x_bias
    global XP_00
    global XP_01
    global XP_10
    global XP_11
    global YP_00
    global YP_01
    global YP_10
    global YP_11

    global KFangleX 
    global KFangleY 
    global gyroXangle 
    global gyroYangle 
    global gyroZangle 
    global CFangleX  
    global CFangleY 
    global CFangleXFiltered 
    global CFangleYFiltered 
    global kalmanX 
    global kalmanY 

    global oldXMagRawValue
    global oldYMagRawValue
    global oldZMagRawValue
    global oldXAccRawValue
    global oldYAccRawValue
    global oldZAccRawValue
    
    global HP_ACCx
    global HP_ACCy
    global HP_ACCz
    global LP_ACCx
    global LP_ACCy
    global LP_ACCz
    global BP_ACCx
    global BP_ACCy
    global BP_ACCz

    global GYRx
    global GYRy
    global GYRz
    
    global a

    global flipper
    global shifter

    global acc_medianTable1X
    global acc_medianTable1Y
    global acc_medianTable1Z
    global acc_medianTable2X
    global acc_medianTable2Y
    global acc_medianTable2Z
    global mag_medianTable1X
    global mag_medianTable1Y
    global mag_medianTable1Z
    global mag_medianTable2X
    global mag_medianTable2Y
    global mag_medianTable2Z
    
    #Read the accelerometer,gyroscope and magnetometer values
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()
    MAGx = IMU.readMAGx()
    MAGy = IMU.readMAGy()
    MAGz = IMU.readMAGz()

    GYRx = IMU.readGYRx()
    GYRy = IMU.readGYRy()
    GYRz = IMU.readGYRz()

    rate_gyr_x =  GYRx * G_GAIN
    rate_gyr_y =  GYRy * G_GAIN
    rate_gyr_z =  GYRz * G_GAIN

    #Apply compass calibration    
    MAGx -= (magXmin + magXmax) /2 
    MAGy -= (magYmin + magYmax) /2 
    MAGz -= (magZmin + magZmax) /2 

    ##Calculate loop Period(LP). How long between Gyro Reads
    b = datetime.datetime.now() - a
    a = datetime.datetime.now()
    LP = b.microseconds/(1000000*1.0)

    ############################################### 
    #### Apply high pass filter ####
    ###############################################
    HP_ACCx =  ACC_HPF_FACTOR * (HP_ACCx + ACCx - oldXAccRawValue)
    HP_ACCy =  ACC_HPF_FACTOR * (HP_ACCy + ACCy - oldYAccRawValue)
    HP_ACCz =  ACC_HPF_FACTOR * (HP_ACCz + ACCz - oldZAccRawValue)

    ############################################### 
    #### Apply low pass filter ####
    ###############################################
    MAGx =  MAGx  * MAG_LPF_FACTOR + oldXMagRawValue*(1 - MAG_LPF_FACTOR);
    MAGy =  MAGy  * MAG_LPF_FACTOR + oldYMagRawValue*(1 - MAG_LPF_FACTOR);
    MAGz =  MAGz  * MAG_LPF_FACTOR + oldZMagRawValue*(1 - MAG_LPF_FACTOR);
    BP_ACCx =  HP_ACCx  * ACC_LPF_FACTOR + BP_ACCx*(1 - ACC_LPF_FACTOR);
    BP_ACCy =  HP_ACCy  * ACC_LPF_FACTOR + BP_ACCy*(1 - ACC_LPF_FACTOR);
    BP_ACCz =  HP_ACCz  * ACC_LPF_FACTOR + BP_ACCz*(1 - ACC_LPF_FACTOR);
    LP_ACCx = ACCx * ACC_LPF_FACTOR + LP_ACCx * (1 - ACC_LPF_FACTOR);
    LP_ACCy = ACCy * ACC_LPF_FACTOR + LP_ACCy * (1 - ACC_LPF_FACTOR);
    LP_ACCz = ACCz * ACC_LPF_FACTOR + LP_ACCz * (1 - ACC_LPF_FACTOR);


    oldXMagRawValue = MAGx
    oldYMagRawValue = MAGy
    oldZMagRawValue = MAGz
    oldXAccRawValue = ACCx
    oldYAccRawValue = ACCy
    oldZAccRawValue = ACCz

    ######################################### 
    #### Median filter for accelerometer ####
    #########################################
    # cycle the table
    for x in range (ACC_MEDIANTABLESIZE-1,0,-1 ):
        acc_medianTable1X[x] = acc_medianTable1X[x-1]
        acc_medianTable1Y[x] = acc_medianTable1Y[x-1]
        acc_medianTable1Z[x] = acc_medianTable1Z[x-1]

    # Insert the lates values
    acc_medianTable1X[0] = LP_ACCx
    acc_medianTable1Y[0] = LP_ACCy
    acc_medianTable1Z[0] = LP_ACCz    

    # Copy the tables
    acc_medianTable2X = acc_medianTable1X[:]
    acc_medianTable2Y = acc_medianTable1Y[:]
    acc_medianTable2Z = acc_medianTable1Z[:]

    # Sort table 2
    acc_medianTable2X.sort()
    acc_medianTable2Y.sort()
    acc_medianTable2Z.sort()

    # The middle value is the value we are interested in\
    LP_ACCx = acc_medianTable2X[5];
    LP_ACCy = acc_medianTable2Y[5];
    LP_ACCz = acc_medianTable2Z[5];



    ######################################### 
    #### Median filter for magnetometer ####
    #########################################
    # cycle the table
    for x in range (MAG_MEDIANTABLESIZE-1,0,-1 ):
        mag_medianTable1X[x] = mag_medianTable1X[x-1]
        mag_medianTable1Y[x] = mag_medianTable1Y[x-1]
        mag_medianTable1Z[x] = mag_medianTable1Z[x-1]

    # Insert the latest values    
    mag_medianTable1X[0] = MAGx
    mag_medianTable1Y[0] = MAGy
    mag_medianTable1Z[0] = MAGz    

    # Copy the tables
    mag_medianTable2X = mag_medianTable1X[:]
    mag_medianTable2Y = mag_medianTable1Y[:]
    mag_medianTable2Z = mag_medianTable1Z[:]

    # Sort table 2
    mag_medianTable2X.sort()
    mag_medianTable2Y.sort()
    mag_medianTable2Z.sort()

    # The middle value is the value we are interested in
    MAGx = mag_medianTable2X[5];
    MAGy = mag_medianTable2Y[5];
    MAGz = mag_medianTable2Z[5];

    if IMU_UPSIDE_DOWN:
        MAGy = -MAGy      #If IMU is upside down, this is needed to get correct heading.
    #Calculate heading
    
    #print(str(MAGy) + ", " + str(MAGx))
    
    heading = 180 * math.atan2(MAGy,MAGx)/M_PI

    flipper[0] = flipper[1]
    flipper[1] = heading

    if flipper[0] > 90 and flipper[1] < -90:
        shifter += 360
    elif flipper[0] < -90 and flipper[1] > 90:
        shifter -= 360 

    flipped_heading = heading + shifter

    #if heading < 0:
    #    heading = heading + 360

#    ####################################################################
#    ###################Tilt compensated heading#########################
#    ####################################################################
#    #Normalize accelerometer raw values.
#    if not IMU_UPSIDE_DOWN:        
#        #Use these two lines when the IMU is up the right way. Skull logo is facing down
#        accXnorm = LP_ACCx/math.sqrt(LP_ACCx * LP_ACCx + LP_ACCy * LP_ACCy + LP_ACCz * LP_ACCz)
#        accYnorm = LP_ACCy/math.sqrt(LP_ACCx * LP_ACCx + LP_ACCy * LP_ACCy + LP_ACCz * LP_ACCz)
#    else:
#        #Us these four lines when the IMU is upside down. Skull logo is facing up
#        accXnorm = -LP_ACCx/math.sqrt(LP_ACCx * LP_ACCx + LP_ACCy * LP_ACCy + LP_ACCz * LP_ACCz)
#        accYnorm = LP_ACCy/math.sqrt(LP_ACCx * LP_ACCx + LP_ACCy * LP_ACCy + LP_ACCz * LP_ACCz)
#
#    #Calculate pitch and roll
#
#    pitch = math.asin(accXnorm)
#    roll = -math.asin(accYnorm/math.cos(pitch))
#
#
#    #Calculate the new tilt compensated values
#    magXcomp = MAGx*math.cos(pitch)+MAGz*math.sin(pitch)
#
#    #The compass and accelerometer are orientated differently on the LSM9DS0 and LSM9DS1 and the Z axis on the compass
#    #is also reversed. This needs to be taken into consideration when performing the calculations
#    if(IMU.LSM9DS0):
#        magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)-MAGz*math.sin(roll)*math.cos(pitch)   #LSM9DS0
#    else:
#        magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)+MAGz*math.sin(roll)*math.cos(pitch)   #LSM9DS1
#
#
#    #Calculate tilt compensated heading
#    tiltCompensatedHeading = 180 * math.atan2(magYcomp,magXcomp)/M_PI

    #if tiltCompensatedHeading < 0:
    #            tiltCompensatedHeading += 360

    ############################ END ##################################

    #print(str(ACCx) + ", " + str(ACCy) + ", " + str(ACCz) + ", " + str(gyroXangle) + ", " + str(gyroYangle) + ", " + str(gyroZangle) + ", " + str(CFangleX) + ", " + str(CFangleY))
    outputarray = [BP_ACCx, BP_ACCy, BP_ACCz, rate_gyr_x, rate_gyr_y, rate_gyr_z]

    #if 1:			#Change to '0' to stop showing the angles from the accelerometer
    #    print ("# ACCX Angle %5.2f \t\t ACCY Angle %5.2f #  " % (AccXangle, AccYangle)),
    #
    #if 1:			#Change to '0' to stop  showing the angles from the gyro
    #    print ("\t\t# GRYX Angle %5.2f \t\t GYRY Angle %5.2f \t\t GYRZ Angle %5.2f # " % (gyroXangle,gyroYangle,gyroZangle)),
    #
    #if 1:			#Change to '0' to stop  showing the angles from the complementary filter
    #    print ("\t\t# CFangleX Angle %5.2f \t\t  CFangleY Angle %5.2f #" % (CFangleX,CFangleY)),
    #
    #if 0:			#Change to '0' to stop  showing the heading
    #    print ("\t\t# HEADING %5.2f \t\t tiltCompensatedHeading %5.2f #" % (heading,tiltCompensatedHeading)),
    #
    #if 1:			#Change to '0' to stop  showing the angles from the Kalman filter
    #    print ("\t\t# kalmanX %5.2f \t\t  kalmanY %5.2f #" % (kalmanX,kalmanY)),
    #
    #if 0:
    #    print ("#MAGX %5.2f     #MAGY %5.2f     #MAGZ %5.2f     #MAGXCOMP %5.2f     #MAGYCOMP %5.2f" % (MAGx, MAGy, MAGz, magXcomp, magYcomp)),

    #print a new line
    #print "" 

    return outputarray

def measureOffset(IMU):
    global accXOffset
    global accYOffset
    global accZOffset
    
    samples = 200

    print("Measuring accelerometer offsets")
    xtotal = 0
    ytotal = 0
    ztotal = 0
    for i in range(samples):
        xtotal = xtotal + IMU.readACCx()
        ytotal = ytotal + IMU.readACCy()
        ztotal = ztotal + IMU.readACCz()

    accXOffset = xtotal / samples
    accYOffset = ytotal / samples
    accZOffset = ztotal / samples
