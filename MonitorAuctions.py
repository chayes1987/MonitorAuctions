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
            update = my_firebase.post('/logs/' + auction_id, {'log': message})
            print('Logged: ' + update)
        except Exception:
            print('Could not perform update...')
            pass

    def initialize_subscriber(self):
        subscriber = context.socket(zmq.SUB)
        subscriber.connect('tcp://127.0.0.1:1000')
        subscriber.connect('tcp://127.0.0.1:1001')
        subscriber.connect('tcp://127.0.0.1:1010')
        subscriber.connect('tcp://127.0.0.1:1011')
        subscriber.connect('tcp://127.0.0.1:1100')
        subscriber.connect('tcp://127.0.0.1:1101')
        subscriber.connect('tcp://127.0.0.1:1110')
        subscriber.connect('tcp://127.0.0.1:1111')
        subscriber.connect('tcp://127.0.0.1:2000')
        subscriber.connect('tcp://127.0.0.1:2001')
        subscriber.connect('tcp://127.0.0.1:2010')
        subscriber.setsockopt(zmq.SUBSCRIBE, str.encode(''))
        print('Subscribed to all commands & events...')

        while True:
            msg = subscriber.recv()
            m = msg.decode(encoding='UTF-8')
            print(m + ' received...')
            self.update_ui(m)

if __name__ == '__main__':
    monitor = MonitorAuctions()
    monitor.initialize_subscriber()