from ui import TrackerInterface
from requester import Requester
from saver import DataSaver

data_requester = Requester("https://api.hypixel.net/skyblock/bazaar")
data_saver = DataSaver("data.json")
gui = TrackerInterface(data_requester, data_saver)

