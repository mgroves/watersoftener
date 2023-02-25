Water Softener level sensor software

(I'm not a Python dev, I have no idea what I'm doing.)

* Designed to run on a Raspberry Pi Pico W

To build it, I basically followed the steps here: https://www.tomshardware.com/how-to/raspberry-pi-pico-ultrasonic-sensor with
one exception: I found that 3.3V doesn't work (it results in garbage output from the sensor), so I use the 5V connection instead.

* Designed to publish a message to /watersoftener MQTT channel

I'm using MQTT because I want this software to do as *little* as possible, and let Home Assistant do the rest.

* Configuration can be changed by accessing settings via web UI

I did this so I don't have to haul the sensor back and forth between my office and water softener to make changes (e.g. I change my wifi SSD and password every so often).

* Put settings into config.json. See config.json.template for how to create this file.

I use this sensor with Home Assistant. Here's how I set up the sensor:

```
# configuration.yaml

mqtt:
  sensor:
    - name: "Water Softener"
      state_topic: "/watersoftener"
      value_template: "{{ value_json.distance }}"
```

And here's the automation I use to send me a notification
on monday, wednesday, and friday at 8:30am if the sensor
detects a distance of 60cm or above.

```
# automations.yaml

- id: '1677353245654'
  alias: 'Water Softener: Check Salt Level'
  description: ''
  trigger:
  - platform: time
    at: 08:30:00
  condition:
  - condition: numeric_state
    entity_id: sensor.water_softener
    above: 60
  - condition: time
    weekday:
    - mon
    - wed
    - fri
  action:
  - service: notify.gmail_smtp
    data:
      title: '[Home Assistant] Water Softener Salt is Low'
      message: Put some more salt in the softener.
  mode: single
```

