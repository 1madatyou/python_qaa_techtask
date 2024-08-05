import requests
import json

INT32_MIN = -2147483648
INT32_MAX = 2147483647

data = {"x": INT32_MIN-1, "y": 1}
r = requests.post("http://127.0.0.1:17678/api/remainder", data=json.dumps(data))
print(r.json())