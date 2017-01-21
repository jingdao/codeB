from client2 import run
import time

user = "Followers"
password = "jchenxyongyshen"

def bid(ticker, amount, price):
    command = "BID "+ticker+" "+ str(price) +" "+str(amount)
    run(user, password, command)


def ask(ticker, amount, price):
    command = "ASK "+ticker+" "+ str(price) +" "+str(amount)
    run(user, password, command)

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

    print price
    return price

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
    main()



    #while time_span < 100:

