from ui import TrackerInterface
from requester import Requester
from saver import DataSaver
import sys, os


def override_where():
    return os.path.abspath("cacert.pem")


if hasattr(sys, "frozen"):
    import certifi.core

    os.environ["REQUESTS_CA_BUNDLE"] = override_where()
    certifi.core.where = override_where
    import requests.utils
    import requests.adapters
    requests.utils.DEFAULT_CA_BUNDLE_PATH = override_where()
    requests.adapters.DEFAULT_CA_BUNDLE_PATH = override_where()
data_requester = Requester("https://api.hypixel.net/skyblock/bazaar")
data_saver = DataSaver("data.json")
gui = TrackerInterface(data_requester, data_saver)

