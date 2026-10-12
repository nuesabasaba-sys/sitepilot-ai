import requests
from bs4 import BeautifulSoup

url = input("URLを入力してください: ")
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

print(response.status_code)
if soup.title is not None:
    title = soup.title.text
else:
    title = ""
print("title:", title)
if soup.h1 is not None:
    h1 = soup.h1.get_text(" ", strip=True)
else:
    h1 = ""
print("h1:", h1)
h2_list = soup.find_all("h2")
h2_text_list = []
for h2 in h2_list:
    h2_text_list.append(h2.get_text(" ", strip=True))
print("h2:", h2_text_list)

print("h2の数:", len(h2_list))

if len(h2_list) ==0:
    print("h2なし")
    
for h2 in h2_list:
    print(h2.text)
    
description_tag = soup.find("meta", attrs={"name": "description"})
if description_tag is not None:
    description = description_tag["content"]
else:
    description = ""
print("description:", description)
body = soup.body
body_text = body.get_text(" ", strip=True)
print(body_text)
page_data = {
    "url": url,
    "title": title,
    "description": description,
    "h1": h1,
    "h2": h2_text_list,
    "body": body_text
}
print(page_data)