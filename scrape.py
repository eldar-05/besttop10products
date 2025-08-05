import requests
from bs4 import BeautifulSoup
import os
from datetime import date, timedelta
import re

def scrape_the_verge():
    """Собирает топ-10 новостей с сайта The Verge."""
    print("Начинаем парсинг The Verge...")
    url = "https://www.theverge.com/tech"
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
    articles = soup.find_all('div', class_='c-compact-river__entry')
    print(f"Найдено статей на странице: {len(articles)}")

    if not articles:
        print("Не удалось найти статьи на главной странице The Verge.")
        return []

    top_10_articles = []
    for i, article in enumerate(articles[:10]):
        title_element = article.find('h2', class_='c-entry-box--compact__title')
        if not title_element: 
            print(f"Статья #{i+1}: Заголовок не найден. Пропускаем.")
            continue

        title_link = title_element.find('a')
        if not title_link:
            print(f"Статья #{i+1}: Ссылка на заголовок не найдена. Пропускаем.")
            continue
        
        title = title_link.text.strip()
        link = title_link['href']

        summary_element = article.find('p', class_='c-entry-box--compact__byline')
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
    tech_articles = scrape_the_verge()
    create_markdown_file(tech_articles)