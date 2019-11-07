# File Name: photoBooth.py
# File Path: /home/ludwigg/Python/PyRpi_PhotoBooth/photoBooth.py
# Run Command: sudo python3 /home/ludwigg/Python/PyRpi_PhotoBooth/photoBooth.py

# Grant Ludwig
# 11/11/2019
# PhotoBooth

# Import Libraries
import time
import RPi.GPIO as GPIO # Raspberry Pi GPIO library
from PIL import Image
from picamera import PiCamera
from twython import Twython

GPIO_A = 12
GPIO_B = 13
GPIO_C = 6
GPIO_D = 16
GPIO_E = 17
GPIO_F = 27
GPIO_G = 5
GPIO_D1 = 22
GPIO_D2 = 25
GPIO_D3 = 24
GPIO_D4 = 23
GPIO_COLON = 10
GPIO_BUTTON = 26

SAVED_PHOTO_NAME = "Photos.png"
PICTURE_TIME = 10
CLOCK_DISPLAY_LENGTH = 4
NUM_PICTURES = 4
BORDER_SIZE = 20
PICTURE_WIDTH = 500
PICTURE_HEIGHT = 500
pictureStripHeight = (PICTURE_HEIGHT * NUM_PICTURES) + (BORDER_SIZE * (NUM_PICTURES + 1))
pictureStripWidth = (PICTURE_WIDTH + BORDER_SIZE * 2)

# Setup GPIO
GPIO.setwarnings(False) # Ignore warnings
GPIO.setmode(GPIO.BCM) # Use BCM Pin numbering

GPIO.setup(GPIO_COLON, GPIO.OUT, initial=GPIO.HIGH) # :

segments = (GPIO_A, GPIO_B, GPIO_C, GPIO_D, GPIO_E, GPIO_F, GPIO_G)
digits = (GPIO_D1, GPIO_D2, GPIO_D3, GPIO_D4)

# sets all segments off
for segment in segments:
	GPIO.setup(segment, GPIO.OUT)
	GPIO.output(segment, 0)
	
# sets all digits to 1, aka not grounded
for digit in digits:
	GPIO.setup(digit, GPIO.OUT)
	GPIO.output(digit, 1)

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

clockOutput = "0000"

clockSet = False
beginTime = 0
takingPictures = False
numberOfPictures = 0
savedPictures = False
camera = PiCamera() 
camera.resolution = (PICTURE_WIDTH, PICTURE_HEIGHT)

def countDown():
    global clockOutput
    global clockSet
    global beginTime
    global camera
    if not clockSet:
        beginTime = time.time() + PICTURE_TIME
        clockSet = True
        return True
    else:
        timeLeft = round(beginTime - time.time(), 2)
        if timeLeft <= 0:
            clockOutput = "0000"
            camera.capture("images/image%s.jpg" % (numberOfPictures + 1))
            return False
        else:
            timeString = str(timeLeft)
            splitTime = timeString.split(".")
            clockOutput = ""
            if len(splitTime[0]) < 2:
                clockOutput += "0"
            clockOutput += splitTime[0]
            clockOutput += splitTime[1]
            while len(clockOutput) < CLOCK_DISPLAY_LENGTH:
                clockOutput += "0"
            return True
				
def startPictures(channel):
    global takingPictures
    global numberOfPictures
    global savedPictures
    if not takingPictures:
        takingPictures = True
        numberOfPictures = 0
        savedPictures = False
        
def savePhotos():
    global savedPictures
    imageList = []
    for i in range(numberOfPictures):
        imageList.append(Image.open("images/image%s.jpg" % (i + 1)))
    suLogo = Image.open("images/SUlogo.png")
    
    watermark = Image.new("RGBA", (pictureStripWidth, pictureStripHeight))
    watermark.paste(suLogo, ((BORDER_SIZE + PICTURE_WIDTH) - suLogo.width, 
                            (BORDER_SIZE * numberOfPictures) + (PICTURE_HEIGHT * numberOfPictures) - suLogo.height - BORDER_SIZE))
    
    newImage = Image.new("RGBA", (pictureStripWidth, pictureStripHeight), (0, 0, 0, 255))
    for i in range(len(imageList)):
        newImage.paste(imageList[i], (BORDER_SIZE, (BORDER_SIZE * (i + 1)) + (PICTURE_HEIGHT * i)))
    
    saveImage = Image.alpha_composite(newImage, watermark) # adds the SU watermark
    saveImage.save("images/%s" % SAVED_PHOTO_NAME)
    savedPictures = True
    tweetPhotos()
   
def setupTwitter():
    # Read secretKeys
    keyFile = open("secretKeys.txt", "r")
    lines = keyFile.readlines()
    C_key = lines[0].rstrip("\n\r")
    C_secret = lines[1].rstrip("\n\r")
    A_token = lines[2].rstrip("\n\r")
    A_secret = lines[3].rstrip("\n\r")
    keyFile.close()
    
    # auth twitter
    return Twython(C_key,C_secret,A_token,A_secret)
   
def tweetPhotos():
    myTweet = setupTwitter()
    photo = open("images/%s" % SAVED_PHOTO_NAME, 'rb') 
    response = myTweet.upload_media(media=photo)
    myTweet.update_status(status="Raspberry PI Photo Booth\n - I was required to do this for class",
                            media_ids=[response['media_id']])
		
GPIO.setup(GPIO_BUTTON, GPIO.IN)	
GPIO.add_event_detect(GPIO_BUTTON, GPIO.FALLING, callback=startPictures, bouncetime=300)
	
try:
    while(True): 
        if takingPictures and numberOfPictures < NUM_PICTURES:
            if not countDown():
                clockSet = False
                numberOfPictures += 1
        else:
            takingPictures = False
        if numberOfPictures == NUM_PICTURES and not savedPictures:
            savePhotos()
        for i in range(len(digits)):
            for j in range(len(segments)):
                GPIO.output(segments[j], numberMap[clockOutput[i]][j])
            GPIO.output(digits[i], 0)
            time.sleep(0.001)
            GPIO.output(digits[i], 1)

except KeyboardInterrupt: 
    # This code runs on a Keyboard Interrupt <CNTRL>+C
	print('\n\n' + 'Program exited on a Keyboard Interrupt' + '\n') 

# except: 
    # # This code runs on any error
	# print('\n' + 'Errors occurred causing your program to exit' + '\n')

finally: 
    # This code runs on every exit and sets any used GPIO pins to input mode.
	GPIO.cleanup()