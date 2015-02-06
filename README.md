# MqHelper

The extremely simple Wrapper around python mosquitto

To install run

```
python setup.py install
```

Supports:

* automatic reconnect
* buffering of one pending message (automatically sent after reconnect)
* management of different callback methods for different topics

< 100 lines of python!

## Usage example

```
import time
import MqHelper

mq = MqHelper.MqHelper('testClient')
mq.send('/foo', 'testmessage... bar')

def callback1(topic, msg):
	print("example callback called on topic '%s' with message '%s'"%(topic, msg))

mq.subscribe("/bar", callback1)

while True:
	mq.loop()
	time.sleep(0.1)
```
