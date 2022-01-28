import can
import cantools
from can.message import Message
import os

class CAN:
    
    #Object voor verwijderen class-------------------------------------------------------------------
    
    def __del__(self):
        pass
    
    def __init__(self):
            
        self.steering_angle_actual = 0
        self.steering_angle_target = 0
        
        os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
        self.bus = can.interface.Bus(channel ='can0', bustype='socketcan_native')
        self.db = cantools.db.load_file('/home/pi/FSG_Data_Logger_data_V1.1.dbc')
        self.stuursys = self.db.get_message_by_name('Stuur_systeem')
    
    #CAN-berichten ontvangen----------------------------------------------------------------------------
    
    def receive(self) -> int:
        message = self.bus.recv(0.0)
        
        if message is None:
            print('Geen data')
            return self.steering_angle_target 
        
        else:
            
            if hex(message.arbitration_id)[2:] == '201':
                message_dc = self.db.decode_message(message.arbitration_id,message.data)
                self.steering_angle_target = message_dc.get('Steering_angle_target')
                print("Target:",self.steering_angle_target)
                return self.steering_angle_target
            
            else:
                print("Onjuist ID")
                return self.steering_angle_target
      
    #CAN-berichten versturen-----------------------------------------------------------------------------------  
      
    def send(self,data1,data2):
        self.data1 = data1
        self.data2 = data2
        
        stuursys_data = self.stuursys.encode({'Steering_angle_actual':self.data1, 'Steering_angle_target':self.data2}) 
        stuursys_msg = can.Message(arbitration_id=self.stuursys.frame_id, data=stuursys_data)
        self.bus.send(stuursys_msg)
        print('Verzonden:',stuursys_msg)
      
    #CAN-bus systeem uitschakelen------------------------------------------------------------------------
      
    def candown(self):
        os.system('sudo ip link set can0 down')
        time.sleep(.1)
        self.bus.shutdown()
        time.sleep(.1)
        print('Bus uit')
     
    