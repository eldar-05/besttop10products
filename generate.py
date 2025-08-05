import requests
import datetime
import os

API_KEY = 
URL = "https://newsapi.org/v2/everything"

today = datetime.date.today().isoformat()
filename = f"content/{today}.md"

os.makedirs("content", exist_ok=True)

params = {
    "q": "technology",
    "language": "en",
    "sortBy": "publishedAt",
    "pageSize": 10,
    "apiKey": API_KEY
}
response = requests.get(URL, params=params)
articles = response.json().get("articles", [])

with open(filename, "w", encoding="utf-8") as f:
    f.write(f"# Топ 10 технологий — {today}\n\n")
    for i, article in enumerate(articles, 1):
        title = article["title"]
        desc = article["description"] or "Описание отсутствует."
        link = article["url"]
        f.write(f"{i}. **{title}**\n   {desc}\n   [Читать подробнее]({link})\n\n")

print(f"Файл {filename} создан.")
