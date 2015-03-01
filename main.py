__author__ = 'Conor'

# Firebase -> https://pypi.python.org/pypi/python-firebase/1.2
# Config file -> https://docs.python.org/2/library/configparser.html

from monitorauctions import MonitorAuctions
from configparser import ConfigParser, Error
from firebase import firebase
from config import Config


def read_config():
    conf = ConfigParser()
    try:
        conf.read_file(open('config.ini'))
        firebase_url = conf.get('Firebase', 'FIREBASE_URL')
        addresses = conf.items('Addresses')
    except (IOError, Error):
        print('Error with config file...')
        return None

    return firebase_url, addresses


if __name__ == '__main__':
    config = read_config()
    if None != config:
        my_firebase = firebase.FirebaseApplication(config[Config.FIREBASE_URL], authentication=None)
        monitor = MonitorAuctions(my_firebase)
        monitor.initialize_subscriber(config[Config.ADDRESSES])