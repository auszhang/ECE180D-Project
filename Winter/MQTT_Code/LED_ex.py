# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
import time
import RPi.GPIO as GPIO

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI 
 
# Configure the count of pixels:
PIXEL_COUNT = 8
 
# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

#Serene's code here:
BLUE = [0, 59, 91]
GOLD = [254, 184, 28]
MAX_INTENSITY = 80 #max intensity desired on these LEDs

def str2color(c1):
    col = [0,0,0]
    if c1 == "d":
        col = GOLD
    elif c1 == "b":
        col = BLUE
    return col
    

def one_at_a_time(pixels, wait=0.9,color=(255,0,0)):
    pixels.clear()
    for i in range(pixels.count()):
        for j in range(pixels.count()):
            if i!=j:
                pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color( 0,0,0 ) )
            else:
                pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] )) 
        pixels.show()
        if wait > 0:
            time.sleep(wait)

#NOTE: Cap rotation functionality was deleted

def have_potato_lights(pixels):
    pixels.clear()
    # red = [254, 0, 0]
    # dark_orange = [255, 90, 0]
    # light_orange = [255, 154, 0]
    # yellow = [254, 206, 0]
    for j in range(PIXEL_COUNT):
        if j == 0:
            color = [38, 110, 246] #blue
        elif j == 1:
            color = [228, 41, 242] #purple
        elif j == 2:
            color = [255, 139, 0] #orange
        elif j == 3: 
            color = [255, 1, 48] #red
        elif j == 4:
            color = [255, 211, 0] #yellow
        elif j == 5:
            color = [18, 231, 114] #green
        else:
            color = GOLD
        r1=color[0] * MAX_INTENSITY/255;
        g1=color[1] * MAX_INTENSITY/255;
        b1=color[2] * MAX_INTENSITY/255;
        pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(r1,g1,b1 ))
    pixels.show()

def eliminated_lights(pixels):
    pixels.clear()
    for j in range(PIXEL_COUNT):
        pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(0,0,0))
    pixels.show()

def show_and_wait(c):
        for j in range(PIXEL_COUNT):
            pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(c[0]*MAX_INTENSITY/255,c[1]*MAX_INTENSITY/255,c[2]*MAX_INTENSITY/255))
            pixels.show()
            time.sleep(0.1)

def winning_sequence(pixels):
    pixels.clear()
    while True:
        show_and_wait( [124, 252, 0] ) #bright green
        show_and_wait( [0, 120, 0]  ) #dark green
        show_and_wait( [51, 204, 10] ) #lime green
        show_and_wait([25, 89, 5] ) #Lincoln green
        show_and_wait( [76, 186, 10] ) #Kelly green

def timer_interval_lights(pixels):
    color = [46, 139, 87] #seagreen
    r1=color[0] * MAX_INTENSITY/255;
    g1=color[1] * MAX_INTENSITY/255;
    b1=color[2] * MAX_INTENSITY/255;
    pixels.clear()
    for j in range(PIXEL_COUNT):
        pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(r1,g1,b1 ))
    pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(r1,g1,b1 ))
    pixels.show()
    time.sleep(0.2)

def final_warning_lights(pixels):
    color = [254, 0, 0] #red
    r1=color[0] * MAX_INTENSITY/255;
    g1=color[1] * MAX_INTENSITY/255;
    b1=color[2] * MAX_INTENSITY/255;
    pixels.clear()
    for j in range(PIXEL_COUNT):
        pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(r1,g1,b1 ))
    pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(r1,g1,b1 ))
    pixels.show()
    time.sleep(0.2)



def no_potato_lights(pixels):
    pixels.clear()
    # light_blue = [167, 214, 235]
    # mid_blue = [103, 170, 223]
    # dark_blue = [20, 91, 155]
    # purple = [128, 129, 184]
    color = BLUE
    for j in range(PIXEL_COUNT):
        r1=color[0] * MAX_INTENSITY/255;
        g1=color[1] * MAX_INTENSITY/255;
        b1=color[2] * MAX_INTENSITY/255;
        pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(r1,g1,b1 ))
    pixels.show()

def enact_lights_basic(pixels, data, my_id):
    pixels.clear()
    print(str(data))
    light_msgs = data.split("#")
    print(str(my_id))
    for msg in light_msgs:
        #client_id = msg[:-9]
        msgs = msg.split(".")
        client_id = msgs[0]
        print(str(client_id))
        if client_id == my_id:
            light_msg = msg[-8:]
            print(str(light_msg))
            for j in range(len(light_msg)):
                #print(int(j))
                c1=int(light_msg[j])*50;
                pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(0,0, c1 )) #preset to blue
            pixels.show()
            # time.sleep(0.2)

def enact_lights_with_color(pixels, data, my_id):
    # NEED TO TEST SOON!!!!!!!!!!!!!!!!!!    
    pixels.clear()
    print(str(data))
    light_msgs = data.split("#")
    print(str(my_id))
    for msg in light_msgs:
        #client_id = msg[:-9]
        msgs = msg.split(".")
        client_id = msgs[0]
        print(str(client_id))
        if client_id == my_id:
            light_msg = msg[-8:]
            print(str(light_msg))
            for j in range(len(light_msg)):
                
                color = str2color(light_msg[j])
                r1=color[0] * MAX_INTENSITY/255;
                g1=color[1] * MAX_INTENSITY/255;
                b1=color[2] * MAX_INTENSITY/255;
                pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(r1,g1,b1 )) 
            pixels.show()
            # time.sleep(0.2)

# enact_lights_basic incorporated with IMU
def enact_lights_basic_tilt(pixels, data, tiltHeading, my_id):
    pixels.clear()
    print(str(data))
    light_msgs = data.split("#")
    print(str(my_id))
    for msg in light_msgs:
        #client_id = msg[:-9]
        msgs = msg.split(".")
        client_id = msgs[0]
        print(str(client_id))
        if client_id == my_id:
            light_msg = msg[-8:]
            print(str(light_msg))
            # Get rotated light_msg.
            rot_light_msg = get_rotation(tiltHeading, light_msg)
            for j in range(len(rot_light_msg)):
                #print(int(j))
                c1=int(rot_light_msg[j])*50;
                pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(0,0, c1 )) #preset to blue
            pixels.show()
            # Return UNROTATED light_msg.
            return light_msg
            # time.sleep(0.2)
    return ''

# Same functionality as enact_lights_basic_tilt, but take a light message directly as input data
def parsed_basic_tilt(pixels, data, tiltHeading):
    light_msg = data
    print(str(light_msg))
    # Get rotated light_msg.
    rot_light_msg = get_rotation(tiltHeading, light_msg)
    pixels.clear()
    for j in range(len(rot_light_msg)):
        c1=int(rot_light_msg[j])*50;
        pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(0,0, c1 )) #preset to blue
    pixels.show()
    # Return UNROTATED light_msg.
    return light_msg

# enact_lights_with_color incorporated with IMU
def enact_lights_with_color_tilt(pixels, data, tiltHeading, my_id):
    pixels.clear()
    print(str(data))
    light_msgs = data.split("#")
    print(str(my_id))
    for msg in light_msgs:
        #client_id = msg[:-9]
        msgs = msg.split(".")
        client_id = msgs[0]
        print(str(client_id))
        if client_id == my_id:
            light_msg = msg[-8:]
            print(str(light_msg))
            # Get rotated light_msg.
            rot_light_msg = get_rotation(tiltHeading, light_msg)
            for j in range(len(rot_light_msg)):
                
                color = str2color(rot_light_msg[j])
                r1=color[0] * MAX_INTENSITY/255;
                g1=color[1] * MAX_INTENSITY/255;
                b1=color[2] * MAX_INTENSITY/255;
                pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(r1,g1,b1 )) 
            pixels.show()
            # Return UNROTATED light_msg. 
            return light_msg
            # time.sleep(0.2)
    return ''

# Same functionality as enact_lights_with_color_tilt, but take a light message directly as input data
def parsed_color_tilt(pixels, data, tiltHeading):
    light_msg = data
    print(str(light_msg))
    # Get rotated light_msg.
    rot_light_msg = get_rotation(tiltHeading, light_msg)
    pixels.clear()
    for j in range(len(rot_light_msg)):
        color = str2color(rot_light_msg[j])
        r1=color[0] * MAX_INTENSITY/255;
        g1=color[1] * MAX_INTENSITY/255;
        b1=color[2] * MAX_INTENSITY/255;
        pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(r1,g1,b1 )) #preset to blue
    pixels.show()
    # Return UNROTATED light_msg. 
    return light_msg

 ## EXAMPLE CODE
# Define the wheel function to interpolate between different hues.
def wheel(pos):
    if pos < 85:
        return Adafruit_WS2801.RGB_to_color( (pos * 3) * MAX_INTENSITY/255, (255 - pos * 3)*MAX_INTENSITY/255, 0)
    elif pos < 170:
        pos -= 85
        return Adafruit_WS2801.RGB_to_color( (255 - pos * 3) * MAX_INTENSITY/255, 0, (pos * 3)*MAX_INTENSITY/255 )
    else:
        pos -= 170
        return Adafruit_WS2801.RGB_to_color(0, (pos * 3) * MAX_INTENSITY/255, (255 - pos * 3)*MAX_INTENSITY/255 )
 
# Define rainbow cycle function to do a cycle of all hues.
def rainbow_cycle_successive(pixels, wait=0.1):
    for i in range(pixels.count()):
        # tricky math! we use each pixel as a fraction of the full 96-color wheel
        # (thats the i / strip.numPixels() part)
        # Then add in j which makes the colors go around per pixel
        # the % 96 is to make the wheel cycle around
        pixels.set_pixel(i, wheel(((i * 256 // pixels.count())) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def rainbow_cycle(pixels, wait=0.005):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((i * 256 // pixels.count()) + j) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def rainbow_colors(pixels, wait=0.05):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((256 // pixels.count() + j)) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def brightness_decrease(pixels, wait=0.01, step=1):
    for j in range(int(256 // step)):
        for i in range(pixels.count()):
            r, g, b = pixels.get_pixel_rgb(i)
            r = int(max(0, r - step))
            g = int(max(0, g - step))
            b = int(max(0, b - step))
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color( r, g, b ))
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def blink_color(pixels, blink_times=5, wait=0.5, color=(255,0,0)):
    for i in range(blink_times):
        # blink two times, then wait
        pixels.clear()
        for j in range(2):
            for k in range(pixels.count()):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            pixels.show()
            time.sleep(0.08)
            pixels.clear()
            pixels.show()
            time.sleep(0.08)
        time.sleep(wait)
 
def appear_from_back(pixels, color=(255, 0, 0)):
    pos = 0
    for i in range(pixels.count()):
        for j in reversed(range(i, pixels.count())):
            pixels.clear()
            # first set all pixels at the begin
            for k in range(i):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            # set then the pixel at position j
            pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
            pixels.show()
            time.sleep(0.02)
            
 
if __name__ == "__main__":
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!
 
    rainbow_cycle_successive(pixels, wait=0.1)
    rainbow_cycle(pixels, wait=0.01)
 
    brightness_decrease(pixels)
    
    appear_from_back(pixels)
    
    for i in range(3):
        blink_color(pixels, blink_times = 1, color=(255, 0, 0))
        blink_color(pixels, blink_times = 1, color=(0, 255, 0))
        blink_color(pixels, blink_times = 1, color=(0, 0, 255))
 
    
    
    rainbow_colors(pixels)
    
    brightness_decrease(pixels)
    
