# MqHelper

The extremely simple Wrapper around python mosquitto

To install run

```
pip install MqHelper
```

Supports:

* automatic reconnect
* buffering of one pending message (automatically sent after reconnect)
* management of different callback methods for different topics
* old and new python mqtt library abstraction

< 100 lines of python!

## Usage example

```
import time
import MqHelper

mq = MqHelper.MqHelper('testClient')
# or for old servers: mq = MqHelper.MqHelper('testClient', protocol=3)
mq.send('/foo', 'testmessage... bar')

def callback1(topic, msg):
	print("example callback called on topic '%s' with message '%s'"%(topic, msg))

mq.subscribe("/bar", callback1)

while True:
	mq.loop()
	time.sleep(0.1)
## or if you know you are using the new client version you can also call:
# mq.client.loop_start()
## on the internal client directly to handle polling in a background thread 
```

### Dev-Info

* update version in setup.py
* run `python setup.py sdist upload -r pypitest` to upload to test or
* `python setup.py sdist upload -r pypi` to publish