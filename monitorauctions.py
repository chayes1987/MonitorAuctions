__author__ = 'Conor'

# The official documentation was consulted for all 3rd party libraries used
# 0mq -> https://learning-0mq-with-pyzmq.readthedocs.org/en/latest/pyzmq/patterns/pubsub.html
# Coding Standards -> https://www.python.org/dev/peps/pep-0008/

from datetime import datetime
import zmq

context = zmq.Context()
my_firebase = None


class MonitorAuctions:
    """
    This class is responsible for monitoring all auctions

    Attributes:
      context (0mq context): A 0mq context.
      my_firebase (Firebase): The firebase reference URL.
    """

    def __init__(self, firebase):
        """
        Constructor
        :param firebase: The firebase reference URL
        :return: Nothing
        """
        global my_firebase
        my_firebase = firebase

    @staticmethod
    def parse_message(message, start_tag, end_tag):
        """
        Parses received messages
        :param message: The message to parse
        :param start_tag: The starting delimiter
        :param end_tag: The ending delimiter
        :return: The required string
        """
        start_index = message.index(start_tag) + len(start_tag)
        substring = message[start_index:]
        end_index = substring.index(end_tag)
        return substring[:end_index]

    def update_dashboard(self, message):
        """
        Updates the dashboard
        :param message: The received message
        :return: Nothing
        """
        auction_id = self.parse_message(message, '<id>', '</id>')
        # Set the data for the update
        data = {'_id': auction_id, 'log': message, 'log_date': datetime.now()}
        try:
            # Perform the update
            my_firebase.post('/auctions/' + auction_id + '/logs', data)
            print('Log updated...')
        except Exception:
            pass

    def initialize_subscriber(self, addresses):
        """
        Initializes the subscriber
        :param addresses: The list of addresses to connect to
        :return: Nothing
        """
        subscriber = context.socket(zmq.SUB)

        # Connect to all the addresses from the configuration file
        for key, address in addresses:
            subscriber.connect(address)

        # Set the topic to empty - all topics
        subscriber.setsockopt(zmq.SUBSCRIBE, str.encode(''))
        print('SUB: All commands & events...')

        while True:
            try:
                msg = subscriber.recv()
                m = msg.decode()
                # Ignore Heartbeat
                if m.startswith('Ok '):
                    continue
                print('REC: ' + m)
                # Perform update
                self.update_dashboard(m)
            except (KeyboardInterrupt, SystemExit):
                print('Application Stopped...')
                raise SystemExit
