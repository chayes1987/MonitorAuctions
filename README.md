# MonitorAuctions

This is the monitor auctions service for my FYP. It is written in Python. It uses a 0mq binding. It is responsible for
monitoring all auctions and recording the data in Firebase for display in the web interface.

## Project Setup

Requires firebase integration.

## License

None

## Setting up MonitorAuctions service on AWS

- Created AWS EC2 Linux instance
- Connected to instance using FileZilla using Public DNS and .pem keyfile
- Uploaded application directory to server
- Connected to server instance using PuTTy using ec2-user@PublicDNS and .ppk keyfile for SSH Auth

## Application Setup Required

- Installed gcc -> sudo yum install gcc-c++
- Installed python-dev -> sudo yum install python-devel
- Installed zmq binding - sudo easy_install pyzmq
- Installed firebase - sudo easy_install requests==1.1.0
		                 - sudo easy_install python-firebase
- Installed config parser -> sudo easy_install configparser
- Installed enum -> sudo easy_install enum

- Running the service -> sudo python /home/ec2-user/MonitorAuctions/main.py

- Service runs and works as expected
