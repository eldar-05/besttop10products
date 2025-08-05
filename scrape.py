import requests
import os
from datetime import date, timedelta

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

def get_top_tech_news():
    """Получает топ-10 релевантных новостей о технологиях и стартапах с News API."""
    if not NEWS_API_KEY:
        print("Ошибка: Ключ API не найден. Убедитесь, что он установлен в secrets GitHub.")
        return []
        
    print("Начинаем получать новости через News API...")
    
    # Новый, более точный запрос к API
    # Используем конкретные источники, чтобы избежать нерелевантного контента
    sources = "techcrunch,the-verge,ars-technica,wired,recode"
    url = f"https://newsapi.org/v2/everything?sources={sources}&sortBy=publishedAt&pageSize=10&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        articles = []
        for article in data['articles']:
            if not article.get('title') or not article.get('url') or not article.get('description'):
                continue
            
            title = article['title']
            link = article['url']
            summary = article['description']
            articles.append({'title': title, 'link': link, 'summary': summary})
            
            if len(articles) >= 10:
                break
        
        print(f"Получено {len(articles)} релевантных статей.")
        
        return articles
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных с API: {e}")
        return []

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
    tech_articles = get_top_tech_news()
    create_markdown_file(tech_articles)