from trader import trader
import pandas as pd
import pandas_datareader as web


def test_trader(asset):
    monitor = trader()
    products = []
    for product in monitor.client.get_products():
        if "USD" in product["id"]:
            ticker = monitor.get_ticker(product["id"])
            try:
                products.append({product["id"]: float(ticker["ask"])})
            except KeyError as e:
                print(e)
                print(ticker["message"])

    message = "Current GDAX USD exchange rates:"
    for product in products:
        for key in product:
            message += "\n{} {}".format(key, product[key])

    print(monitor.get_macd("BTC-USD"))

    monitor.message_bot.send_message(message)


test_trader("BTC-USD")
