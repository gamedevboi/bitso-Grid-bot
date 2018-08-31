# bitso-Grid (Gridso)
A bot that buys and Sell bitcoin, eth, xrp, ltc or any cryptocurrency available for the Mexican Exchange Bitso using a Grid strategy through the Bitso API

## Bitso uses Python 2.7 

## Instructions

First install the bitso library using pip install bitso-py
Run the script

your gonna be asked for the grid size, the distance between buy orders, the distance between sell orders, the pair you want to trade i.e. 'xrp_mxn', 'btc_mxn', etc, and the quantity of currency you're going to buy/sell each time. 

### Important

It's recommended for you to have some currency in the pair, for example if you're trading mxn_btc I recommend you have both mxn and btc so you can buffer the movements, remember this is a high volatility market. If the market moves and you don't have enough btc to buy or sell when the order is executed, the bot will stop.

 The script ask you things in spanish right now only because the exchange is from México. I'll add english if asked.
 
 for more info on bitso API go to https://bitso.com/api_info?
 
 ### Disclaimer
Trading Crypto can be a challenging and potentially profitable opportunity for investors. However, before deciding to participate in the crypto market, you should carefully consider your investment objectives, level of experience, and risk appetite. Most importantly, do not invest money you cannot afford to lose. I have not personally tested this bot for a long period of time and I don't know how profitable is. Trade responsibly! :) 
