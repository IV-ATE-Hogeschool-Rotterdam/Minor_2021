from simple_pid import PID


class PIDC:
    
    def __init__(self,p,i,d,ll,ul):
        self.p = p
        self.i = i
        self.d = d
        self.ll = ll
        self.ul = ul
        self.sp = 0
        self.pwm = 0
        
    #Setpoint berekenene a.d.h.v. gewenste stuurhoek-----------------------------------------------------
    
    def spcalc(self,gw):
        self.gw = gw
        
        #Omrekenen gewenste stuurhoek wielen naar stuurhoek motor----------------------------------------
        
        self.sp = ((360/972) * round((float(self.gw)/(32.09/132.16))/(360/972)))

        #Maximum instellen-------------------------------------------------------------------------------

        if self.sp > 132.16:
            self.sp = ((360/972) * round((32.09)/(32.09/132.16)/(360/972)))
        
        #PID instellen-----------------------------------------------------------------------------------
        
        self.pid = PID(self.p,self.i,self.d,setpoint = self.sp)
        self.pid.output_limits = (self.ll,self.ul)
        print('Setpoint:',self.sp)
        
    #Setpoint opvragen-----------------------------------------------------------------------------------
        
    def get_sp(self):
        return self.sp
    
    #PID controller uitvoeren----------------------------------------------------------------------------
    
    def pidexc(self,a):
        self.a = a
        self.pwm = -self.pid(a)
        print((self.a*(32.09/132.16)),self.pwm)

    #Berkend PWM opvragen--------------------------------------------------------------------------------
    
    def get_pwm(self):
        return self.pwm