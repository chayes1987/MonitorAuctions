__author__ = 'Conor'

# Firebase -> https://pypi.python.org/pypi/python-firebase/1.2
# Config file -> https://docs.python.org/2/library/configparser.html

from monitorauctions import MonitorAuctions
from configparser import ConfigParser, Error
from firebase import firebase
from config import Config


def read_config():
    config = ConfigParser()
    try:
        config.read_file(open('config.ini'))
        firebase_url = config.get('Firebase', 'FIREBASE_URL')
        addresses = config.items('Addresses')
    except (IOError, Error):
        print('Error with config file...')
        return None

    return firebase_url, addresses


if __name__ == '__main__':
    configuration = read_config()
    if None != configuration:
        my_firebase = firebase.FirebaseApplication(configuration[Config.FIREBASE_URL], authentication=None)
        monitor = MonitorAuctions(my_firebase)
        monitor.initialize_subscriber(configuration[Config.ADDRESSES])