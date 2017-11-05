from trader import trader


def test_trader(asset):
    monitor = trader()
    ticker = monitor.get_ticker(asset)
    monitor.message_bot.send_message(
        'Current price of {}: {}'.format(asset, ticker['ask']))


test_trader('BTC-USD')
