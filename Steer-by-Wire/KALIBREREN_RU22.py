from PM45Y_RU22 import PANASONIC
import time
from DOGA_RU22 import DOGA
import RPi.GPIO as GPIO

class KALIBREREN:
    
    def __del__(self):
        pass
    
    def __init__(self):
        self.panasonic = PANASONIC(16,35)
        self.kalstat = False
        self.pos = self.panasonic.getLight()
    
    #Kalibratie-proces loop-------------------------------------------------------------------------------
    
    def kalibratie(self):
        doga = DOGA(33,37,100)
        
        while self.kalstat == False:
       
            #Rechtsom sturen wanneer beginstand naar links gestuurd staat--------------------------------
               
            if self.pos == True: 
                doga.motor_aansturen(-8)
               
                if self.panasonic.getLight() == False:
                    doga.motor_aansturen(0)
                    self.kalstat = True
                    
            #Linksom sturen wanneer beginstand naar rechts gestuurd staat--------------------------------
            
            if self.pos == False:
                doga.motor_aansturen(8)
                
                if self.panasonic.getLight() == True:
                    doga.motor_aansturen(0)
                    self.kalstat = True
                    
            
            time.sleep(.1)
            
    #Bepalen van de beginstand stuurhoek----------------------------------------------------------------
        
    def getStartPos(self):
        
        if self.pos == True:
            angleIN = -0.79
            print(angleIN)
            return angleIN
        
        if self.pos == False:
            angleIN = -1.40
            print(angleIN)
            return angleIN
    
    #Opvragen kalibratie status-------------------------------------------------------------------------
        
    def getKalStat(self):
        return self.kalstat
                 
            