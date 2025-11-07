#!/usr/bin/env python3
"""
Generate 20+ comprehensive, well-written articles per category for DeiTheon
Uses article_content.py for detailed content
"""
import os
import sys
from datetime import datetime, timedelta
import random

# Import the rich content database
from article_content import ARTICLES_DATA, ADDITIONAL_TOPICS, generate_generic_article, generate_section_content

# Updated categories with exactly 20 articles each
categories = {
    'philosophy': {'display': 'Philosophy', 'count': 20},
    'science': {'display': 'Science', 'count': 20},
    'psychology': {'display': 'Psychology', 'count': 20},
    'society': {'display': 'Society', 'count': 20},
    'culture': {'display': 'Culture', 'count': 20},
    'food': {'display': 'Food', 'count': 20},
    'tech': {'display': 'Technology', 'count': 20},
    'politics': {'display': 'Politics', 'count': 20},
}

authors = [
    'Dr. Sarah Mitchell',
    'Prof. James Chen',
    'Dr. Maya Patel',
    'Alex Rodriguez',
    'Dr. Emily Thompson',
    'Prof. David Kim',
    'Dr. Rachel Foster',
    'Michael Zhang'
]

# HTML template with component-based navbar/footer
article_template = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Deitheon</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <link rel="icon" href="/assets/images/favicon.png" type="image/x-icon">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://deitheon.com/articles/{category}/{slug}.html">
    <meta property="og:title" content="{title} | Deitheon">
    <meta property="og:description" content="{description}">

    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://deitheon.com/articles/{category}/{slug}.html">
    <meta property="twitter:title" content="{title} | Deitheon">
    <meta property="twitter:description" content="{description}">

    <!-- Styles -->
    <link rel="stylesheet" href="/assets/css/styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
    <script>
        if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
            document.documentElement.classList.add('dark');
        }} else {{
            document.documentElement.classList.remove('dark');
        }}
    </script>
</head>
<body class="min-h-screen bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-200">
    <!-- Navbar Container (loaded dynamically) -->
    <div id="navbar-container"></div>

    <!-- Article Content -->
    <main class="container mx-auto px-4 max-w-4xl pt-24 pb-16">
        <!-- Breadcrumbs -->
        <nav class="text-sm mb-8" aria-label="Breadcrumb">
            <ol class="list-none p-0 flex flex-wrap items-center space-x-2">
                <li><a href="/" class="text-blue-600 dark:text-blue-400 hover:underline">Home</a></li>
                <li class="text-gray-500 dark:text-gray-400">/</li>
                <li><a href="/articles" class="text-blue-600 dark:text-blue-400 hover:underline">Articles</a></li>
                <li class="text-gray-500 dark:text-gray-400">/</li>
                <li><a href="/articles/{category}" class="text-blue-600 dark:text-blue-400 hover:underline">{category_title}</a></li>
                <li class="text-gray-500 dark:text-gray-400">/</li>
                <li class="text-gray-600 dark:text-gray-300">{title}</li>
            </ol>
        </nav>

        <!-- Article Header -->
        <header class="mb-12">
            <h1 class="text-4xl md:text-5xl font-bold mb-6 leading-tight">{title}</h1>
            <div class="flex flex-wrap items-center gap-4 text-sm text-gray-600 dark:text-gray-400 mb-6">
                <span><i class="fas fa-user mr-2"></i>{author}</span>
                <span>•</span>
                <time datetime="{date}"><i class="fas fa-calendar mr-2"></i>{date_formatted}</time>
                <span>•</span>
                <span><i class="fas fa-clock mr-2"></i>{read_time} min read</span>
            </div>
            <p class="text-xl text-gray-700 dark:text-gray-300 leading-relaxed">{description}</p>
        </header>

        <!-- Table of Contents -->
        <aside class="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-700 p-6 rounded-lg mb-12 border border-blue-100 dark:border-gray-600">
            <h2 class="text-lg font-bold mb-4 flex items-center">
                <i class="fas fa-list-ul mr-2 text-blue-600 dark:text-blue-400"></i>
                Table of Contents
            </h2>
            <nav>
                <ol class="list-decimal list-inside space-y-2">
                    {toc}
                </ol>
            </nav>
        </aside>

        <!-- Article Content -->
        <article class="prose prose-lg dark:prose-invert max-w-none prose-headings:font-bold prose-h2:text-3xl prose-h2:mt-12 prose-h2:mb-6 prose-p:mb-4 prose-p:leading-relaxed prose-a:text-blue-600 dark:prose-a:text-blue-400 prose-a:no-underline hover:prose-a:underline">
            {content}
        </article>

        <!-- Tags -->
        <div class="mt-16 pt-8 border-t border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-bold mb-4 flex items-center">
                <i class="fas fa-tags mr-2 text-blue-600 dark:text-blue-400"></i>
                Tags
            </h3>
            <div class="flex flex-wrap gap-2">
                {tags}
            </div>
        </div>

        <!-- Author Bio -->
        <div class="mt-12 p-6 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-bold mb-3">About the Author</h3>
            <p class="text-gray-700 dark:text-gray-300"><strong>{author}</strong> is a contributor to DeiTheon, specializing in {category_title} and related topics.</p>
        </div>

        <!-- Share Section -->
        <div class="mt-12 text-center">
            <p class="text-gray-600 dark:text-gray-400 mb-4">Found this article helpful? Share it with others!</p>
            <div class="flex justify-center gap-4">
                <a href="https://twitter.com/intent/tweet?url=https://deitheon.com/articles/{category}/{slug}.html&text={title}" 
                   target="_blank" rel="noopener"
                   class="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition">
                    <i class="fab fa-twitter mr-2"></i>Share on Twitter
                </a>
                <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://deitheon.com/articles/{category}/{slug}.html" 
                   target="_blank" rel="noopener"
                   class="px-6 py-3 bg-blue-700 text-white rounded-lg hover:bg-blue-800 transition">
                    <i class="fab fa-linkedin mr-2"></i>Share on LinkedIn
                </a>
            </div>
        </div>
    </main>

    <!-- Footer Container (loaded dynamically) -->
    <div id="footer-container"></div>

    <!-- Component Loader & Core Scripts -->
    <script src="/assets/js/components.js"></script>
    <script>
        // Reading Progress
        const readingProgress = document.getElementById('readingProgress');
        if (readingProgress) {{
            window.addEventListener('scroll', () => {{
                const windowHeight = document.documentElement.clientHeight;
                const fullHeight = document.documentElement.scrollHeight - windowHeight;
                const scrolled = window.scrollY;
                const progress = (scrolled / fullHeight) * 100;
                readingProgress.style.width = `${{progress}}%`;
            }});
        }}
    </script>
</body>
</html>"""

def slugify(text):
    """Convert text to URL-friendly slug"""
    return text.lower().replace(' ', '-').replace(',', '').replace(':', '').replace('?', '').replace('\'', '').replace('(', '').replace(')', '')

def generate_toc_html(sections):
    """Generate table of contents HTML"""
    toc_items = []
    for i, section_title in enumerate(sections.keys(), 1):
        slug = slugify(section_title)
        toc_items.append(f'<li><a href="#{slug}" class="text-blue-600 dark:text-blue-400 hover:underline">{section_title}</a></li>')
    return '\n'.join(toc_items)

def generate_content_html(sections):
    """Generate article content HTML from sections"""
    content_parts = []
    for section_title, section_content in sections.items():
        content_parts.append(generate_section_content(section_title, section_content, is_detailed=True))
    return '\n'.join(content_parts)

def generate_tags_html(tags):
    """Generate tags HTML"""
    tag_links = []
    for tag in tags:
        slug = slugify(tag)
        tag_links.append(
            f'<a href="/tags/{slug}" class="px-4 py-2 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-sm hover:bg-blue-200 dark:hover:bg-blue-800 transition">{tag}</a>'
        )
    return '\n'.join(tag_links)

def generate_articles():
    """Generate 20+ articles for each category with rich content"""
    base_date = datetime(2025, 11, 8)
    all_articles = []
    
    print("🚀 Generating comprehensive articles for DeiTheon...")
    print("=" * 60)
    
    for category, config in categories.items():
        category_path = f'articles/{category}'
        if not os.path.exists(category_path):
            os.makedirs(category_path)
        
        print(f"\n📁 {config['display']} ({config['count']} articles)")
        
        article_count = 0
        
        # First, add detailed articles from ARTICLES_DATA
        if category in ARTICLES_DATA:
            for article_data in ARTICLES_DATA[category]:
                if article_count >= config['count']:
                    break
                
                date = base_date - timedelta(days=random.randint(0, 365))
                read_time = random.randint(8, 15)
                
                article_info = {
                    'title': article_data['title'],
                    'slug': article_data['slug'],
                    'category': category,
                    'category_title': config['display'],
                    'author': random.choice(authors),
                    'date': date.strftime('%Y-%m-%d'),
                    'date_formatted': date.strftime('%B %d, %Y'),
                    'description': article_data['description'],
                    'keywords': ', '.join(article_data['tags']),
                    'read_time': read_time,
                    'toc': generate_toc_html(article_data['sections']),
                    'content': generate_content_html(article_data['sections']),
                    'tags': generate_tags_html(article_data['tags'])
                }
                
                # Generate article HTML
                article_html = article_template.format(**article_info)
                
                # Save article
                article_path = f'{category_path}/{article_info["slug"]}.html'
                with open(article_path, 'w', encoding='utf-8') as f:
                    f.write(article_html)
                
                all_articles.append({
                    'title': article_info['title'],
                    'category': category,
                    'slug': article_info['slug'],
                    'url': f'/articles/{category}/{article_info["slug"]}.html',
                    'date': article_info['date']
                })
                
                article_count += 1
                print(f"   ✅ {article_info['title'][:60]}...")
        
        # Then, add generic articles from ADDITIONAL_TOPICS to reach 20
        if category in ADDITIONAL_TOPICS:
            for topic_title in ADDITIONAL_TOPICS[category]:
                if article_count >= config['count']:
                    break
                
                date = base_date - timedelta(days=random.randint(0, 365))
                slug = slugify(topic_title)
                
                # Generate generic but structured content
                sections = generate_generic_article(category, topic_title)
                tags = [config['display'], 'Analysis', 'Research', 'Insights']
                
                article_info = {
                    'title': topic_title,
                    'slug': slug,
                    'category': category,
                    'category_title': config['display'],
                    'author': random.choice(authors),
                    'date': date.strftime('%Y-%m-%d'),
                    'date_formatted': date.strftime('%B %d, %Y'),
                    'description': f'An in-depth exploration of {topic_title.lower()}, examining key concepts, challenges, and future directions.',
                    'keywords': f'{topic_title}, {config["display"]}, research, analysis',
                    'read_time': random.randint(6, 12),
                    'toc': generate_toc_html(sections),
                    'content': generate_content_html(sections),
                    'tags': generate_tags_html(tags)
                }
                
                # Generate article HTML
                article_html = article_template.format(**article_info)
                
                # Save article
                article_path = f'{category_path}/{slug}.html'
                with open(article_path, 'w', encoding='utf-8') as f:
                    f.write(article_html)
                
                all_articles.append({
                    'title': article_info['title'],
                    'category': category,
                    'slug': slug,
                    'url': f'/articles/{category}/{slug}.html',
                    'date': article_info['date']
                })
                
                article_count += 1
                print(f"   ✅ {topic_title[:60]}...")
    
    print("\n" + "=" * 60)
    print(f"✨ Generated {len(all_articles)} total articles!")
    print("=" * 60)
    
    # Generate sitemap
    generate_sitemap(all_articles)
    
    return all_articles

def generate_sitemap(articles):
    """Generate sitemap.xml with all articles"""
    sitemap_template = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://deitheon.com/</loc>
        <lastmod>2025-11-08</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://deitheon.com/categories</loc>
        <lastmod>2025-11-08</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://deitheon.com/articles</loc>
        <lastmod>2025-11-08</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.9</priority>
    </url>
    {urls}
</urlset>"""
    
    urls = []
    for article in articles:
        url_entry = f"""    <url>
        <loc>https://deitheon.com{article['url']}</loc>
        <lastmod>{article['date']}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>"""
        urls.append(url_entry)
    
    sitemap_content = sitemap_template.format(urls='\n'.join(urls))
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print("\n📄 Sitemap.xml updated successfully!")

if __name__ == '__main__':
    try:
        articles = generate_articles()
        print(f"\n🎉 Article generation complete! {len(articles)} articles created.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
