# Startup (libraries)
import cantools                     # Importeert can library      (CAN)
import can                          # Importeert can library      (CAN)
from can.message import Message     # Importeert can library      (CAN)

import os

os.system("sudo /sbin/ip link set can0 up type can bitrate 500000 # Instellingen voor setup CAN-bus")

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')                           # Maakt de CAN bus aan (type bus en kanaal wordt gedefineerd)
db = cantools.db.load_file('/home/pi/Desktop/RU22_Remsysteem/FSG_Data_Logger_data_V1.1.dbc')  # Laad het .dbc file voor ontcijferen berichten
Aansturing_Remsysteem = db.get_message_by_name('Aansturing_Remsysteem')                       # Ontcijfert de Aansturing_Remsysteem berichten uit het .dbc file
Verzending_Remsysteem = db.get_message_by_name('Verzending_Remsysteem')                       # Ontcijfert de Verzending_Remsysteem berichten uit het .dbc file

def arduino_map(x, in_min, in_max, out_min, out_max): # De meet klasse wordt aangemaakt, in deze klasse wordt het analoge signal omgezet naar digitaal.
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

while True:
    
    # Aansturing Remsysteem bericht
    
    Target_Rempedaal = 100              # Gewenste voertuigsnelheid in km/h
    Systeem_Mode = 2                   # Systeem modus van het autonome systeem 0 = off, 1 = ready, 2 = driving, 3 = emergency brake, 4 = finish
    Service_Mode = 1                   # Service modus van het remsysteem 1 = disengaged, 2 = engaged, 3 = available
    
    # Zelfde proces als Test_berichten (er wordt een bericht aangemaakt en verzonden)
    Aansturing_Remsysteem_data = Aansturing_Remsysteem.encode({'Target_Rempedaal': Target_Rempedaal, 'Systeem_Mode': Systeem_Mode, 'Service_Mode': Service_Mode})
    Aansturing_Remsysteem_bericht = can.Message(arbitration_id = Aansturing_Remsysteem.frame_id, data = Aansturing_Remsysteem_data)
    bus.send(Aansturing_Remsysteem_bericht)    
    
    # Verzending Remsysteem bericht
    
    message = bus.recv()                                             # Berichten van de bus worden verbonden aan parameter 'message'
    message=db.decode_message(message.arbitration_id, message.data)  # De berichten worden gedecodeerd aan de hand van de dbc file
    Verzending_Remsysteem_CR =round(message.get('Current_Rempedaal'))      # Met behulp van het dbc file worden specifieke waardes uit de data gehaald
    Verzending_Remsysteem_OVS=message.get('Overtravel_switch')       # Idem
    
    print(Verzending_Remsysteem_CR, Verzending_Remsysteem_OVS)       # Ontvangen data wordt geprint