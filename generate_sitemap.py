import os
import glob
from datetime import datetime

def generate_sitemap():
    """Generate sitemap.xml with all pages"""
    
    # Base URLs
    base_urls = [
        {'loc': 'https://deitheon.com/', 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': 'https://deitheon.com/about.html', 'priority': '0.8', 'changefreq': 'monthly'},
        {'loc': 'https://deitheon.com/contact.html', 'priority': '0.8', 'changefreq': 'monthly'},
        {'loc': 'https://deitheon.com/articles/', 'priority': '0.9', 'changefreq': 'daily'},
    ]
    
    # Category URLs
    categories = ['philosophy', 'science', 'psychology', 'society', 'culture', 'food', 'tech', 'politics']
    for category in categories:
        base_urls.append({
            'loc': f'https://deitheon.com/articles/{category}/',
            'priority': '0.8',
            'changefreq': 'daily'
        })
    
    # Article URLs
    for category in categories:
        for article_path in glob.glob(f'articles/{category}/*.html'):
            if 'index.html' not in article_path:
                article_url = f'https://deitheon.com/{article_path}'
                base_urls.append({
                    'loc': article_url,
                    'priority': '0.7',
                    'changefreq': 'monthly'
                })
    
    # Generate sitemap XML
    today = datetime.now().strftime('%Y-%m-%d')
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">"""
    
    for url in base_urls:
        sitemap_content += f"""
    <url>
        <loc>{url['loc']}</loc>
        <lastmod>{today}</lastmod>
        <changefreq>{url['changefreq']}</changefreq>
        <priority>{url['priority']}</priority>
    </url>"""
    
    sitemap_content += """
</urlset>"""
    
    # Write sitemap file
    with open('sitemap.xml', 'w') as f:
        f.write(sitemap_content)

if __name__ == '__main__':
    generate_sitemap()