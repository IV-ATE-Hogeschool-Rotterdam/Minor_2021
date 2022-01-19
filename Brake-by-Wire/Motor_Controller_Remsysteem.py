from encoder import Encoder
import RPi.GPIO as GPIO
from simple_pid import PID

import Functies_Remsysteem

class Huidige_Hoek:
    def __init__(self):
        self.angle = 0
        
class Hall:
    
    def __init__(self,A,B):
        self.A = A
        self.B = B
        #self.angle = 0
        self.e1 = Encoder(self.A,self.B)

    def Hoek_meting(self,Huidige_Hoek):      
        Huidige_Hoek.angle = round(Functies_Remsysteem.arduino_map(self.e1.getValue(),0,1000,0,100))
        return Huidige_Hoek
       
class PIDC:
    
    def __init__(self,p,i,d,ll,ul):
        self.p = p
        self.i = i
        self.d = d
        self.ll = ll
        self.ul = ul
        self.sp = 0
        self.pwm = 0
    
    def spcalc(self,gw):
        self.gw = gw
        self.sp = self.gw
        self.pid = PID(self.p,self.i,self.d,setpoint = self.sp)
        self.pid.output_limits = (self.ll,self.ul)
        return self.sp

    def pidexc(self, Huidige_Hoek):
        self.a = Huidige_Hoek.angle
        self.pwm = self.pid(self.a)
        print(self.a)
        return self.a, self.pwm

    def get_pwm(self):
        return self.pwm

class DOGA:
    
    def __init__(self,doga_pwm,doga_dir,freq):     
        self.doga_PWM = doga_pwm
        self.doga_dir = doga_dir
        self.freq = freq
        GPIO.setup(self.doga_dir,GPIO.OUT)                                              
        GPIO.setup(self.doga_PWM,GPIO.OUT)                                              
        self.doga_pwm = GPIO.PWM(self.doga_PWM, self.freq)
        self.doga_pwm.start(0)

    def motor_aansturen(self,PIDC):
        self.pwm = PIDC.pwm
        
        if self.pwm >= 0:
            GPIO.output(self.doga_dir,True)
            self.doga_pwm.ChangeDutyCycle(self.pwm)
                
        elif self.pwm < 0:
            GPIO.output(self.doga_dir,False)
            self.doga_pwm.ChangeDutyCycle(abs(self.pwm))
        