import requests

API_KEY = "ea6cfd6f29063416f8b3c2723816346a"

url = "https://v3.football.api-sports.io/fixtures?next=5"

headers = {
    "x-apisports-key": API_KEY
}

res = requests.get(url, headers=headers)

print(res.status_code)
print(res.text)