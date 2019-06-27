import pygame, sys, os
import vlc, random
import time, threading
from datetime import datetime


isRaspi = False
if os.uname()[4][:3]=='arm':
    isRaspi = True
    import RPi.GPIO as GPIO
    GPIO.cleanup()
    servoPIN = 2
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    servo = GPIO.PWM(servoPIN, 50) # GPIO 8 als PWM mit 50Hz
    servo.start(3) # Initialisierung

def servoOpen():
    if isRaspi:
        servo.ChangeDutyCycle(3)
def servoClose():
    if isRaspi:
        servo.ChangeDutyCycle(11)

running = True
last = 0.0
current = 0.0

DEBUG = False


FILES = ["ScreenTest.png",
    "AnnaFolder.jpg",#Anna Folder
    "SteegerBerge.jpg",#Steeger Berge
    "Klostermauern.jpg",#Klostermauern
    "Irland.jpg",#Irland
    "Universitaet.jpg",#Universitaet
    "Krieg.jpg",#Krieg
    "Schiff.jpg",#Schiff
    "Schiff.jpg",#Indien
    "Schiff.jpg",#Hospital
    "Glaskreuz.jpg",#Glaskreuz
    "FilmAnna1.mp4",#Film Anna 1 (Frida)
    "BergeTirol.jpg",#Berge Tirol
    "NewYork.jpg",#New york
    "Indien_HFH.jpg",#Indien Hole Family Hospital
    "VatikanAussen.jpg",#Vatikan aussen
    "VatikanInnen.jpg",#Vatikan innen
    "kardinaele.jpg",#kardinaele
    "SteegBerg.jpg",
    "SteegKirche.jpg",
    "SteegBerg.jpg",
    "LiedText.mp4",

]

Media = [
    FILES[0],
    FILES[1],
    FILES[2],
    FILES[3],
    FILES[2],
    FILES[2],
    FILES[3]
]



if len(sys.argv)>1:
        if sys.argv[1]=="--DEBUG":
                DEBUG = True



fadeDelay = 0#.0000001
Delay = 0#.0001

fadeMultiplier = 4

if DEBUG:
    fadeDelay = 0#.000000001
    Delay = 0#.0000001
    print ("DEBUG_MODE")


print ('')
print ('')
print ('!START!')
print(datetime.now())
print ('')


#Fade in pic Function
def fadeInPic(pic):
    #print ()
    image = pygame.image.load('media/'+pic)
    imageA = image

    for i in range (int(254/fadeMultiplier)):
        
        screen.fill(BLACK)		
        imageA.set_alpha(i*fadeMultiplier)
        screen.blit(imageA,(0,0))
        pygame.display.flip()		
        time.sleep(fadeDelay)
        
    pygame.display.flip()

#END Fade in pic Function

#Fade in pic Function
def fadeOutPic(pic):

    image = pygame.image.load('media/'+pic)
    imageA = image

    for i in reversed(range (int(254/fadeMultiplier))):
		
        screen.fill(BLACK)
        imageA.set_alpha(i*fadeMultiplier)
        screen.blit(imageA,(0,0))
        pygame.display.flip()		
        time.sleep(fadeDelay)



#END Fade in pic Function

#INIT Col
BLACK = ( 0, 0, 0)
WHITE = ( 230, 230, 230)
#END INIT Col


#INIT Pygame

pygame.display.init()
infoObject = pygame.display.Info()


w = infoObject.current_w
h = infoObject.current_h

if DEBUG:
	w=1280
	h=1024


if DEBUG:
	screen = pygame.display.set_mode((w, h))
else:
	screen = pygame.display.set_mode((w, h),pygame.FULLSCREEN)
	
screen.fill(BLACK)

i = 0

pygame.display.set_caption('GW_ImagePlayer')

pygame.mouse.set_pos(w, h)
pygame.mouse.set_visible(False)
#END INIT Pygame


#INIT VLC
#vlcInstance = vlc.Instance('--mouse-hide-timeout=0')
#player = vlcInstanceTimelapse.media_player_new()
#END INIT VLC

#player.set_media()

def isImage(x):  
    return not (".mp4" in Media[int(x)])
      
def Change():
    print("")
    print("Current="+str(current))
    print("Last="+str(last))
    
    if current.is_integer():
        servoOpen()
        if isImage(current):
            fadeInPic(Media[int(current)])
        #else:
            
    else:
        servoClose()
        if isImage(last):
            fadeOutPic(Media[int(last)])
        


def exit():
    globals().update(running = False)
    #GPIO.cleanup()
    print('\nQuit\n')
    pygame.quit()

try:
            
    #time.sleep(5000)
    Change()
    while running:
        if current <0:
            current = 0
        
        if current != last:
            Change()

        last = current

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                print("KEYDOWN")
                if event.key == pygame.K_SPACE:
                    print("Space")
                    
                    current = current + 0.5
                    print(current)
                if event.key == pygame.K_LEFT:
                    print("K_LEFT")
                    
                    current = current - 0.5
                    print(current)
                if event.key == pygame.K_RIGHT:
                    print("K_RIGHT")
                    
                    current = current + 0.5
                    print(current)
                if event.key == pygame.K_ESCAPE:
                    print("ESC")
                    exit()

        

except (KeyboardInterrupt, SystemExit):
	exit()