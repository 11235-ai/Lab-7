import json
import requests


city_name = "Madrid"
key = ""
response = requests.post(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={key}")
result = json.loads(response.text)
print(result)
