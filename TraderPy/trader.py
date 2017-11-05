from groupme import groupme
import gdax

class trader:

    def __init__(self):
        self.message_bot = groupme()
        self.client = gdax.PublicClient()

    def get_ticker(self, asset):
        return self.client.get_product_ticker(asset)
