import kiteconnect
transaction_history = []

def buy(stock_ticker, quantity, price, date):
    # Add code from zerodha kite api to buy scrip
    ec2=boto3.client("ec2")
    kiteconnect.buy(stock_ticker, quantity, price, date)
    transaction_history.append({"stock_ticker": stock_ticker, "quantity": quantity, "price": price, "date": date, "action": "buy"})
    print("Buying " + str(quantity) + " of " + stock_ticker + " at " + str(price) + " on " + str(date))

def sell(stock_ticker, quantity, price, date):
    kiteconnect.sell(stock_ticker, quantity, price, date)
    transaction_history.append({"stock_ticker": stock_ticker, "quantity": quantity, "price": price, "date": date, "action": "sell"})

    print("Selling " + str(quantity) + " of " + stock_ticker + " at " + str(price) + " on " + str(date))


def calculate_result(stock_ticker):
    # Calculate profit from initial buy ans curretn sell transaction
    buy_price = 0
    sell_price = 0
    for transaction in transaction_history:
        if transaction["stock_ticker"] == stock_ticker:
            if transaction["action"] == "buy":
                buy_price = transaction["price"]
            else:
                sell_price = transaction["price"]
    return sell_price - buy_price

