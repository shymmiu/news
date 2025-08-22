from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import extracter
import re
from datetime import datetime
import saver

app = Flask(__name__)

def get_news_data():
    """Fetch and extract news URLs"""
    try:
        url = 'https://www.eldiariomontanes.es'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        urls = extracter.extract_urls(soup.prettify())
        return urls
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def extract_article_info(url):
    """Extract title and basic info from URL"""
    # Extract date from URL (format: YYYYMMDD)
    date_match = re.search(r'(\d{8})', url)
    date_str = "Unknown date"
    if date_match:
        date_raw = date_match.group(1)
        try:
            date_obj = datetime.strptime(date_raw, '%Y%m%d')
            date_str = date_obj.strftime('%B %d, %Y')
        except:
            pass
    
    # Fetch the actual page title from the article URL
    title = "Unable to load title"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title_tag = soup.find('title')
            if title_tag:
                # Clean up the title (remove site name and extra text)
                full_title = title_tag.get_text().strip()
                # Remove common suffixes like " | El Diario Montañés" or similar
                title = full_title.split(' | ')[0].split(' - ')[0].strip()
            else:
                # Fallback to URL-based title if no title tag found
                title = url.split('/')[-1].replace('-nt.html', '').replace('-', ' ').title()
    except Exception as e:
        print(f"Error fetching title for {url}: {e}")
        # Fallback to URL-based title
        title = url.split('/')[-1].replace('-nt.html', '').replace('-', ' ').title()
    
    # Extract category from URL using the extracter module
    category = extracter.extract_category(url)
    if not category:
        category = "General"
    
    return {
        'title': title,
        'url': url,
        'date': date_str,
        'category': category
    }

@app.route('/')
def home():
    """Main page showing all news"""
    urls = get_news_data()
    articles = []
    
    # Process only first 15 articles for better performance
    # (fetching titles from individual pages takes time)
    for url in urls[:15]:
        print(f"Fetching title for: {url}")
        article_info = extract_article_info(url)
        articles.append(article_info)
    
    return render_template('index.html', articles=articles)

@app.route('/api/news')
def api_news():
    """API endpoint to get news as JSON"""
    urls = get_news_data()
    articles = []
    
    for url in urls:
        article_info = extract_article_info(url)
        articles.append(article_info)
    
    return jsonify(articles)

@app.route('/category/<category_name>')
def category_news(category_name):
    """Show news filtered by category"""
    urls = get_news_data()
    articles = []
    
    for url in urls:
        article_info = extract_article_info(url)
        if article_info['category'].lower() == category_name.lower():
            articles.append(article_info)
    
    return render_template('category.html', articles=articles, category=category_name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
