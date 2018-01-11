import requests
import csv
from bs4 import BeautifulSoup

# セッションを開始
client = requests.session()

URL = 'https://premier.no1s.biz'

# Retrieve the CSRF token first
csrftoken = ""
client.get(URL)  # sets cookie
if 'csrfToken' in client.cookies:
    # Django 1.6 and up
    csrftoken = client.cookies['csrfToken']
else:
    # older versions
    csrftoken = client.cookies['_csrfToken']

# メールアドレスとパスワードの指定
MAIL = "micky.mouse@no1s.biz"
PASS = "micky"

# ログイン
login_info = {
    "_method":"POST",
    "_csrfToken":csrftoken,
    "email":MAIL,
    "password":PASS
}

# action
url_login = "https://premier.no1s.biz"
res = client.post(url_login, data=login_info, headers=dict(Referer=url_login))

for i in range(3):
    res = client.get("https://premier.no1s.biz/admin?page="+str(i+1))
    bsObj = BeautifulSoup(res.text, "html.parser")
    # テーブルを指定
    table = bsObj.findAll("table", {"class": "table-striped"})[0]
    rows = table.findAll("tr")

    if i == 0:
        csvFile = open("premier01.csv", 'wt', newline='', encoding='utf-8')
        writer = csv.writer(csvFile, quoting=csv.QUOTE_ALL,delimiter=',',quotechar='"', lineterminator=',\n')

    try:
        for row in rows:
            csvRow = []
            if  row.findAll(['td']) == []:
                continue
            for cell in row.findAll(['td']):
                csvRow.append(cell.get_text())
            writer.writerow(csvRow)
    finally:
        if i == 2:
            csvFile.close()