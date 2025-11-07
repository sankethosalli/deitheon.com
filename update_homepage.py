import os
import glob
import json
import random
from datetime import datetime

def get_featured_articles():
    """Get 2 random articles from each category"""
    categories = ['philosophy', 'science', 'psychology', 'society', 'culture', 'food', 'tech', 'politics']
    featured_articles = {}
    
    for category in categories:
        articles = []
        for article_path in glob.glob(f'articles/{category}/*.html'):
            if 'index.html' in article_path:
                continue
                
            with open(article_path, 'r') as f:
                content = f.read()
                
            title = content.split('<title>')[1].split('</title>')[0].split(' - ')[0]
            description = content.split('<meta name="description" content="')[1].split('">')[0]
            date = content.split('<time datetime="')[1].split('"')[0]
            
            articles.append({
                'title': title,
                'description': description,
                'url': f'/articles/{category}/{os.path.basename(article_path)}',
                'date': date,
                'category': category.title()
            })
        
        # Get 2 random articles from this category
        featured_articles[category] = random.sample(articles, 2)
    
    return featured_articles

def generate_featured_section():
    """Generate HTML for featured articles section"""
    featured_articles = get_featured_articles()
    
    sections_html = []
    for category, articles in featured_articles.items():
        section_html = f"""
        <section class="py-12">
            <div class="flex justify-between items-center mb-8">
                <h2 class="text-2xl md:text-3xl font-bold">{category.title()}</h2>
                <a href="/articles/{category}" class="text-blue-600 dark:text-blue-400 hover:underline">View All →</a>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                {''.join(generate_article_card(article) for article in articles)}
            </div>
        </section>"""
        sections_html.append(section_html)
    
    return '\n'.join(sections_html)

def generate_article_card(article):
    """Generate HTML for a single article card"""
    return f"""
    <article class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
        <div class="p-6">
            <div class="text-sm text-blue-600 dark:text-blue-400 mb-2">{article['category']}</div>
            <h3 class="text-xl font-bold mb-2">
                <a href="{article['url']}" class="hover:text-blue-600 dark:hover:text-blue-400">{article['title']}</a>
            </h3>
            <p class="text-gray-600 dark:text-gray-300 mb-4">{article['description']}</p>
            <div class="flex justify-between items-center">
                <time datetime="{article['date']}" class="text-sm text-gray-500 dark:text-gray-400">
                    {datetime.strptime(article['date'], '%Y-%m-%d').strftime('%B %d, %Y')}
                </time>
                <a href="{article['url']}" class="text-blue-600 dark:text-blue-400 hover:underline">Read More →</a>
            </div>
        </div>
    </article>"""

def update_index_html():
    """Update index.html with featured articles"""
    with open('index.html', 'r') as f:
        content = f.read()
    
    # Find the featured articles div and replace its content
    start_marker = '<div id="featured-articles">'
    end_marker = '</div>'
    featured_section = generate_featured_section()
    
    before_content = content.split(start_marker)[0]
    after_content = content.split(end_marker, 1)[1]
    new_content = before_content + start_marker + featured_section + end_marker + after_content
    
    with open('index.html', 'w') as f:
        f.write(new_content)

if __name__ == '__main__':
    update_index_html()