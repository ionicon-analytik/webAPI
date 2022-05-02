#################################################
#                                               #
# Ionicon WebAPI - usage example                #
#                                               #
#################################################
import os
import time
import json

import ioniclient


client = ioniclient.IoniClient('localhost', port=8002)

print('# Example 1: Quick measurement (with default filename) for 10 seconds, then stop')
print(client.start_measurement())
time.sleep(10)
print(client.stop_measurement())


print('# Example 2: Measurement with filename, for 10 seconds, then stop')
folder = os.path.join('D:', 'Data')
os.makedirs(folder, exist_ok=True)
filename = time.strftime("example2_%m-%d-%Y_%H-%M-%S", time.localtime())
path = os.path.join(folder, filename)

print(client.start_measurement(path))
time.sleep(10)
print(client.stop_measurement())


print('# Example 3: Start measurement, print some TPS parameters')
print(client.start_measurement())
for parameter in ['TPS_Pull_L', 'TPS_Lens1', 'DPS_Udrift', 'E/N', 'Press_Foreline']:
    raw = client.get(parameter)
    data = json.loads(raw)
    setv = data[0]['Act']
    print(data[0]['Name'], setv['Real'], setv['Unit'], setv['Time'])

print(client.stop_measurement())


print('# Example 4: Start measurement, for 10 seconds, print the first few calc traces')
print(client.start_measurement())
for i in range(10):
    traces = client.get_traces()
    if not traces:
        continue

    parsed = json.loads(traces)
    for name, value in zip(parsed["CalcTracesNames"], parsed["CalcTraces"]):
        print(name, value)

print(client.stop_measurement())


print('# Example 5: use API to set TPS parameters')

prev = client.get('DPS_Udrift')
data = json.loads(prev)
original = data[0]['Set']['Real']

print('scanning drift voltage in 100 V steps...')
for voltage in range(400, 700, 100):
    client.set('DPS_Udrift', voltage)
    print(client.get('DPS_Udrift'))

client.set('DPS_Udrift', original)

