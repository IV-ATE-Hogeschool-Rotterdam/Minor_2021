# Analoog / Digitaal Converter

import RPi.GPIO                                      # Importeert GPIO library      (RPi)
import busio                                         # Importeert busio library     (adafruit)
import adafruit_ads1x15.ads1015 as ADS               # Importeert ADS library       (adafruit)
from adafruit_ads1x15.analog_in import AnalogIn      # Importeer AnalogIn library   (adafruit)

i2c = busio.I2C(3,2)                # busio.I2C creeert een interface voor de I2C protocol
ads = ADS.ADS1015(i2c)                               # De ADS drive wordt aangegeven welke interface toegepast moet worden
chan1 = AnalogIn(ads, ADS.P0)                        # De toegepaste kanalen op de ADC worden gedefineerd
chan2 = AnalogIn(ads, ADS.P1)                        # De toegepaste kanalen op de ADC worden gedefineerd

class Remdruksensor:                                 # Klasse voor de remdruksensor wordt aangemaakt
    def __init__(self, chan1, chan2):                # De klasse wordt geinitialiseerd
        self.chan1 = chan1                           # Kanaal 1 wordt aangeduid
        self.chan2 = chan2                           # Kanaal 2 wordt aangeduid
        
    def meet(self):                                  # De meet klasse wordt aangemaakt, in deze klasse wordt het analoge signal omgezet naar digitaal.
        meetwaarde = round(chan1.voltage,2),round(chan2.voltage,2),\
             int(chan1.voltage/(chan1.voltage+chan2.voltage)*100), int(chan2.voltage/(chan1.voltage+chan2.voltage)*100)
        return meetwaarde

Signalen_Remdruksensor = Remdruksensor(chan1, chan2)