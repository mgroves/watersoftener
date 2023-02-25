from machine import Pin
import time
from umqttsimple import MQTTClient
from microdot import Microdot, Response, send_file, redirect
from microdot_utemplate import render_template
import ubinascii
import machine
import utime
import micropython
import network
import ujson
import _thread
import gc
gc.collect()

with open("config.json") as configfile:
    configdata = ujson.load(configfile)

ssid = configdata["wifissid"]
password = configdata["wifipassword"]
mqtt_server = configdata["mqtt_server"]
mqttusername = configdata["mqttusername"]
mqttpassword = configdata["mqttpassword"]
secondsbetweenchecking = configdata["secondsbetweenchecking"]
webpassword = configdata["webpassword"]
topic_pub = b'/watersoftener'

client_id = ubinascii.hexlify(machine.unique_id())

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass

print('Connection successful')
print(station.ifconfig())

def connect():
    print('Connecting to MQTT Broker...')
    global client_id, mqtt_server
    client = MQTTClient(client_id, mqtt_server, user = mqttusername, password = mqttpassword)
    client.connect()
    print('Connected to %s MQTT broker' % (mqtt_server))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

def ultra():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    return f"{{ \"distance\" : {distance} }}"

try:
    client = connect()
except OSError as e:
    restart_and_reconnect()

# web server
app = Microdot()

Response.default_content_type = "text/html"

@app.route('/', methods=['GET'])
def index(request):
    with open("config.json") as jsonfile:
        configjson = ujson.load(jsonfile)
        jsontoshow = ujson.dumps(configjson)
    return render_template('index.html', jsontoshow)

@app.route('/', methods=['POST'])
def index(request):
    config = request.form.get('configjson')
    password = request.form.get('password')
    if password != webpassword:
        return "Not authorized",401
    with open("config.json",'w') as jsonfile:
        jsontosave = ujson.loads(config)
        ujson.dump(jsontosave,jsonfile)
    return redirect("/")

@app.route('/images/<path:path>')
def static(request,path):
    if '..' in path:
        return 'Not found',404
    return send_file('images/' + path)

# sensor loop
def sensor_loop():
    while True:
        try:
            msg = ultra()
            print('Publishing message: %s on topic %s' % (msg, topic_pub))
            client.publish(topic_pub, msg)
            time.sleep(secondsbetweenchecking)
        except OSError as e:
            restart_and_reconnect()

_thread.start_new_thread(sensor_loop,())

app.run(port=80)
