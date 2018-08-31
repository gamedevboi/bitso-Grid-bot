# -*- coding: cp1252 -*-
#Gridso bot for grid trading v.1.0.1
#1.0.1 Update Notes: *Added first sell limit when starting the bot

import bitso
import time
api = bitso.Api('your public key','your private key')
starttime = time.time()


#Tomar valor de la moneda una vez
def start_ticker(crypto):
    tick = api.ticker(crypto)
    return tick
    

#Pone una orden limit-Long
def long_limit(quantity_crypto,price_to_long,crypto):
    order = api.place_order(book=crypto, side='buy', order_type='limit', major= quantity_crypto, price=price_to_long)
#Orden limit-short
def short_limit(quantity_crypto, price_to_short,crypto):
        order = api.place_order(book=crypto, side='sell', order_type='limit', major= quantity_crypto, price= price_to_short)

#Nos da la informacion de la moneda cada segundo
def ticker_by_seconds():
    btc= 'btc_mxn'
    starttime = time.time()
    while True:
        tick = start_ticker(btc)
        print tick
        time.sleep(1.0 - ((time.time() - starttime)  % 1.0))

#separa los buys, returns only buys
def get_buys(moneda):
    buy_orders = []
    oo = api.open_orders(moneda)
    for i in range(len(oo)):
        if oo[i].side == 'buy':
            buy_orders.append(oo[i])
    return buy_orders
#separa los sells, returns only sells.
def get_sells(moneda):
    sell_orders = []
    oo = api.open_orders(moneda)
    for i in range(len(oo)):
        if oo[i].side == 'sell':
            sell_orders.append(oo[i])
    return sell_orders

#Creamos el Grid de ordenes compra-venta
def crearGrid(gridsize, gridstep_buy, gridstep_sell, moneda,cantidad):
    ask = start_ticker(moneda).ask
    bid = start_ticker(moneda).bid #not necesary for now
    spread = ask-bid
    saved_price = []
    save_sellstop = []
    save_buystop = []
    for i in range(1,gridsize+1):
        price_order = float(ask) -(float(i*gridstep_buy))
        saved_price.append(price_order) #guardamos los precios de los buys
        long_limit(cantidad,price_order,moneda)#ponemos ordenes de compra
    

    
#vemos si es que alguna orden buy se dispara
def trigger_Orders(gridsize):
    #separamos los buys 
    buy_orders = get_buys(currency)
    if gridsize != len(buy_orders):
        trigger_order = True
    else:
        trigger_order = False
    return trigger_order

#vemos si una sell se dispara
def trigger_sells(curr_sells):
    #separamos los sells 
    sell_orders = get_sells(currency)
    if curr_sells != len(sell_orders):
        trigger_order = True
    else:
        trigger_order = False
    return trigger_order

def bubblesort(list):
# Swap the elements to arrange in order
    for iter_num in range(len(list)-1,0,-1):
        for idx in range(iter_num):
            if list[idx].price>list[idx+1].price:
                temp = list[idx]
                list[idx] = list[idx+1]
                list[idx+1] = temp
    return list

def cancelAll(moneda):
    buy_orders = get_buys(moneda)
    for i in range(len(buy_orders)):        
            oid = buy_orders[i].oid
            api.cancel_order(oid)
#main ----------------
gridsize = input('Escribe el tamano del grid: ')
gridstep = input('Escribe la distancia entre las compras: ')
gridstep_sell = input('Escribe la distancia entre las ventas: ')
print " "
print api.available_books()
print " "
currency = input("Escribe la criptomoneda con comillas, ('xrp_mxn', 'btc_mxn','eth_mxn',etc...): ")
cantidad = input('cantidad de crypto a comprar: ') 
crearGrid(gridsize,gridstep,gridstep_sell,currency,cantidad)
bid = start_ticker(currency).bid
order = api.place_order(book=currency, side='buy', order_type='market', major= cantidad)
short_limit(cantidad,float(bid)+gridstep_sell,currency)

curr_sells = get_sells(currency)
while True:
    
    trigger_buy = trigger_Orders(gridsize)
    trigger_sell = trigger_sells(len(curr_sells))
    print 'Ejecutando'
    #DEBUG print trigger_buy,'trigger buy'
    #DEBUG print trigger_sell,'trigger sells'
    if trigger_buy: #se disparó la orden buy
        #Revisar que orden ya no está:
        #primero vemos si es buy o sell
        buy_orders = get_buys(currency)
        #si es buy, ponemos la orden de buy abajo y la de sell arriba
        buy_orders = bubblesort(buy_orders)
        new_order = float(buy_orders[len(buy_orders)-1].price) - (gridstep*(gridsize-1))
        new_sell =  float(buy_orders[len(buy_orders)-1].price) + gridstep_sell
        long_limit(cantidad,new_order,currency)
        short_limit(0.8,new_sell,currency)
        curr_sells = get_sells(currency)
        buy_orders = bubblesort(buy_orders)
        #luego vemos si es sell
    elif trigger_sell:
        #si es sell ponemos la de sell arriba y la de buy
        sell_orders = get_sells(currency)
        #si es sell, ponemos la orden de sell mas arriba y la de buy abajo
        sell_orders = bubblesort(sell_orders)
        buy_orders = get_buys(currency)
        buy_orders = bubblesort(buy_orders)
        if sell_orders == []:
            new_order = float(buy_orders[len(buy_orders)-1].price) + gridstep
            long_limit(0.8,new_order,currency)
            new_sell =  new_order + gridstep_sell
            short_limit(0.8,new_sell,currency)
            curr_sells = get_sells(currency)
            buy_orders = bubblesort(buy_orders)
        elif sell_orders !=[]:
            curr_sells = get_sells(currency)
        #cancel order
        buy_orders = bubblesort(buy_orders)
        cancelAll(currency)
        crearGrid(gridsize,gridstep,gridstep_sell,currency,cantidad)
    time.sleep(5.0)
        
        
















