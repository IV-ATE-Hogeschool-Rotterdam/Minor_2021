#Imports----------------------------------------------------------------------------------------------
import time
from DOGA_ENCODER_RU22 import HALL
from PID_RU22 import PIDC
from DOGA_RU22 import DOGA
from CAN_RU22 import CAN
from ACTUONIX_RU22 import ACTUONIX
import RPi.GPIO as GPIO
import can
from can.message import Message
import os
from KALIBREREN_RU22 import KALIBREREN

#OntKoppeling------------------------------------------------------------------------------------------
def koppelen():
    actuonix = ACTUONIX(32,36,8,100)                                               
    
    doga = DOGA(33,37,100)
    print('Actuator koppeling, geduld AUB')
    doga.motor_aansturen(5)
    actuonix.koppeling()
    time.sleep(3.5)
    actuonix.uitschakelen()
    doga.motor_aansturen(0)
    print('Actuotor gekoppeld, kalibratie wordt gestart')
    del doga
    del actuonix
    time.sleep(2)

#Kalibreren------------------------------------------------------------------------------------------------

def kalibreren():
    print('Kalibratie wordt gestart')
    time.sleep(1)
    kal.kalibratie()
    print('Kalibratie gereed, startpositie is',kal.getStartPos(),'graden')
    time.sleep(.5)
    print('Autonoom stuursysteem wordt gestart')
    
#Definities--------------------------------------------------------------------------------------------

def GPIO_set():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(switch,GPIO.IN)
    
switch = 38
i = 0
GPIO_set()

#Objecten----------------------------------------------------------------------------------------------
def off():
    actuonix = ACTUONIX(32,36,8,100)
    print("Systeem wordt uigeschakeld"),
    try:
        canb.candown()
    except:
        pass
    try:
        doga.motor_aansturen(0)
    except:
        pass
    actuonix.ontkoppeling()
    time.sleep(3)
    actuonix.uitschakelen()
    del actuonix
    GPIO.cleanup
    #exit()

#Opstart procedure------------------------------------------------------------------------------------
def startup():    
    koppelen()
    kalibreren()
   
#Hoofd loop-------------------------------------------------------------------------------------------   
while True:
    
    #Stand-by loop-------------------------------------------------------------------------------------

    while GPIO.input(switch) == False:
        print('Switch staat uit')
        
        if i == 0:
            off()
            try:
                kal.kalStat = False
            except:
                pass
            try:
                del doga
                del kal
            except:
                pass
            
            try:
                del hall
            except:
                pass
            
            try:
                del canb
            except:
                pass
            
            GPIO.cleanup()
            GPIO_set()
            i += 1
            
        time.sleep(.1)

    #Opstarten--------------------------------------------------------------------------------------------

    else:
        GPIO_set()
        kal = KALIBREREN()
        startup()
        hall = HALL(29,31,kal.getStartPos())
        doga = DOGA(33,37,100)
        canb = CAN()
        pidc = PIDC(5.5,0.2,0,-100,100)
        k = kal.getKalStat()
        i = 0

    #Stuur loop------------------------------------------------------------------------------------------- 
    while GPIO.input(switch) == True and k == True:
        
        target = canb.receive()
        pidc.spcalc(target)
        actual = hall.getAngle()
        pidc.pidexc(actual)
        doga.motor_aansturen(pidc.get_pwm())
        
        print('Verschil:',target-(actual*(32.78/135)))
        
        try:
            canb.send((actual*(32.78/135)),target)
        except:
            print('CAN send ERROR')
        
    else:
        if k == False:
            print('ERROR, geen kalibratie!')
            time.sleep(2)
            


