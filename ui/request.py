import requests

URI = "https://8000-aldojesusmartin-apidemo-bv1shlw5kif.ws-us105.gitpod.io/v1/contactos"

response = requests.get(URI)

print(f"GET : {response.text}")
print(f"GET : {response.status_code}")

data = {"nombre":"Prueba","email":"prueba@gmail.com"}

response = requests.post(URI, json=data)

print(f"POST : {response.text}")
print(f"POST : {response.status_code}")
