
# Binance_Trading_Bot
Trading bot for binance

## Intro and disclaimer

This is not a finished bot. It has missing implementations.

I did it this way to make sure that, whoever wants to use it, understands the code and can manage it. Also, I think it as a starting project for freshmen. 

The bot is built using the binance API, but not websockets. That means that if you wanted to use it, surely within a short time of starting, binance will kick you out of the system.
You will have to do that implementation by yourself.

Also, if you had a power or internet outage while you have an open operation, you will have to create a new sales function to make better use of your resources and re-enter the market.

_(A good solution for this would be to change the market orders to limit orders, and if you suffer from a bug in the bot host, the orders on how to act will already be given beforehand.)
Remember you are investing your money, take all regards)._


## Getting started


You will find 3 files:
- BBking
- Config
- Indicators

**BBking** is the proper bot, **Config** is for basic configurations and **Indicators** is a helpfull tool to create indicators without repeating code. 

## Config file

Here you will find 4 important variables:

**API_KEY:** Here you'll have to paste your api key

**API_SECRET:** Here you'll have to paste your api key

**invest_amount:** This is the money you want to invest in USDT
**min_amount:** This is the smallest amount you can buy on binance


After these, you'll find a consecutive number of **constants** to make easy create **indicators objects**

##### Example:

This is the line to get Candles from binance API</p>


**_klines = client.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_15MINUTE, "15 hour ago UTC")_**



Now you can do it quickly using the **constants**:

**_klines = client.get_historical_klines(symbolTicker, M15, "15"+HOUR)_**

It's just an explanation, we will use it with objects, but will show you in the next file



## Indicators file

Here you'll find a Indicators class, so you could create objets and aproach the methods(functions) to use an indicator.

At time it has 2 indicators to apply a strategy, you could add more.

##### Example:

**_Indicator = Indicators(symbolTicker, M15, 15, HOUR,60, 57, 3)_** 

Now you can call the **_MA_** method to get the indicator (I know, is not a good practice write a function with capital letter, but at time I thought it was better):

**_Indicator.MA()_**

Or maybe a **_trend_**:

**_Indicator.trend()_**

Maybe you are a bit lost with this, just read the code and you'll understand everything

Be free to create your own indicators to apply your strategy, and if you want it, send me a message and I'll add it to the project.

# BBking

## How does it works?

At time, **BB**, is implemented to follow the next strategy:

You pick a pair, bb will take two moving averages (one fast and one slow), then start comparing MAs. When the fast MA is above the slow one, it will make a purchase, then it will sell the asset taking various factors.

- While the asset increases he will take the current price as a reference price and will do a loop untill the price stop growing and will take 2 paths:
  - It will sell when the asset price is "x"% (you can choose it) under the reference price
  - The Asset grows more than "x"% so it sell it to take profit.
-Then it start the cycle again.


**important**

You will find two cases for TP and SL, one if the global trend is increasing and anohter if it's decreasing.

Choose wisely the MAs period and the TP and SL percentages if you gonna use this strategy, remember that price oscilation is different for each asset, and a great formula for an asset could be terrible for another)

**NEVER** run this bot with assets you are stacking. 


Do you want to know more? Watch the code, it has a lot of comments.







