# File Name: photoBooth.py
# File Path: /home/ludwigg/Python/PyRpi_PhotoBooth/photoBooth.py
# Run Command: sudo python3 /home/ludwigg/Python/PyRpi_PhotoBooth/photoBooth.py

# Grant Ludwig
# 11/11/2019
# PhotoBooth

# Import Libraries
import RPi.GPIO as GPIO # Raspberry Pi GPIO library

# Setup GPIO
GPIO.setwarnings(False) # Ignore warnings
GPIO.setmode(GPIO.BCM) # Use BCM Pin numbering
GPIO.setup(4, GPIO.OUT, initial=GPIO.HIGH) # DP
GPIO.setup(5, GPIO.OUT, initial=GPIO.HIGH) # G
GPIO.setup(6, GPIO.OUT, initial=GPIO.HIGH) # C
GPIO.setup(12, GPIO.OUT, initial=GPIO.HIGH) # A
GPIO.setup(13, GPIO.OUT, initial=GPIO.HIGH) # B
GPIO.setup(16, GPIO.OUT, initial=GPIO.HIGH) # D
GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH) # E
GPIO.setup(27, GPIO.OUT, initial=GPIO.HIGH) # F

try:
# Setup infinite loop
	while(1): 
		print()

except KeyboardInterrupt: 
    # This code runs on a Keyboard Interrupt <CNTRL>+C
	print('\n\n' + 'Program exited on a Keyboard Interrupt' + '\n') 

except: 
    # This code runs on any error
	print('\n' + 'Errors occurred causing your program to exit' + '\n')

finally: 
    # This code runs on every exit and sets any used GPIO pins to input mode.
	GPIO.cleanup()