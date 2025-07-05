import requests

coords = "64.445063,39.770515;64.5018043170571,39.80572777628643"
url = f"https://router.project-osrm.org/route/v1/driving/{coords}?overview=false&alternatives=true&steps=false"

resp = requests.get(url)
data = resp.json()

shortest = min(data["routes"], key=lambda r: r["distance"])
print(f"Самая короткая дистанция: {round(shortest['distance'] / 1000, 2)} км")
