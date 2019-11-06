# File Name: photoBooth.py
# File Path: /home/ludwigg/Python/PyRpi_PhotoBooth/photoBooth.py
# Run Command: sudo python3 /home/ludwigg/Python/PyRpi_PhotoBooth/photoBooth.py

# Grant Ludwig
# 11/11/2019
# PhotoBooth

# Import Libraries
import time
import RPi.GPIO as GPIO # Raspberry Pi GPIO library

GPIO_A = 12
GPIO_B = 13
GPIO_C = 6
GPIO_D = 16
GPIO_E = 17
GPIO_F = 27
GPIO_G = 5

# Setup GPIO
GPIO.setwarnings(False) # Ignore warnings
GPIO.setmode(GPIO.BCM) # Use BCM Pin numbering

GPIO.setup(4, GPIO.OUT, initial=GPIO.HIGH) # DP

segments = (GPIO_A, GPIO_B, GPIO_C, GPIO_D, GPIO_E, GPIO_F, GPIO_G)
# digits = () #TODO

# sets all segments off
for segment in segments:
	GPIO.setup(segment, GPIO.OUT)
	GPIO.output.(segment, 0)
	
# sets all digits to 1, aka not grounded
for digit in digits:
	GPIO.setup(digit, GPIO.OUT)
	GPIO.output.(digit, 1)

# A B C D E F G
numberMap = {" ":(0,0,0,0,0,0,0),
			"0":(1,1,1,1,1,1,0),
			"1":(0,1,1,0,0,0,0),
			"2":(1,1,0,1,1,0,1),
			"3":(1,1,1,1,0,0,1),
			"4":(0,1,1,0,0,1,1),
			"5":(1,0,1,1,0,1,1),
			"6":(1,0,1,1,1,1,1),
			"7":(1,1,1,0,0,0,0),
			"8":(1,1,1,1,1,1,1),
			"9":(1,1,1,1,0,1,1)}

try:
	while(True): 
		output = "0123"
        for i in range(len(digits):
            for j in range(len(segments)):
                GPIO.output(segments[j], numberMap[output[i]][j])
            GPIO.output(digits[i], 0)
            time.sleep(0.001)
            GPIO.output(digits[i], 1)

except KeyboardInterrupt: 
    # This code runs on a Keyboard Interrupt <CNTRL>+C
	print('\n\n' + 'Program exited on a Keyboard Interrupt' + '\n') 

except: 
    # This code runs on any error
	print('\n' + 'Errors occurred causing your program to exit' + '\n')

finally: 
    # This code runs on every exit and sets any used GPIO pins to input mode.
	GPIO.cleanup()