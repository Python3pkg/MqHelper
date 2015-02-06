#!/usr/bin/python
# -*- coding: UTF-8 -*-

# support both old and new python package ( http://mosquitto.org/documentation/python/ )
try: from paho.mqtt.client import Client as Mosquitto
except ImportError: from mosquitto import Mosquitto

class MqHelper:

	def __init__(self, name=None, host=None):
		self.client = None
		self.pending = None
		self.host = host or '127.0.0.1'
		self.clientName = name or 'testClient'
		self.subscriptions = {}

	def loop(self):
		if self.client == None:
			self.reconnect()
		ret = self.client.loop()
		if ret != 0:
			print("mosquitto client error")
			try:
				self.client.disconnect()
			except:
				pass
			self.client = None

	def send(self, topic, msg):
		if self.client:
			ret = -1
			try:
				ret = self.client.publish(topic, msg, 1)
			except:
				print("error sending msg")
			if ret == 0 or len(ret) > 1 and ret[0] == 0:
				# sending success
				self.pending = None
			else:
				print("returned %s"%str(ret))
				print("saving pending msg %s %s"%(topic, msg))
				self.pending = (topic, msg)
				self.reconnect()				
		else:
			print("client not available, saving as pending")
			self.pending = (topic, msg)
			self.reconnect()

	def onConnect(self):
		def callback(mosq, obj, rc):
			if rc != 0:
				self.client = None
				print("connecting failed")
			else:
				self.client.on_message = self.createMsgCallback()
				self.__subscribeAll()
				print("connected")
				if self.pending:
					print("sending pending message %s"%self.pending[1])
					self.send(self.pending[0], self.pending[1])
		return callback

	def __subscribeAll(self):
		for topic in self.subscriptions.keys():
			self.client.subscribe(topic, 0)

	def subscribe(self, topic, callback):
		self.subscriptions[topic] = callback
		if self.client != None:
			self.client.subscribe(topic, 0)

	def createMsgCallback(self):
		def callback(mosq, obj, msg):
			print("received msg on %s"%msg.topic)
			if self.subscriptions.has_key(msg.topic):
				self.subscriptions[msg.topic](msg.topic, msg.payload)
		return callback

	def reconnect(self):
		print("reconnecting...")
		try:
			self.client = Mosquitto(self.clientName)
			ret = self.client.connect(self.host)
			if ret == 0:
				self.client.on_connect = self.onConnect()
			else:
				self.client = None
		except:
			self.client = None
