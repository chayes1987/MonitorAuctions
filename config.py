__author__ = 'Conor'

# Enums -> http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
# Coding Standards -> https://www.python.org/dev/peps/pep-0008/

from enum import Enum


class Config(Enum):
    """
    Class to store enumerations for the configuration file for readability
    """
    FIREBASE_URL = 0
    ADDRESSES = 1
