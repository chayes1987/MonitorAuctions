__author__ = 'Conor'

# The official documentation was consulted for all three 3rd party libraries used
# ZeroMQ -> https://learning-0mq-with-pyzmq.readthedocs.org/en/latest/pyzmq/patterns/pubsub.html

from datetime import datetime
import zmq

context = zmq.Context()
my_firebase = None


class MonitorAuctions:

    def __init__(self, firebase):
        global my_firebase
        my_firebase = firebase

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

    def initialize_subscriber(self, addresses):
        subscriber = context.socket(zmq.SUB)

        for key, address in addresses:
            subscriber.connect(address)

        subscriber.setsockopt(zmq.SUBSCRIBE, str.encode(''))
        print('SUB: All commands & events...')

        while True:
            msg = subscriber.recv()
            m = msg.decode()
            print('REC: ' + m)
            self.update_ui(m)
