#!/usr/bin/python3
import cgi
import cgitb
import json
import random
import sys

cgitb.enable()

try:
    input_data = sys.stdin.read()
    data = json.loads(input_data)
except Exception as e:
    print("Content-Type: text/html\n")
    print("<html><body>")
    print(f"<h2>Error reading input  : {e}</h2>")
    print("</body></html>")
    sys.exit(1)
try:
    shots = int(data['d'])
    t = data['t']
    buy_list = data['buy_list']
    sell_list = data['sell_list']
    mean_list = data['mean_list']
    std_list = data['std_list']
except KeyError as e:
    print("Content-Type: text/html\n")
    print("<html><body>")
    print(f"<h2>Missing data: {e}</h2>")
    print("</body></html>")
    sys.exit(1)

var95_list = []
var99_list = []

if t == 'buy':
    target_list = buy_list
elif t == 'sell':
    target_list = sell_list
else:
    print("Content-Type: application/json\n")
    print(json.dumps({"statusCode": 400, "body": "Invalid transaction"}))
    sys.exit(1)

try:
    for index, signal in enumerate(target_list):
        if signal == 1:
            mean = float(mean_list[index])
            std_dev = float(std_list[index])
            simulated_returns = [random.gauss(mean, std_dev) for _ in range(shots)]
            simulated_returns.sort(reverse=True)
            var95 = simulated_returns[int(len(simulated_returns) * 0.05)]
            var99 = simulated_returns[int(len(simulated_returns) * 0.01)]

            var95_list.append(var95)
            var99_list.append(var99)
except Exception as e:
    print("Content-Type: application/json\n")
    print(json.dumps({"statusCode": 500, "body": f"Errors: {str(e)}"}))
    sys.exit(1)

print("Content-Type: application/json\n")
print(json.dumps({
    'var95_list': var95_list,
    'var99_list': var99_list
}))
