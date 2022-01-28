import RPi.GPIO as GPIO
#import time

class PANASONIC:

    def __init__(self, light_on, dark_on):
        self.light_on = light_on
        self.dark_on = dark_on
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.light_on,GPIO.IN)                                                
        GPIO.setup(self.dark_on,GPIO.IN)
        
    #Meten van de lichtsluissensor----------------------------------------------------------------------
        
    def getLight(self):
        
        #Als de beginstand naar links gestuurd staat----------------------------------------------------
        
        if GPIO.input(self.light_on) == True and GPIO.input(self.dark_on) == False:
            print(True)
            return True
        
        #Als de beginstand naar rechts gestuurd staat---------------------------------------------------
        
        elif GPIO.input(self.dark_on) == True and GPIO.input(self.light_on) == False:
            print(False)
            return False
        
