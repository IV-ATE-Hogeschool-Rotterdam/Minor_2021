import RPi.GPIO as GPIO

class DOGA:
    
    def __del__(self):
        pass
    
    def __init__(self,doga_pwm,doga_dir,freq):
        
        self.doga_PWM = doga_pwm
        self.doga_dir = doga_dir
        self.freq = freq

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.doga_dir,GPIO.OUT)                                                
        GPIO.setup(self.doga_PWM,GPIO.OUT)                                             
        
        #Instellen van de PWM-pin------------------------------------------------------------------------
    
        self.doga_pwm = GPIO.PWM(self.doga_PWM, self.freq)
        self.doga_pwm.start(0)
        
    #Aansturen van de stuuractuator a.d.h.v. ontvangen PWM-----------------------------------------------

    def motor_aansturen(self,pwm):
        self.pwm = pwm
        
        #Linksom-----------------------------------------------------------------------------------------
        
        if self.pwm >= 0:
            GPIO.output(self.doga_dir,True)
            self.doga_pwm.ChangeDutyCycle(self.pwm)
            print('motor draait',self.pwm)
            
        #Rechtsom----------------------------------------------------------------------------------------
                
        elif self.pwm < 0:
            GPIO.output(self.doga_dir,False)
            self.doga_pwm.ChangeDutyCycle(abs(self.pwm))
            print('motor draait')
            
 
            