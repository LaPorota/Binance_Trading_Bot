
from binance.client import Client
from binance.enums import *
import time
import numpy as np
from datetime import datetime
from indicators import *
from config import *




print("")
print("                         :::'########:::::::'########::::::::::'##:::'##:'####:'##::: ##::'######:::")
print("                         ::: ##.... ##:::::: ##.... ##::::::::: ##::'##::. ##:: ###:: ##:'##... ##::")
print("                         ::: ##:::: ##:::::: ##:::: ##::::::::: ##:'##:::: ##:: ####: ##: ##:::..:::")
print("                         ::: ########::::::: ########:::::::::: #####::::: ##:: ## ## ##: ##::'####:")
print("                         ::: ##.... ##:::::: ##.... ##::::::::: ##. ##:::: ##:: ##. ####: ##::: ##::")
print("                         ::: ##:::: ##:'###: ##:::: ##:'###:::: ##:. ##::: ##:: ##:. ###: ##::: ##::")
print("                         ::: ########:: ###: ########:: ###:::: ##::. ##:'####: ##::. ##:. ######:::")
print("                         :::........:::...::........:::...:::::..::::..::....::..::::..:::......::::")


print()
print()
print("B.B. King v2.0 by Pedro Orlando")


### we create next variables as global to declare it without givin them values
global buy_price
global TP
global SL


 
client = Client(API_KEY, API_SECRET, tld='com')

coin = 'SOL'   ### This is the asset you want to trade
symbolTicker = coin+'USDT' ### Here we create the pair to compare
divX = float(client.get_asset_balance(asset=coin)['free']) ### Here it takes the balance in your wallet of the asset you want to trade

###### Now we creates the objects to take each MA. watch I'm using a big number of candles for the range to analyze
######  maybe you want to change ;) 
fastMA = Indicators(symbolTicker, M15, 15, HOUR,60, 57, 3)  
slowMA = Indicators(symbolTicker, M15, 15, HOUR,60, 51, 9)  

### It calculates the global trend, at time it is working with 1 H candles and a range of 6 hours.
### It returns 3 possible solutions: 
#### True: The trend is increasing
#### False: Trend is decreasing
#### error : could not find it
def trend():
	x = []
	y = []
	ma_t = 0

	time.sleep(1)

	resp = False

	klines = client.get_historical_klines(symbolTicker, H1,  "6"+HOUR)

	if (len(klines) != 6):
		resp = 'error'
	for i in range(1,6):
		for j in range(i-5,i):
			ma_t += float(klines[j][4])
		ma_t = round(ma_t / 6, 7)
		
		x.append(i)
		y.append(float(ma_t))

	modelo = np.polyfit(x, y, 1)

	if (modelo[0]>0):
		resp = True

	return resp

### As it say, takes the current price of the pair.
def current_price():
	return float(client.get_symbol_ticker(symbol=symbolTicker) ['price'])


def sell():
	### we call the global variables to use and rewrite them
	global client
	global divX
	global buy_price
	global TP
	global SL
  
	sleep = 0
	trend_side= ''
	### Here takes the price we bought the asset
	buy_price = float(client.get_my_trades(symbol=symbolTicker, limit=1)[0]['price'])
	
	### Here it takes the trend and validate it, Here you choice your TP and SL

	while trend_side == '':
		if trend() == True:
			TP= 1.03
			SL= 0.99
			##After a sell the fast MA will be over the slow MA, to don't buy again with a decreasing price, we make BB sleep 
			## sleep time depends on the asset oscilation so be carefull about it
			sleep = 1200
			trend_side = 'Increasing'

		elif trend() == False:
			TP= 1.0175
			SL= 0.995
			sleep =1200
			trend_side = 'Decreasing'
			
		
		else:
			time.sleep(3)
		
	### Now prints the status of all we care
	print(symbolTicker.center(50, "-"))
	print(f"Actual price: {current_price()}")
	print(f'Fast MA: {fastMA.MA()}')   
	print(f'Slow MA: {slowMA.MA()}')
	print(f'Trend: {trend_side}')
	print(f'Waiting for sell it for: {float(buy_price) *TP} on winning, or for: {float(buy_price)*SL}  on lossing.') 
	
	#now assign the buy price to the reference price
	reference_price= buy_price

	loop_validator = 7

	while loop_validator == 7 :
		
		if float(current_price()) == 0:
			time.sleep(3)
		
		#Here it rewrite the reference_price variable to update it to the current price
		elif current_price() > reference_price:
			reference_price = current_price()
			print(f"New reference price: {current_price()}")
			time.sleep(5)

		#when asset price stop growing will analize if it growed untill reach the TP we want
		elif current_price() >= buy_price * TP:
			print('[+]selling...')
	
			try:            
				## here it creates the order
				order = client.create_order(symbol=symbolTicker, side='SELL', type='MARKET', quantity=divX)

				print(f'[+]Sold {divX} {coin} for {current_price()}')
				divX = 0
				
				result = (current_price() / buy_price) -1
				percentage= str(round(result,2))

				final_percentage = percentage.split('.')
				
				print(f"[+]We've won a {final_percentage[1]} %")
				print('Entering sleep state...')
				loop_validator= 8
				
				time.sleep(int(sleep))    
			except:
				print("[-]Trying to sell it again")
				time.sleep(1)    
	
		#when asset price stop growing and start to decrease will sell it on a % unther the reference price
		elif current_price() <= reference_price * SL: 
			print('[+]selling...')
	
			try:            
				
				order = client.create_order(symbol=symbolTicker, side='SELL', type='MARKET', quantity=divX)

				print(f'[+]Sold {divX} {coin} for: {current_price()}')
				divX = 0
				
				result = current_price() / reference_price -1
				percentage = str(round(result,2))
				print(f"[+]We have lost a {percentage} % of the investment amount")
				
				loop_validator = 9
				
				print('Entering sleep state...')
				time.sleep(int(sleep))    
			except:
				print("[-]Trying to sell it again")
				time.sleep(1)
		
		else:
			time.sleep(5)

#### We already talked about send bb to sleep after a sell, 
#### so what happen if he wakes up and fast MA is still over the slow one or is in the middle of a new operation?
#### it takes the las two candles and verify if the price is decreasing and goes sleep again
def buy_validator():
    
	values=np.array([])
    
	klines = client.get_historical_klines(symbolTicker, M15, "30"+MINUTES)
	if (len(klines) == 2):
            
		for i in range(0, 2):
			values = np.append(values,float(klines[i][4]))
		
        
		if values[0] > values[1]:
			short_trend_validator=False
		elif values [0] < values[1]:
			short_trend_validator= True
		else:
			time.sleep(60)
	
	return short_trend_validator		


def buy():
	global client
	global divX
	global buy_price

	
	
	if slowMA.MA() == 0 or fastMA.MA() == 0:
		time.sleep(3) 


	elif fastMA.MA() > slowMA.MA() and buy_validator() == True:
		info = client.get_symbol_info(symbol=symbolTicker)
		lotSize = float([i for i in info['filters'] if i['filterType'] == 'LOT_SIZE'] [0] ['minQty'])
		buy_quantity = round(float(invest_amount)/current_price(), len(str(lotSize).split('.')[1]))         
			
          
		try:        
					  
			order = client.create_order(symbol=symbolTicker, side='BUY', type='MARKET', quantity=buy_quantity)
			
		
			data=order['fills']
			
			
			buy_price=float(data[0]['price'])
			
			divX = float(client.get_asset_balance(asset=coin)['free'])
		
			
			print(f'[+]Bought {divX} {coin} for {buy_price}')
		
			
			time.sleep(30)         
			
		except:
			client = Client(API_KEY, API_SECRET, tld='com')
			print('[-]Trying to buy again, verify that you have the intended balance.') 
			time.sleep(3)  
		
		
	else:
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		print(f'Fast MA: {fastMA.MA()}')   
		print(f'Slow MA: {slowMA.MA()}')   
		print(f'The fast MA is under the slow MA. Time: {current_time}')
		time.sleep(60)



################################################################ Execution #####################################################################

if __name__ == "__main__":

	### first it see if you have more than the smallest amount binance lets you buy in your wallet
	### It's because if the host goes down when you're on a sellig, after reconnect you will keep with the selling.
	if current_price() * divX > min_amount:
		while divX > 0:
			sell()
	

	### If you have no assets on your wallet you will be ready to buy, but whats app if you run BB and you lost the enteracce point?
	### Start an operation after the entrance point is a bad idea, you could get in to late.
	### So if BB finds he start runing during an possible operation he will let it pass and will sleep 'till 
	### find the slow Ma over the Fast one.
	
	while fastMA.MA() > slowMA.MA():
		print('[+]Waiting to find conditions to enter')
		time.sleep(900)

    
	print('[+]B.B. enters the market')

    ###And now, the circle of life 
	while 1:
		if current_price() * divX < min_amount:
			buy()
		else:
			sell()



