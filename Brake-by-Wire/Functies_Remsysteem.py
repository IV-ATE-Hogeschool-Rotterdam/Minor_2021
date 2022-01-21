import RPi.GPIO                                      # Importeert GPIO library      (RPI)
import keyboard                                      # Importeert keyboard library  (RPi)
import digitalio                                     # Importeert digitalio library (adafruit)
from gpiozero import InputDevice

import busio                                         # Importeert busio library     (adafruit)
import adafruit_ads1x15.ads1015 as ADS               # Importeert ADS library       (adafruit)
from adafruit_ads1x15.analog_in import AnalogIn      # Importeer AnalogIn library   (adafruit)

# Arduino Map Functie

def arduino_map(x, in_min, in_max, out_min, out_max):#Maakt de Arduino map() functie na voor het verwerken van analoge signalen                          
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Over-travel switch functie

Pin1 = InputDevice(16)
Pin2 = InputDevice(20)
Schakelaarstand = 0

class Remdruksensor:
    def __init__(self):
        self.i2c = busio.I2C(3,2)
        self.ads = ADS.ADS1015(self.i2c)
        self.chan1 = AnalogIn(self.ads,ADS.P0)
        self.chan2 = AnalogIn(self.ads,ADS.P1)
    
    def Meting(self):
        self.Remdruk_Voor = (self.chan1.voltage)
        self.Remdruk_Achter = (self.chan2.voltage)     
        print(round(self.Remdruk_Voor,2),round(self.Remdruk_Achter,2))
        return self.Remdruk_Voor, self.Remdruk_Achter

class Over_travel_switch:
    def __init__(self):
        self.Pin1_value = True
        self.Pin2_value = False
        self.Schakelaarstand = Schakelaarstand
                        
    def Positie_meting(self):
        self.Pin1_value = Pin1.value
        self.Pin2_value = Pin2.value
        
        if Pin1.value == False and Pin2.value == True:
            self.Schakelaarstand = 0
            return self.Schakelaarstand
            
        elif Pin1.value == True and Pin2.value == False:
            self.Schakelaarstand = 1
            return self.Schakelaarstand

# Keyboard functies

class Keyboard:                                  # Klasse voor het toetsenbord wordt aangemaakt 
    def __init__ (self):                         # De klasse wordt geinitialiseerd                             
        self.block = True                        # De block parameter wordt op True gezet 
        self.display = True                      # De display parameter wordt op True gezet 
#         self.dir1 = digitalio.DigitalInOut(37)             # Pin 26 wordt aangeduid als een digitale In-/Output
#         self.dir2 = digitalio.DigitalInOut(18)             # Pin 24 wordt aangeduid als een digitale In-/Output
#         self.dir1.direction = digitalio.Direction.OUTPUT          # Pin 26 wordt als Output gedefineerd 
#         self.dir2.direction = digitalio.Direction.OUTPUT          # Pin 24 wordt als Output gedefineerd   
        
    def motor_uit(self,PWM):                     # De motor_uit functie wordt aangemaakt, hierin wordt de DC op 0 gezet en wordt er motor uit geprint 
        PWM.duty_cycle = 0                       # in de terminal  
        #print("Motor Uit")       
#         self.dir1.value = True                        # De richting van de motor wordt vastgesteld als 1 = True en 2 False is de richting rechtsom 
#         self.dir2.value = False       
        
    def motor_aan(self,PWM):                     # De motor aan functie wordt aangemaakt, hierin wordt de DC op 65535 gezet (maximale waarde) en wordt er
        PWM.duty_cycle = 65535                   # in de terminal aangegeven dat de motor geactiveerd is.
        #print("Motor Aan")        
#         self.dir1.value = True
#         self.dir2.value = False
#         
    def Toggle_k(self):
        if keyboard.is_pressed("k"):             # Wanneer toets k ingedrukt open loop      
            if self.block == False:              # Wanneer waarde block gelijk is aan False open loop
                self.display = not self.display  # De waarde van Display wordt omgedraaid True -> False en andersom  dit is belangrijk voor de onderstaande IF loop
                self.block = True                # Waarde van Block wordt True zodat loop niet opnieuw opend
        else: 
            self.block = False                   # Block wordt terug op False gezet
        return self.display