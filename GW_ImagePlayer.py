import sys, os
import vlc
import sched, time
from datetime import datetime
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
    if isRaspi:
        servo.ChangeDutyCycle(0)

running = True
last = 0.0
current = 0.0

DEBUG = False

FILES = ["ScreenTest.png",#0
    "1.png",#1 Anna Folder
    "2.png",#2 Steeger Berge
    "3.png",#3 Klostermauern
    "4_1.png",#4 Irland
    "4_2.png",#5 Universitaet
    "5.png",#6 Krieg
    "6_1.png",#7 Schiff
    "6_2.png",#8 Indien
    "6_3.png",#9 Hospital
    "6a.png",#10 Glaskreutz
    "Frida.mp4",#11 Frida
    "8und9.png",#12 tiroler Berge
    "10_1.png",#13 New york
    "10_2.png",#14 New york
    "10_3.png",#15 New york
    "11.png",#16 Indien Hole Family Hospital
    "12_1.png",#17 Vatikan aussen
    "12_2.png",#18 Vatikan innen
    "kardinaele.mp4",#19
    "14_1.png",#20
    "14_2.png",#21
    "15.png"#22

]


Media = [
    FILES[0],
    FILES[1],
    FILES[2],
    FILES[3],
    FILES[4],
    FILES[5],
    FILES[6],
    FILES[6],
    FILES[7],
    FILES[8],
    FILES[9],
    FILES[10],
    FILES[11],
    FILES[12],
    FILES[12],
    FILES[13],
    FILES[14],
    FILES[15],
    FILES[16],
    FILES[17],
    FILES[18],
    FILES[19],
    FILES[19],
    FILES[19],
    FILES[19],
    FILES[19],
    FILES[19],
    FILES[20],
    FILES[21],
    FILES[22]
]


if len(sys.argv)>1:
        if sys.argv[1]=="--DEBUG":
                DEBUG = True


fadeDelay = 0#.0000001
Delay = 0#.0001

fadeMultiplier = 8

if DEBUG:
    fadeDelay = 0#.000000001
    Delay = 0#.0000001
    print ("DEBUG_MODE")


print ('')
print ('')
print ('!START!')
print(datetime.now())
print ('')


def showImage(pic):
    imageA = image.load('media/'+pic)
    screen.blit(imageA,(0,0))
    display.flip()


#Fade in pic Function
def fadeInPic(pic):
    #print ()
    imageA = image.load('media/'+pic)


    for i in range (int(254/fadeMultiplier)):

        screen.fill(BLACK)
        imageA.set_alpha(i*fadeMultiplier)
        screen.blit(imageA,(0,0))
        display.flip()
        #time.sleep(fadeDelay)

    display.flip()

#END Fade in pic Function

#Fade in pic Function
def fadeOutPic(pic):

    imageA = image.load('media/'+pic)

    for i in reversed(range (int(254/fadeMultiplier))):

        screen.fill(BLACK)
        imageA.set_alpha(i*fadeMultiplier)
        screen.blit(imageA,(0,0))
        display.flip()
        #time.sleep(fadeDelay)



#END Fade in pic Function

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

#sch = sched.scheduler(time.time, time.sleep)

def startVideo(x):
    vlc_media = vlcInstance.media_new("media/"+x)
    player.set_media(vlc_media)
    player.play()

def stopVideo():

    player.stop()

def isImage(x):
    return not (".mp4" in Media[int(x)])

def Change():
    print("")
    print("Current="+str(current))
    print("Last="+str(last))

    if current.is_integer():
        servoOpen()
        if isImage(current):
            #fadeInPic(Media[int(current)])
            showImage(Media[int(current)])
        else:
            startVideo(Media[int(current)])
    else:
        servoClose()
        screen.fill(BLACK)
        display.flip()

        if isImage(last):
            #fadeOutPic(Media[int(last)])
            print("")
        else:
            stopVideo()

	#sch.enter(5, 1, servoStop())
	#sch.run()

def exit():
    globals().update(running = False)
    #GPIO.cleanup()
    print('\nQuit\n')
    quit()


"""
if current <0:
            current = 0

        if current != last:
            Change()

        last = current"""

try:

    #time.sleep(5000)
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
                print("KEYDOWN")
                print(e.key)
                if e.key == K_SPACE or e.key == K_RIGHT:
                    current = current + 0.5
                    print(current)
                if e.key == K_LEFT:
                    current = current - 0.5
                    print(current)
                if e.key == K_ESCAPE:
                    exit()

    time.wait(0)


except (KeyboardInterrupt, SystemExit):
	exit()
