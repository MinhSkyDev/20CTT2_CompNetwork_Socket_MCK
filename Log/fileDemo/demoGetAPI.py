import requests



urlGetAPIKey = requests.get('https://vapi.vnappmob.com/api/request_api_key?scope=exchange_rate')
APIKey = urlGetAPIKey.json()['results']

key = 'Bearer '+APIKey

header = {
    'Accept': 'application/json',
    'Authorization': key
    }

urlGetAPI = requests.get(
"https://vapi.vnappmob.com/api/v2/exchange_rate/sbv",headers = header)
print(urlGetAPI.json())
