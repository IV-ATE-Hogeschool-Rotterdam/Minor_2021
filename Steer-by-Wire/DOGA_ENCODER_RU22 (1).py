from encoder import Encoder
import time
class HALL:
    
    def __del__(self):
        pass
    
    def __init__(self,A,B,angleIN):
        self.A = A
        self.B = B
        self.angle = 0
        self.angleIN = angleIN
        self.e1 = Encoder(self.A,self.B)
      
    #Berekenen huidige hoekverdraaiing van de motor-----------------------------------------------------  
    
    def getAngle(self):
        self.angle = self.e1.getValue() * (360/972) + self.angleIN
        return self.angle


    