__author__ = 'Conor'

import zmq

context = zmq.Context()
SUBSCRIBER_ADDRESS = 'tcp://127.0.0.1:1111'


class MonitorAuctions:

    @staticmethod
    def initialize_subscriber():
        subscriber = context.socket(zmq.SUB)
        subscriber.connect(SUBSCRIBER_ADDRESS)

if __name__ == '__main__':
    monitor = MonitorAuctions()
    monitor.initialize_subscriber()