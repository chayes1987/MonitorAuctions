__author__ = 'Conor'

# The official documentation was consulted for all three 3rd party libraries used
# ZeroMQ -> https://learning-0mq-with-pyzmq.readthedocs.org/en/latest/pyzmq/patterns/pubsub.html
# Firebase -> https://pypi.python.org/pypi/python-firebase/1.2

from firebase import firebase
from datetime import datetime
import zmq

context = zmq.Context()
FIREBASE_URL = 'https://auctionapp.firebaseio.com'
my_firebase = firebase.FirebaseApplication(FIREBASE_URL, authentication=None)


class MonitorAuctions:

    @staticmethod
    def parse_message(message, start_tag, end_tag):
        start_index = message.index(start_tag) + len(start_tag)
        substring = message[start_index:]
        end_index = substring.index(end_tag)
        return substring[:end_index]

    def update_ui(self, message):
        auction_id = self.parse_message(message, '<id>', '</id>')
        data = {'_id': auction_id, 'log': message, 'log_date': datetime.now()}
        try:
            my_firebase.post('/auctions/' + auction_id + '/logs', data)
            print('Log updated...')
        except Exception:
            pass

    def initialize_subscriber(self):
        subscriber = context.socket(zmq.SUB)
        subscriber.connect('tcp://172.31.32.20:2000')
        subscriber.connect('tcp://172.31.32.21:2100')
        subscriber.connect('tcp://172.31.32.22:2200')
        subscriber.connect('tcp://172.31.32.23:2300')
        subscriber.connect('tcp://172.31.32.23:2350')
        subscriber.connect('tcp://172.31.32.23:2360')
        subscriber.connect('tcp://172.31.32.23:2370')
        subscriber.connect('tcp://172.31.32.24:2400')
        subscriber.connect('tcp://172.31.32.25:2500')
        subscriber.connect('tcp://172.31.32.28:2800')
        subscriber.connect('tcp://172.31.32.29:2900')
        subscriber.setsockopt(zmq.SUBSCRIBE, str.encode(''))
        print('Subscribed to all commands & events...')

        while True:
            msg = subscriber.recv()
            m = msg.decode()
            print(m + ' received...')
            self.update_ui(m)

if __name__ == '__main__':
    monitor = MonitorAuctions()
    monitor.initialize_subscriber()