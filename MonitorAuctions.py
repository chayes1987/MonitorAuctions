__author__ = 'Conor'

# The official documentation was consulted for all three 3rd party libraries used
# ZeroMQ -> https://learning-0mq-with-pyzmq.readthedocs.org/en/latest/pyzmq/patterns/pubsub.html
# Firebase -> https://pypi.python.org/pypi/python-firebase/1.2

from firebase import firebase
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
        try:
            my_firebase.post('/auctions/' + auction_id + '/logs', {'log': message})
            print('Log updated...')
        except Exception:
            pass

    def initialize_subscriber(self):
        subscriber = context.socket(zmq.SUB)
        subscriber.connect('tcp://172.31.32.20:1001')
        subscriber.connect('tcp://172.31.32.22:1010')
        subscriber.connect('tcp://172.31.32.21:1011')
        subscriber.connect('tcp://172.31.32.23:1100')
        subscriber.connect('tcp://172.31.32.29:1101')
        subscriber.connect('tcp://172.31.32.23:1110')
        subscriber.connect('tcp://172.31.32.23:1111')
        subscriber.connect('tcp://172.31.32.24:2000')
        subscriber.connect('tcp://172.31.32.25:2001')
        subscriber.connect('tcp://172.31.32.28:2010')
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