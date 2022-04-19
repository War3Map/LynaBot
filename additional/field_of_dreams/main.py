import requests


url = "http://100500otvetov.ru/page/vopros-1"
response = requests.get(url)
print(response.status_code)

with open("result.txt", "w", encoding="utf-8") as data_file:
    data_file.write(response.text)
