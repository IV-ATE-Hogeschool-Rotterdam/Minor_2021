import RPi.GPIO as GPIO
import time

class ACTUONIX:
    
    def __init__(self, A_IA, A_IB, A_IB2, freq):
        self.A_IA = A_IA
        self.A_IB = A_IB
        self.A_IB2 = A_IB2
        self.freq = freq
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.A_IA,GPIO.OUT)                                              
        GPIO.setup(self.A_IB,GPIO.OUT)                                              
        GPIO.setup(self.A_IB2,GPIO.OUT)
        
        #Instellen PWM-pin-----------------------------------------------------------------------------
        
        self.act_pwm = GPIO.PWM(self.A_IA, self.freq)
        self.act_pwm.start(0)
        
    #Koppelen van de stuuractuator (uitschuiven Actuonix)----------------------------------------------
                
    def koppeling(self):
        GPIO.output(self.A_IB, True)
        GPIO.output(self.A_IB2, False)
        self.act_pwm.ChangeDutyCycle(100)
        
    #Ontkoppelen van de stuuractuator (intrekken Actuonix)---------------------------------------------
            
    def ontkoppeling(self):
        GPIO.output(self.A_IB, False)
        GPIO.output(self.A_IB2, True)
        self.act_pwm.ChangeDutyCycle(100)
        
    #Stilzetten Actuonix-------------------------------------------------------------------------------
        
    def uitschakelen(self):
        GPIO.output(self.A_IB, False)
        self.act_pwm.ChangeDutyCycle(0)
            
