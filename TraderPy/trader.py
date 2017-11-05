from groupme import groupme
import gdax

class trader:

    def __init__(self):
        self.message_bot = groupme()
        self.public_client = gdax.PublicClient()

    def get_ticker(self, asset):
        return self.public_client.get_product_ticker(asset)
