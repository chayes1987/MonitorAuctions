__author__ = 'Conor'

import zmq

context = zmq.Context()


class MonitorAuctions:

    @staticmethod
    def update_ui(message):
        print(message)

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