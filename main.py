__author__ = 'Conor'

# Firebase -> https://pypi.python.org/pypi/python-firebase/1.2
# Config file -> https://docs.python.org/2/library/configparser.html
# Coding Standards -> https://www.python.org/dev/peps/pep-0008/

from monitorauctions import MonitorAuctions
from configparser import ConfigParser, Error
from firebase import firebase
from config import Config


def read_config():
    """
    Reads the configuration file
    :return: A tuple with the entries from the file, None if exception
    """
    config = ConfigParser()
    try:
        # Open the file and extract the contents
        config.read_file(open('config.ini'))
        firebase_url = config.get('Firebase', 'FIREBASE_URL')
        addresses = config.items('Addresses')
    except (IOError, Error):
        print('Error with config file...')
        return None

    return firebase_url, addresses


if __name__ == '__main__':
    configuration = read_config()
    # Check configuration
    if None != configuration:
        my_firebase = firebase.FirebaseApplication(configuration[Config.FIREBASE_URL], authentication=None)
        monitor = MonitorAuctions(my_firebase)
        monitor.initialize_subscriber(configuration[Config.ADDRESSES])