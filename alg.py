from client2 import run
import time
import numpy

user = "Followers"
password = "jchenxyongyshen"

def bid(ticker, amount, price):
    command = "BID "+ticker+" "+ str(price) +" "+str(amount)
    run(user, password, command)
    print 'bought ',ticker,price


def ask(ticker, amount, price):
    command = "ASK "+ticker+" "+ str(price) +" "+str(amount)
    run(user, password, command)
    print 'sold ',ticker,price

def mycash():
    return float(run(user, password, "MY_CASH")[0].rstrip().split()[1])

def check_mine():
    output = run(user, password, "MY_SECURITIES")[0].rstrip().strip("\n")
    ticker = {}
    tokens = output.split(" ")
    tokens = tokens[1:]
    for i in range(len(tokens)):
        if i % 3 == 0:
            ticker[tokens[i]] = []
            current_ticker = tokens[i]
        else:
            ticker[current_ticker].append(float(tokens[i]))

    return ticker

def check_market_price(ticker):
    command = "ORDERS "+ ticker
    output = run(user, password, command)[0].rstrip().strip("\n")
    price = {"BID":[], "ASK":[]}

    tokens = output.split(" ")
    tokens = tokens[1:]

    curr_state = ""
    curr_price = 0
    curr_shr = 0

    for i in range(len(tokens)):
        if i % 4 == 0:
            curr_state = tokens[i]
        elif i % 4 == 2:
            curr_price = tokens[i]
        elif i % 4 == 3:
            curr_shr = tokens[i]
            price[curr_state].append((curr_price,curr_shr))
        else:
            pass

#print price
    return price

hist_price = {}
hist_div = {}
threshold = {}
bought_price = {}
shares_owned = {}
dividend = {}
time_shares_owned = {}
time_to_trade = 20
bestCompany = None

def get_all_tickers_info():
    output = run(user, password,"SECURITIES")[0].rstrip().strip("\n")
    ticker = {}
    tokens = output.split(" ")
    tokens = tokens[1:]
    for i in range(len(tokens)):
        if i % 4 == 0:
            ticker[tokens[i]] = []
            current_ticker = tokens[i]
        else:
            ticker[current_ticker].append(float(tokens[i]))
    return ticker

def init_buy(companies):
    cash = mycash()
    money_to_spend = (cash - 200) / 10;
    for c in companies:
        price = float(check_market_price(c)['ASK'][0][0])
        numBought = int(money_to_spend / price)
        shares_owned[c] = numBought
        bought_price[c] = price
        time_shares_owned[c] = 0
        bid(c,numBought,price)

def sell_all(companies):
    shares = check_mine()
    for c in shares:
        numShares = int(shares[c][0])
        if numShares > 0:
            price = float(check_market_price(c)['BID'][0][0])
            ask(c,numShares,price)

def sell_all_and_buy(companies):
    shares = check_mine()
    shares_to_buy = []
    bid_ask = {}
    
    for c in shares:
        numShares = int(shares[c][0])
        if numShares > 0:
            priceBid = float(check_market_price(c)['BID'][0][0])
            priceAsk = float(check_market_price(c)['ASK'][0][0])
            if (priceAsk - priceBid)  < 5:
                ask(c,numShares,priceBid)
                shares_to_buy.append(c)
    cash = mycash()
    if len(shares_to_buy) >0:
        money_to_spend = (cash - 200) / len(shares_to_buy);
        for c in shares_to_buy:
            price = float(check_market_price(c)['ASK'][0][0])
            numBought = int(money_to_spend / price)
            shares_owned[c] = numBought
            bought_price[c] = price
            time_shares_owned[c] = 0
            bid(c,numBought,price)

def trackPerformance(ticker):
    try:
        currentPrice = float(check_market_price(c)['BID'][0][0])
    except IndexError:
        print check_market_price(c)
        currentPrice = hist_price[ticker][-1]

    hist_price[ticker].append(currentPrice)

def tryToSell(ticker):
    currentPrice = float(check_market_price(c)['BID'][0][0])
    
    if time_shares_owned[ticker] < 10:
        time_shares_owned[ticker] += 1
    else:
        time_shares_owned[ticker] = 0
        currentPrice = float(check_market_price(c)['BID'][0][0])
        dividendFuture = dividend[ticker] / (1 - 0.97)
        profit = currentPrice - bought_price[ticker] - dividendFuture
        print 'profit ',profit,currentPrice,dividendFuture
        if profit > 0:
            numShares = shares_owned[ticker]
            ask(ticker,numShares,currentPrice)

def sellWorstAndBuyBest(companies):
    bestCompany = None
    secondBestCompany = None
    worstCompany = None
    secondWorstCompany = None
    
    bestReturn = float("-inf")
    secondBestReturn = float("-inf")
    
    worstReturn = float("inf")
    secondWorstReturn = float("inf")
    
    
    gradientArray = []
    divArray = []
    
    for c in companies:
        gradient = numpy.array(hist_price[c][1:]) - numpy.array(hist_price[c][:-1])/(numpy.array(hist_price[c][:-1]))
        gradientArray.append(numpy.mean(gradient))
        d = numpy.percentile(hist_div[c],50)
        divArray.append(d)
    
    for c in companies:
        gradient = (numpy.array(hist_price[c][1:]) - numpy.array(hist_price[c][:-1]))/(numpy.array(hist_price[c][:-1]))
        #gradientScore = (numpy.mean(gradient) - numpy.mean(gradientArray)) / numpy.std(gradientArray)
        gradientScore = numpy.mean(gradient)
        d = numpy.percentile(hist_div[c],50)
        divScore = (d - numpy.mean(divArray)) / (numpy.std(divArray))
        hist_price[c] = []
        hist_div[c] = []
        ret = 1.0 * gradientScore + 0* divScore
        
        if ret > bestReturn:
            secondBestReturn = bestReturn
            bestReturn = ret
            secondBestCompany = bestCompany
            bestCompany = c
        
        elif ret > secondBestReturn:
            secondBestReturn = ret
            secondBestCompany = c
        if shares_owned[c] > 0:
            if ret < worstReturn:
                secondWorstReturn = worstReturn
                worstReturn = ret
                secondWorstCompany = worstCompany
                worstCompany = c
                
            elif ret < secondWorstReturn and shares_owned[c] > 0:
                secondWorstReturn = ret
                secondWorstCompany = c
    

    cash = mycash()
    print 'Cash ',cash,'Worst ',worstCompany,' Best ',bestCompany, ' Second Worst ', secondWorstCompany,' Second best ', secondBestCompany
    
    
    numShares = 0
    numShares_second = 0
    sellPrice = 0
    sellPrice_second = 0
    
    if worstCompany:
        numShares = shares_owned[worstCompany]*0.9
        shares_owned[worstCompany] = 0
        sellPrice = float(check_market_price(worstCompany)['BID'][0][0])
        ask(worstCompany,numShares,sellPrice)

    if secondWorstCompany:
        numShares_second = shares_owned[secondWorstCompany]*0.9
        shares_owned[secondWorstCompany] = 0
        sellPrice_second = float(check_market_price(secondWorstCompany)['BID'][0][0])
        ask(secondWorstCompany,numShares_second,sellPrice_second)

    money_to_spend = (cash - 200 + numShares * sellPrice + numShares_second * sellPrice_second)*0.75
    money_to_spend_second = (cash - 200 + numShares * sellPrice + numShares_second * sellPrice_second)*0.25

    buyPrice = float(check_market_price(bestCompany)['ASK'][0][0])
    buyPrice_second= float(check_market_price(secondBestCompany)['ASK'][0][0])

    numBought = int(money_to_spend / buyPrice)
    numBought_second = int(money_to_spend_second /buyPrice_second)
    if (money_to_spend>1) and (money_to_spend_second > 1):
        shares_owned[bestCompany] = numBought
        bought_price[bestCompany] = buyPrice
        bid(bestCompany,numBought,buyPrice)

        shares_owned[secondBestCompany] = numBought_second
        bought_price[secondBestCompany] = buyPrice_second
        bid(secondBestCompany,numBought_second,buyPrice_second)

def main():

    #init_time = time.time()
    #current_time = time.time()
    #time_span = current_time-init_time


    #bid("AMZN", 1, 65)
    #ask("AMZN", 1, 59)
    #check_mine()


    #check_market_price("QQ")

    check_mine()
    #output = get_all_tickers_info()
    #parse_price(output)

if __name__ == "__main__":
    #main()
    companies = get_all_tickers_info()
    sell_all(companies)
    for c in companies:
        shares_owned[c] = 0
        hist_price[c] = []
        hist_div[c] = []
    init_buy(companies)

    i = 0
    while True:
        try:
            portfolio = check_mine()
            for c in companies:
                dividend[c] = portfolio[c][1]
                hist_div[c].append(dividend[c])
                trackPerformance(c)
            if i%30 == 29:
                #pass
                sell_all_and_buy(companies)
            elif i%time_to_trade == time_to_trade - 1:
                sellWorstAndBuyBest(companies)
            time.sleep(1)
            i+=1
        except Exception as e:
            print e
            continue




    #while time_span < 100:

