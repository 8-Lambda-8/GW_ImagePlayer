import sys, os
import vlc
import time
from threading import Timer
from pygame import *


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

def servoStop():
    
    print("StopServo")
    if isRaspi:
        servo.ChangeDutyCycle(0)

running = True
last = 0.0
current = 0.0

DEBUG = False

FILES = ["ScreenTest.png",#0
    "1.png",#1 Anna Folder
    "2.png",#2 Steeger Berge
    "3.png",#3 Klostermauern   xx
    "4_1.png",#4 Irland
    "4_2.png",#5 Universitaet
    "5.png",#6 Krieg
    "6_1.png",#7 Schiff
    "6_2.png",#8 Indien
    "6_3.png",#9 Hospital
    "6_a.png",#10 Glaskreutz
    "Frida.mp4",#11 Frida
    "8und9.png",#12 tiroler Berge
    "10_1.png",#13 New york
    "10_2.png",#14 New york
    "10_3.png",#15 New york
    "11.png",#16 Indien Hole Family Hospital
    "12_1.png",#17 Vatikan aussen
    "12_2.png",#18 Vatikan innen
    "kardinaele.mp4",#19
    "14_1.png",#20 steeger berge 
    "14_2.png",#21 steeg kirche
    "15_1.png",#22 lyrics
    "15_2.png",#23 
    "15_3.png",#24 
    "16_1.png",#25 folder
    "16_2.png"#26 folder2

]


Media = [
    
    FILES[0],
    "PP",
    FILES[1],
    FILES[2],    
    #FILES[3],
    FILES[7],#Schiff
    FILES[4],
    FILES[5],
    FILES[6],
#    FILES[6],
    FILES[8],#9
    FILES[9],#10
    FILES[10],
    FILES[11],
    FILES[12],
    #Pause
    "PP",
    FILES[13],#14
    FILES[14],#15
    #FILES[15],
    FILES[8],#Indien
    FILES[16],
    FILES[17],#18
    FILES[18],
    FILES[19],
    FILES[19],
    FILES[19],
    FILES[19],
    FILES[19],
    FILES[19],
    FILES[20],
    FILES[21],
    FILES[22],
    FILES[23],
    FILES[24],
    FILES[25],
    FILES[26]
]


if len(sys.argv)>1:
        if sys.argv[1]=="--DEBUG":
                DEBUG = True


if DEBUG:
    fadeDelay = 0#.000000001
    Delay = 0#.0000001
    print ("DEBUG_MODE")


print ('')
print ('')
print ('!START!')
print ('')

def showImage(pic):
    imageA = image.load('media/'+pic)
    screen.blit(imageA,(0,0))
    display.flip()

#INIT Col
BLACK = ( 0, 0, 0)
WHITE = ( 230, 230, 230)
#END INIT Col


#INIT Pygame

display.init()
infoObject = display.Info()

w = infoObject.current_w
h = infoObject.current_h

if DEBUG:
	w=1280
	h=1024
	screen = display.set_mode((w, h))
else:
	screen = display.set_mode((w, h),FULLSCREEN)

screen.fill(BLACK)

i = 0

ppInt = 0


display.set_caption('GW_ImagePlayer')

mouse.set_pos(w, h)
mouse.set_visible(False)
#END INIT Pygame


#INIT VLC
vlcInstance = vlc.Instance('--mouse-hide-timeout=0')
player = vlcInstance.media_player_new()
player.set_xwindow(display.get_wm_info()['window'])
vlc_media = vlcInstance.media_new("media/kardinaele.mp4")
#END INIT VLC

def startVideo(x):
    if isImage(last):
        vlc_media = vlcInstance.media_new("media/"+x)
        player.set_media(vlc_media)
    player.play()

def stopVideo():
    if isImage(current+0.5):
        player.stop()
    else:
        player.pause()

def isImage(x):
    return not (".mp4" in Media[int(x)])

def PP():
    if current.is_integer() and Media[int(current)] is "PP":
        globals().update(ppInt =  ppInt + 1)
        print(ppInt)
        if ppInt > 85:
            globals().update(ppInt = 1)
        showImage("PP/Folie"+str(ppInt)+".png")
        Timer(14, PP, ()).start()

def Change():
    print("")
    print("Current="+str(current))
    print("Last="+str(last))

    if current.is_integer():
        servoOpen()
        if Media[int(current)] != "PP":
            if isImage(current):
                showImage(Media[int(current)])
            else:
                startVideo(Media[int(current)])
                Timer(0.4, servoStop, ()).start()
        else:
            #start Pause Praesentation
            globals().update(ppInt = 0)
            print("PP")
            PP()
    else:
        if isImage(current+0.5)|isImage(current-0.5):
            servoClose()
        screen.fill(BLACK)
        display.flip()

        if isImage(last):
            print("")
        else:
            stopVideo()
	

def exit():
    globals().update(running = False)
    if isRaspi:
        servoOpen()
        GPIO.cleanup()

    print('\nQuit\n')
    quit()

try:

    Change()
    while running:

        if current <0:
            current = 0

        if current != last:
            Change()
        last = current

        for e in event.get():
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                print(e.key)
                if e.key == K_SPACE or e.key == K_RIGHT:
                    if current == 3 or current == 4 or current == 7 or current == 13 or current == 15 or current == 17 or current == 25 or current == 27 or current == 28 or current == 30:
                        print("is 5")
                        current = current + 1
                    else:
                        current = current + 0.5
                if e.key == K_LEFT:
                    current = current - 0.5
                if e.key == K_ESCAPE:
                    exit()

    time.wait(0)

except (KeyboardInterrupt, SystemExit):
	exit()
