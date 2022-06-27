from config import *
from binance.client import Client
from binance.enums import *
import time
import numpy as np


class Indicators():
    
    client = Client(API_KEY, API_SECRET, tld='com')

    

    def __init__(self, symbolticker, interval,time_quantity, timer ,candle_quantity, range_init,period):
        self.symbolTicker = symbolticker
        self.interval= interval
        self.time_quantity = time_quantity
        self.candle_quantity = candle_quantity
        self.range_init = range_init
        self.period = period
        self.timer = timer

    def __str__(self) :
        return f'Pair: {self.symbolTicker} Candle interval: {self.interval} from last {self.time_quantity}  hours, Candle quantity to take: {self.candle_quantity}, analayzing from {self.range_init} candle till {(self.candle_quantity) -1} inclusive, periods: {self.period}'





############################################## MMA ####################################
#  3 PERIODS MMA EXAMPLE:    
#    def MMA():
#	    client = Client(API_KEY, API_SECRET, tld='com')
#       ma = 0
#	    
#
#	    klines = client.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_15MINUTE, "15 hour ago UTC")
#
#        if (len(klines) == 60):
#
#            for i in range(57, 60):
#                ma += float(klines[i][4])
#
#            ma = round(ma / 3,3)
#
#        return ma  
#
####################################################################################################

    def MA(self):
        client = Client(API_KEY, API_SECRET, tld='com')
        ma = 0

        klines = client.get_historical_klines(self.symbolTicker, self.interval, f"{self.time_quantity} {self.timer}")

        if (len(klines) == self.candle_quantity):

            for i in range(self.range_init, self.candle_quantity):
                ma += float(klines[i][4])

            ma = round(ma / self.period,3)

        return ma


############################################### Trend #######################################################    
#  
# 
#2 periods trend Example:
#
#    def tendencia():
#        client = Client(API_KEY, API_SECRET, tld='com')
#        valores=[]
#        klines = client.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_15MINUTE, "30 min ago")
#        if (len(klines) == 2):
#
#            for i in range(0, 2):
#                valores.append(float(klines[i][4]))
#            print(valores)
#            if valores[0] > valores[1]:
#                tendencia=False
#            elif valores [0] < valores[1]:
#                tendencia= True
#            else:
#                time.sleep(60)
#        
#        return tendencia		
# 
# 
# SER PRECISOS EN la CANTIDAD DE VELAS SEGUN EL PERIODO.
################################################################################################################

    
    def trend(self):
        client = Client(API_KEY, API_SECRET, tld='com')
        values=np.array([])
        klines = client.get_historical_klines(self.symbolTicker, self.interval, f"{self.time_quantity} {self.timer}")
        if (len(klines) == self.candle_quantity):

            for i in range(self.range_init, self.candle_quantity):
                values = np.append(values, float(klines[i][4]))
            print(values)
            if values[0] > values[len(values) -1]:
                trend=False
            elif values [0] < values[len(values) -1]:
                trend= True
            else:
                time.sleep(60)
        
        return trend	




