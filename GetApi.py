import requests
import json
def getAPI():
    ## Ta phải lấy API-key trước
    urlGetAPIKey = requests.get('https://vapi.vnappmob.com/api/request_api_key?scope=exchange_rate')
    APIKey = urlGetAPIKey.json()['results']

    #Sau đó ta format lại chuẩn theo requirement ở trên web yêu cầu
    key = 'Bearer '+APIKey
    ## Chỉnh sửa ở header
    header = {
        'Accept': 'application/json',
        'Authorization': key
        }

    urlGetAPI = requests.get(
    "https://vapi.vnappmob.com/api/v2/exchange_rate/vcb",headers = header)

    ##Kết quả return là một json object, vì thế ta cần phải format nó lại về string
    return json.dumps(urlGetAPI.json())
