# Startup (libraries)
#import pulseio               # Importeert de library voor de motor aansturing (PWM signalen)
import RPi.GPIO as GPIO            # Importeert de library voor de motor aansturing (pin aanduiding)

import Functies_Remsysteem   # Importeert de overige functies voor het remsysteem script
import CANbus_Remsysteem     # Importeert de CAN bus library waarin de CAN berichten van het remsysteem verwerkt worden

import Motor_Controller_Remsysteem 

import os                    # Importeert Operating System library (OS)

os.system("sudo /sbin/ip link set can0 up type can bitrate 500000") # Instellingen voor setup CAN-bus
eigen_keyboard = Functies_Remsysteem.Keyboard()
CAN_bus = CANbus_Remsysteem.CAN()
Ontvangen_data = CANbus_Remsysteem.Ontvangen_Parameters()
HALL = Motor_Controller_Remsysteem.Hall(23,27)    # 16,13 voor BOARD layout
PID = Motor_Controller_Remsysteem.PIDC(1,0,0,-100,100)
Motor = Motor_Controller_Remsysteem.DOGA(12,26,500) # 33, 18 voor BOARD layout
Current_Rempositie = Motor_Controller_Remsysteem.Huidige_Hoek()

while True:
        
#     if eigen_keyboard.Toggle_k() :                            # wordt zal de code in deze klasse geactiveerd worden (en zal de motor in/uitgeschakeld worden) 
#         eigen_keyboard.motor_uit(pulseio.PWMOut(32))   # Als Display True is opend deze loop
#     else:                                                     # Als Display False is opend deze loop
#         eigen_keyboard.motor_aan(pulseio.PWMOut(32))

    CAN_bus.Verzenden(Current_Rempositie)                                   # De Remdruksensoren data wordt uitgezonden   
    Ontvangen_data = CAN_bus.Ontvangen(Ontvangen_data)                                   # Data vanuit de CAN bus wordt ontvangen
    
    HALL.Hoek_meting(Current_Rempositie)
    
    PID.spcalc(Ontvangen_data.Target_Rempedaal)
    PID.pidexc(Current_Rempositie)
    PID.get_pwm()
    Motor.motor_aansturen(PID)
  
    if Ontvangen_data.Service_Mode == 1 or Ontvangen_data.Service_Mode == 3:
        #print('Service_Mode 1 of 3')
        # Geen Actie
        pass
    
    elif Ontvangen_data.Service_Mode == 2:
        #print('Service_Mode 2')
        # Pedaal stand naar 0 %
        pass
    
    if Ontvangen_data.Systeem_Mode == 1 or Ontvangen_data.Systeem_Mode == 4:
        #print('Systeem_Mode 1 of 4')
        # Pedaalstand naar 0
        pass

    elif Ontvangen_data.Systeem_Mode == 2 or Ontvangen_data.Systeem_Mode == 5:
        #print('Systeem_Mode 2 of 5')
        # Pedaalstand naar 100
        pass
    
    elif Ontvangen_data.Systeem_Mode == 3:
        #print('Systeem_Mode 3')
        # Pedaalstand Dynamisch
        pass