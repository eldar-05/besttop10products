import requests
from bs4 import BeautifulSoup
import os
from datetime import date, timedelta
import re

def scrape_techcrunch():
    """Собирает топ-10 новостей с сайта TechCrunch."""
    print("Начинаем парсинг TechCrunch...")
    url = "https://techcrunch.com/"
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
    articles = soup.find_all('article', class_='post--pe-latest')

    print(f"Найдено статей на странице: {len(articles)}")

    if not articles:
        articles = soup.find_all('div', class_='river-unit')
        print(f"Попробовали альтернативный селектор. Найдено: {len(articles)}")
    
    if not articles:
        print("Не удалось найти статьи на главной странице TechCrunch.")
        return []

    top_10_articles = []
    for i, article in enumerate(articles[:10]):
        title_element = article.find('a', class_='post-block__title__link')
        if not title_element: continue

        title = title_element.text.strip()
        link = title_element['href']

        summary_element = article.find('div', class_='post-block__content')
        summary = summary_element.text.strip() if summary_element else 'Нет описания.'
        
        top_10_articles.append({'title': title, 'link': link, 'summary': summary})
        print(f"Статья #{i+1} добавлена: {title}")
    
    return top_10_articles

def create_markdown_file(articles, target_date=None):
    """Создает Markdown-файл с собранными данными."""
    if not articles:
        print("Нет данных для создания файла.")
        return

    if not target_date:
        target_date = date.today()

    formatted_date = target_date.strftime("%Y-%m-%d")
    
    folder_name = "_posts"
    os.makedirs(folder_name, exist_ok=True)
    file_path = os.path.join(folder_name, f'{formatted_date}-top-10.md')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f'---\n')
        f.write(f'layout: default\n')
        f.write(f'title: "Топ-10 технологий на {formatted_date}"\n')
        f.write(f'date: {formatted_date}\n')
        f.write(f'---\n\n')

        f.write(f'# Топ-10 новых технологий на {formatted_date}\n\n')

        for i, article in enumerate(articles, 1):
            f.write(f'## {i}. [{article["title"]}]({article["link"]})\n\n')
            f.write(f'**Описание:** {article["summary"]}\n\n')
            f.write('---\n\n')

    print(f"Markdown-файл успешно создан: {file_path}")

if __name__ == "__main__":
    tech_articles = scrape_techcrunch()
    create_markdown_file(tech_articles)