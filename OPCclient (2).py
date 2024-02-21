import RPi.GPIO as gpio
import dht11
import time
import datetime
from opcua import Server

server = Server()

def InOut():
	gpio.setmode(gpio.BOARD)
	gpio.setup(36,gpio.OUT)

def setting_DHT_Sensor():

	gpio.setwarnings(False)
	gpio.setmode(gpio.BOARD)
	gpio.cleanup()

	return dht11.DHT11(12)


def by():

	print("GoodBy")
	server.stop()


def OPCUA_Connect():
	url="opc.tcp://192.168.1.103:4080"
	server.set_endpoint(url)

	name="OPCUA_Server"
	addspace=server.register_namespace(name)

	node=server.get_objects_node()
	param=node.add_object(addspace,"Parametres")


	temp=param.add_variable(addspace,"Temperature",1)
	hum=param.add_variable(addspace,"Humidity",1)
	tim=param.add_variable(addspace,"Time",1)
	led=param.add_variable(addspace,"LED ON/OFF",0)

	temp.set_writable()
	hum.set_writable()
	tim.set_writable()
	led.set_writable()


	server.start()

	print("server is starting please set your value")
	return temp,hum,tim,led

try:
	[temp,hum,tim,led]=OPCUA_Connect()
	dhtread=setting_DHT_Sensor()
	InOut()
	while True:
		reading=dhtread.read()
		if reading.is_valid():
			Temperature=reading.temperature
			Humidity=reading.humidity
			now=datetime.datetime.now()
			Time=now.strftime("%H:%M:%S")
			temp.set_value(Temperature)
			tim.set_value(Time)
			hum.set_value(Humidity)
		time.sleep(1)
		Led=led.get_value()
		#led.set_value(Led)
		if Led == 1:
			gpio.output(36, gpio.HIGH)
		elif Led == 0 :
			gpio.output(36, gpio.LOW)
except:
        by()






