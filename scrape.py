import requests
from bs4 import BeautifulSoup
import os
from datetime import date
import re

def scrape_habr():
    """Собирает топ-10 новостей с Habr."""
    url = "https://habr.com/ru/feed/posts/all/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении страницы: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', class_='tm-articles-list__item')

    top_10_articles = []
    for article in articles[:10]:
        title_element = article.find('a', class_='tm-title__link')
        
        if not title_element:
            continue  

        title = title_element.text.strip()
        link = "https://habr.com" + title_element['href']

        summary_element = article.find('div', class_='article-formatted-body')
        summary = summary_element.text.strip() if summary_element else 'Нет описания.'
        summary = re.sub(r'[\r\n\t]+', ' ', summary)
        
        top_10_articles.append({'title': title, 'link': link, 'summary': summary})

    return top_10_articles

def create_markdown_file(articles):
    """Создает Markdown-файл с собранными данными."""
    if not articles:
        print("Нет данных для создания файла.")
        return

    today = date.today().strftime("%Y-%m-%d")
    
    folder_name = f"_posts"
    os.makedirs(folder_name, exist_ok=True)
    file_path = os.path.join(folder_name, f'{today}-top-10.md')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f'---\n')
        f.write(f'layout: post\n')
        f.write(f'title: "Топ-10 технологий на {today}"\n')
        f.write(f'date: {today}\n')
        f.write(f'---\n\n')

        f.write(f'# Топ-10 новых технологий на {today}\n\n')

        for i, article in enumerate(articles, 1):
            f.write(f'## {i}. [{article["title"]}]({article["link"]})\n\n')
            f.write(f'**Описание:** {article["summary"]}\n\n')
            f.write('---\n\n')

    print(f"Markdown-файл успешно создан: {file_path}")

if __name__ == "__main__":
    tech_articles = scrape_habr()
    create_markdown_file(tech_articles)