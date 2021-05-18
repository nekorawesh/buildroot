from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
import paho.mqtt.client as mqtt
import json
from enum import Enum


class MQTTAddress(Enum):
	address = "localhost"
	port = 1883
	keep_alive = 60


class MQTTSubTopics(Enum):
	time = "maestro/hss/time"
	operationRuntime = "maestro/hss/operationRuntime"
	PSMMeasurement = "maestro/hss/PSMMeasurement"
	moduleRuntime = "maestro/hss/moduleRuntime"
	errorRuntime = "maestro/hss/errorRuntime"
	inputDemands = "maestro/hss/inputDemands"
	signalGroupSignals = "maestro/hss/signalGroupSignals"
	relayState = "maestro/hss/relayState"
	userSettings = "maestro/hss/userSettings"
	logInfo = "maestro/hss/logInfo"
	lastLogIndex = "maestro/hss/lastLogIndex"
	gateStateLog = "maestro/hss/gateStateLog"
	state = "maestro/hss/state"
	phaseCount = "maestro/hss/phaseCount"
	stepCount = "maestro/hss/stepCount"
	stepInfo = "maestro/hss/stepInfo"


class MQTTPubTopics(Enum):
	time = "maestro/mmi/time"
	userSettings = "maestro/mmi/userSettings"
	factoryReset = "maestro/mmi/factoryReset"
	relayState = "maestro/mmi/relayState"
	startSignalGroupSignals = "maestro/mmi/startSignalGroupSignals"
	startInputDemand = "maestro/mmi/startInputDemand"
	lastLogIndex = "maestro/mmi/lastLogIndex"
	PSMMeasurement = "maestro/mmi/PSMMeasurement"
	gprsSetting = "maestro/mmi/gprsSetting"
	logInfo = "maestro/mmi/logInfo"
	startInputDemands = "maestro/mmi/startInputDemands"
	phaseCount = "maestro/mmi/phaseCount"
	stepCount = "maestro/mmi/stepCount"
	stepInfo = "maestro/mmi/stepInfo"


class SubThread(QThread):
	signal_time = pyqtSignal(dict)
	signal_operationRuntime = pyqtSignal(dict)
	signal_PSMMeasurement = pyqtSignal(dict)
	signal_moduleRuntime = pyqtSignal(dict)
	signal_errorRuntime = pyqtSignal(dict)
	signal_inputDemands = pyqtSignal(dict)
	signal_signalGroupSignals = pyqtSignal(dict)
	signal_relayState = pyqtSignal(dict)
	signal_logInfo = pyqtSignal(dict)
	signal_userSettings = pyqtSignal(dict)
	signal_lastLogIndex = pyqtSignal(dict)
	signal_gateStateLog = pyqtSignal(dict)
	signal_phaseCount = pyqtSignal(dict)
	signal_stepCount = pyqtSignal(dict)
	signal_stepInfo = pyqtSignal(dict)

	signal_MQTT_server_error = pyqtSignal(bool)
	signal_State = pyqtSignal(dict)

	def run(self):
		mqttc = mqtt.Client()
		mqttc.on_message = self.on_message

		try:
			mqttc.connect(MQTTAddress.address.value, MQTTAddress.port.value, MQTTAddress.keep_alive.value)

			for topic in MQTTSubTopics:
				mqttc.subscribe(topic.value, 0)

			PubThread.MQTT_connection_status = True
			mqttc.loop_forever()
			self.signal_MQTT_server_error.emit(False)
		except Exception as e:
			print(e)
			PubThread.MQTT_connection_status = False
			self.signal_MQTT_server_error.emit(True)
			#print("MQTT SERVER NOT FOUND")
			self.sleep(5)
			self.off_restart()

	def on_message(self, mosq, obj, msg):
		# self.change_signal.emit(("MESSAGE: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload)))
		# #print("MESSAGE: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
		data = json.loads(msg.payload)
		# #print(str(msg.topic) + str(data))
		# if(msg.topic == "maestro/hss/heartbeat"):
		if msg.topic == MQTTSubTopics.time.value:
			self.signal_time.emit(data)
		elif msg.topic == MQTTSubTopics.operationRuntime.value:
			self.signal_operationRuntime.emit(data)
		elif msg.topic == MQTTSubTopics.PSMMeasurement.value:
			self.signal_PSMMeasurement.emit(data)
		elif msg.topic == MQTTSubTopics.moduleRuntime.value:
			self.signal_moduleRuntime.emit(data)
		elif msg.topic == MQTTSubTopics.errorRuntime.value:
			self.signal_errorRuntime.emit(data)
		elif msg.topic == MQTTSubTopics.inputDemands.value:
			self.signal_inputDemands.emit(data)
		elif msg.topic == MQTTSubTopics.signalGroupSignals.value:
			self.signal_signalGroupSignals.emit(data)
		elif msg.topic == MQTTSubTopics.relayState.value:
			self.signal_relayState.emit(data)
		elif msg.topic == MQTTSubTopics.userSettings.value:
			self.signal_userSettings.emit(data)
		elif msg.topic == MQTTSubTopics.logInfo.value:
			self.signal_logInfo.emit(data)
		elif msg.topic == MQTTSubTopics.lastLogIndex.value:
			self.signal_lastLogIndex.emit(data)
		elif msg.topic == MQTTSubTopics.gateStateLog.value:
			self.signal_gateStateLog.emit(data)
		elif msg.topic == MQTTSubTopics.state.value:
			self.signal_State.emit(data)
		elif msg.topic == MQTTSubTopics.phaseCount.value:
			self.signal_phaseCount.emit(data)
		elif msg.topic == MQTTSubTopics.stepCount.value:
			self.signal_stepCount.emit(data)
		elif msg.topic == MQTTSubTopics.stepInfo.value:
			self.signal_stepInfo.emit(data)


	def on_unsubscribe(self):
		pass

	def off_restart(self):
		# QTest.qWait(1000)
		#print("MQTT RESTARTED")
		self.run()


class PubThread(QThread):
	MQTT_MSG_dict = ""
	MQTT_MSG = ""
	MQTT_TOPIC = "maestro/mmi/relayState"
	# MQTT_connection_status = False
	MQTT_connection_status = True
	mqttc = ""

	def run(self):
		if self.MQTT_connection_status:
			self.mqttc = mqtt.Client()

			self.mqttc.on_log = self.on_log
			self.mqttc.on_connect = self.on_connect
			self.mqttc.on_publish = self.on_publish

			# mqttc.username_pw_set(username="username", password="password")
			self.mqttc.connect(MQTTAddress.address.value, MQTTAddress.port.value, MQTTAddress.keep_alive.value)
			self.mqttc.publish(self.MQTT_TOPIC, self.MQTT_MSG)

			self.disconnect()

	def changed_values(self, MQTT_MSG_dict):
		self.MQTT_MSG = json.dumps(MQTT_MSG_dict)

	def on_connect(self, client, userdata, flags, rc):
		#print(client, userdata, flags, rc)
		pass

	def on_publish(self, client, userdata, mid):
		#print(client, userdata, mid)
		pass

	def on_log(mqttc, obj, level, string):
		#print(mqttc, obj, level, string)
		pass

	def disconnect(self):
		self.mqttc.disconnect()
