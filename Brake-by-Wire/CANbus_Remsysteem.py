import can                                           # Importeert can library       (CAN)
import cantools                                      # Importeert can library       (CAN)
from can.message import Message                      # Importeert can library       (CAN)

import Functies_Remsysteem                           # Importeert de overige functies voor het remsysteem script
import ADC_Remsysteem                                # Importeert de functies voor de ADC 
import Motor_Controller_Remsysteem                   # Importeert de motor_ Controller Module

Over_Travel_switch = Functies_Remsysteem.Over_travel_switch()
Huidige_Positie = Motor_Controller_Remsysteem.Huidige_Hoek()

class Ontvangen_Parameters:
    def __init__(self):
        self.Service_Mode = 1
        self.Systeem_Mode = 1
        self.Target_Rempedaal = 0

class CAN:                                                                                # Maakt de CAN klasse aan
    
    def __init__(self):
        self.bus = can.interface.Bus(channel='can0', bustype='socketcan_native')                           # Maakt de CAN bus aan (type bus en kanaal wordt gedefineerd)
        self.db = cantools.db.load_file('/home/pi/Desktop/RU22_Remsysteem/FSG_Data_Logger_data_V1.1.dbc')  # Laad het .dbc file voor ontcijferen berichten
        self.Verzending_Remsysteem = self.db.get_message_by_name('Verzending_Remsysteem')                  # Ontcijfert de Verzending_Remsysteem uit het .dbc file
        self.Aansturing_Remsysteem = self.db.get_message_by_name('Aansturing_Remsysteem')                  # Ontcijfert de Aansturing_Remsysteem berichten uit het .dbc file            
          
    def Verzenden(self, Huidige_Positie):                                                      # De data voor de remdruksensoren
        Verzenden_Remsysteem = self.db.get_message_by_name('Verzending_Remsysteem')            # Ontcijfert de Test_berichten uit het .dbc file
        Verzenden_Remsysteem_CR = Huidige_Positie.angle                                        # Parameter voor de data Current_Rempedaal wordt aangemaakt                                 
        Over_Travel_switch.Positie_meting() 
        Verzenden_Remsysteem_OVS = Over_Travel_switch.Schakelaarstand # Parameter voor de data Overtravel_switch wordt aangemaakt
        Verzenden_Remsysteem_data = Verzenden_Remsysteem.encode({'Current_Rempedaal':Verzenden_Remsysteem_CR, 'Overtravel_switch':Verzenden_Remsysteem_OVS}) # Er wordt aangegeven welke data bij welke aangegeven .dbc waarde hoort            
        Verzenden_Remsysteem_bericht=can.Message(arbitration_id=Verzenden_Remsysteem.frame_id, data=Verzenden_Remsysteem_data) # Het CAN bericht wordt opgesteld
        self.bus.send(Verzenden_Remsysteem_bericht)                                            # Het bericht wordt over de bus verzonden

    def Ontvangen(self, Ontvangen_Parameters):                                                         # Het ontvangen en verwerken van data over de CAN bus
        message = self.bus.recv()                                                     # Berichten van de bus worden verbonden aan parameter message
        
        if message.arbitration_id == 512:                                      # Leest het bericht uit als deze een ID heeft van 514
             message514 = self.db.decode_message(message.arbitration_id, message.data) # Ontcijfert de data afkomstig uit bericht 'message'                         
             Ontvangen_Parameters.Target_Rempedaal = round(message514.get('Target_Rempedaal'))                  # De data wordt uitgelezen op basis van de verbonden waardes in het .dbc file
             Ontvangen_Parameters.Systeem_Mode = message514.get('Systeem_Mode')
             Ontvangen_Parameters.Service_Mode = message514.get('Service_Mode')            
             print(Ontvangen_Parameters.Target_Rempedaal, Ontvangen_Parameters.Systeem_Mode, Ontvangen_Parameters.Service_Mode) 
             #print(message514)
            
#         elif message.arbitration_id == 514:                                      # Leest het bericht uit als deze een ID heeft van 514
#             message514 = self.db.decode_message(message.arbitration_id, message.data) # Ontcijfert de data afkomstig uit bericht 'message'                         
#             Target_Rempedaal = message514.get('Target_Rempedaal')                  # De data wordt uitgelezen op basis van de verbonden waardes in het .dbc file
#             Systeem_Mode = message514.get('Systeem_Mode')
#             Service_Mode = message514.get('Service_Mode')
#                           
#             print(Target_Rempedaal, Systeem_Mode, Service_Mode) 
#             #print(message514)      
                           
        else:                                                                    # Overige berichten worden niet gelezen, momenteel aangegeven met print functie
            print("Overige berichten")
            
        return Ontvangen_Parameters