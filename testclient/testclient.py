
import requests

rsp = requests.get("http://host.docker.internal:80/query")
assert len(rsp.json()["records"]) == 1461
print(rsp.json())

rsp = requests.get("http://host.docker.internal:80/query?weather=rain&limit=5")
assert len(rsp.json()["records"]) == 5
print(rsp.json())

rsp = requests.get("http://host.docker.internal:80/query?weather=rain&limit=3")
assert len(rsp.json()["records"]) == 3
print(rsp.json())

rsp = requests.get("http://host.docker.internal:80/query?weather=rain&wind=4.5&temp_min=11.1")
assert len(rsp.json()["records"]) == 1
print(rsp.json())
