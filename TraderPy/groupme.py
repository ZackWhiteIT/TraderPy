import requests
import yaml
import os


class groupme:
    def __init__(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, "secrets.yml")

        with open(filename, "r") as ymlfile:
            self.secrets = yaml.load(ymlfile)

    def send_message(self, message):
        try:
            r = requests.post(
                self.secrets["groupme"]["url"],
                data={"bot_id": self.secrets["groupme"]["bot_id"], "text": message},
            )
        except Error as e:
            print(e)
