import os
from datetime import datetime, timedelta
import random
import json

# Article templates and content structure
categories = {
    'philosophy': {
        'topics': ['Metaphysics', 'Ethics', 'Epistemology', 'Logic', 'Aesthetics', 'Political Philosophy', 'Philosophy of Mind',
                  'Existentialism', 'Phenomenology', 'Ancient Philosophy', 'Modern Philosophy', 'Eastern Philosophy'],
        'count': 75
    },
    'science': {
        'topics': ['Physics', 'Biology', 'Chemistry', 'Astronomy', 'Neuroscience', 'Quantum Mechanics', 'Evolution',
                  'Climate Science', 'Genetics', 'Mathematics', 'Computer Science', 'Earth Science'],
        'count': 75
    },
    'psychology': {
        'topics': ['Cognitive Psychology', 'Behavioral Psychology', 'Social Psychology', 'Clinical Psychology',
                  'Developmental Psychology', 'Personality Psychology', 'Neuropsychology', 'Mental Health'],
        'count': 75
    },
    'society': {
        'topics': ['Social Issues', 'Education', 'Urban Development', 'Community', 'Social Justice', 'Economics',
                  'Human Rights', 'Social Media', 'Relationships', 'Work Culture'],
        'count': 60
    },
    'culture': {
        'topics': ['Art', 'Music', 'Literature', 'Film', 'Fashion', 'Architecture', 'Cultural Identity',
                  'Traditions', 'Popular Culture', 'Cultural Change'],
        'count': 60
    },
    'food': {
        'topics': ['Cuisine', 'Nutrition', 'Cooking Techniques', 'Food History', 'Sustainable Food',
                  'Restaurant Culture', 'Diet', 'Food Science'],
        'count': 45
    },
    'tech': {
        'topics': ['Artificial Intelligence', 'Blockchain', 'Cybersecurity', 'Software Development',
                  'Hardware', 'Internet', 'Mobile Technology', 'Future Tech'],
        'count': 60
    },
    'politics': {
        'topics': ['Political Theory', 'International Relations', 'Government', 'Policy',
                  'Democracy', 'Political Movements', 'Elections', 'Geopolitics'],
        'count': 50
    }
}

# HTML template
article_template = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - {category} | Deitheon</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://deitheon.com/articles/{category}/{slug}.html">
    <meta property="og:title" content="{title} - {category} | Deitheon">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="https://deitheon.com/assets/images/articles/{category}/{slug}.jpg">

    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://deitheon.com/articles/{category}/{slug}.html">
    <meta property="twitter:title" content="{title} - {category} | Deitheon">
    <meta property="twitter:description" content="{description}">
    <meta property="twitter:image" content="https://deitheon.com/assets/images/articles/{category}/{slug}.jpg">

    <!-- Article Schema -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{title}",
        "description": "{description}",
        "image": "https://deitheon.com/assets/images/articles/{category}/{slug}.jpg",
        "author": {{
            "@type": "Person",
            "name": "{author}"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "Deitheon",
            "logo": {{
                "@type": "ImageObject",
                "url": "https://deitheon.com/assets/images/logo.png"
            }}
        }},
        "datePublished": "{date}",
        "dateModified": "{date}"
    }}
    </script>

    <!-- Styles -->
    <link rel="stylesheet" href="/assets/css/styles.css">
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
</head>
<body class="min-h-screen bg-white dark:bg-gray-900">
    <!-- Reading Progress Bar -->
    <div class="fixed top-0 left-0 w-full h-1 bg-gray-200 dark:bg-gray-700 z-50">
        <div id="readingProgress" class="h-full bg-blue-600 w-0 transition-all duration-150"></div>
    </div>

    <!-- Article Content -->
    <main class="container-custom pt-20">
        <!-- Breadcrumbs -->
        <nav class="text-sm mb-8" aria-label="Breadcrumb">
            <ol class="list-none p-0 flex flex-wrap items-center space-x-2">
                <li><a href="/" class="text-blue-600 dark:text-blue-400">Home</a></li>
                <li class="text-gray-500 dark:text-gray-400">/</li>
                <li><a href="/articles" class="text-blue-600 dark:text-blue-400">Articles</a></li>
                <li class="text-gray-500 dark:text-gray-400">/</li>
                <li><a href="/articles/{category}" class="text-blue-600 dark:text-blue-400">{category_title}</a></li>
                <li class="text-gray-500 dark:text-gray-400">/</li>
                <li class="text-gray-600 dark:text-gray-300">{title}</li>
            </ol>
        </nav>

        <!-- Article Header -->
        <header class="mb-12">
            <h1 class="text-4xl md:text-5xl font-bold mb-4">{title}</h1>
            <div class="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-300">
                <span>By {author}</span>
                <span>•</span>
                <time datetime="{date}">{date_formatted}</time>
                <span>•</span>
                <span>{read_time} min read</span>
            </div>
        </header>

        <!-- Table of Contents -->
        <aside class="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg mb-8">
            <h2 class="text-lg font-bold mb-4">Table of Contents</h2>
            <nav>
                <ol class="list-decimal list-inside space-y-2">
                    {toc}
                </ol>
            </nav>
        </aside>

        <!-- Article Content -->
        <article class="prose prose-lg dark:prose-invert max-w-none">
            {content}
        </article>

        <!-- Tags -->
        <div class="mt-12">
            <h3 class="text-lg font-bold mb-4">Tags</h3>
            <div class="flex flex-wrap gap-2">
                {tags}
            </div>
        </div>

        <!-- Related Articles -->
        <section class="mt-16">
            <h3 class="text-2xl font-bold mb-8">Related Articles</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <!-- Related article cards will be populated here -->
            </div>
        </section>
    </main>

    <!-- Scripts -->
    <script src="/assets/js/main.js" defer></script>
    <script>
        // Reading Progress
        const readingProgress = document.getElementById('readingProgress');
        window.addEventListener('scroll', () => {{
            const windowHeight = document.documentElement.clientHeight;
            const fullHeight = document.documentElement.scrollHeight - windowHeight;
            const scrolled = window.scrollY;
            const progress = (scrolled / fullHeight) * 100;
            readingProgress.style.width = `${{progress}}%`;
        }});
    </script>
</body>
</html>"""

def slugify(text):
    """Convert text to URL-friendly slug"""
    return text.lower().replace(' ', '-').replace(',', '').replace(':', '')

def generate_articles():
    """Generate articles for each category"""
    base_date = datetime(2025, 11, 7)
    authors = ['John Doe', 'Jane Smith', 'Alex Johnson', 'Maria Garcia', 'David Chen']
    all_articles = []
    
    for category, data in categories.items():
        category_path = f'articles/{category}'
        if not os.path.exists(category_path):
            os.makedirs(category_path)
            
        for i in range(data['count']):
            topic = random.choice(data['topics'])
            date = base_date - timedelta(days=random.randint(0, 365))
            title = f"The {topic} Revolution: A New Perspective"
            slug = slugify(title)
            
            article_data = {
                'title': title,
                'category': category,
                'category_title': category.title(),
                'slug': slug,
                'author': random.choice(authors),
                'date': date.strftime('%Y-%m-%d'),
                'date_formatted': date.strftime('%B %d, %Y'),
                'description': f"Exploring the latest developments and insights in {topic.lower()}.",
                'keywords': f"{topic.lower()}, {category}, research, analysis, insights",
                'read_time': random.randint(5, 20),
                'toc': '\n'.join([
                    f'<li><a href="#{slugify(section)}" class="text-blue-600 dark:text-blue-400 hover:underline">{section}</a></li>'
                    for section in ['Introduction', 'Background', 'Key Concepts', 'Analysis', 'Implications', 'Conclusion']
                ]),
                'content': '\n'.join([
                    f'<section id="{slugify(section)}"><h2>{section}</h2><p>Content for {section.lower()} section...</p></section>'
                    for section in ['Introduction', 'Background', 'Key Concepts', 'Analysis', 'Implications', 'Conclusion']
                ]),
                'tags': '\n'.join([
                    f'<a href="/tags/{slugify(tag)}" class="px-3 py-1 bg-gray-100 dark:bg-gray-800 rounded-full text-sm hover:bg-gray-200 dark:hover:bg-gray-700">{tag}</a>'
                    for tag in [topic, category.title(), 'Research', 'Analysis']
                ])
            }
            
            # Generate article HTML
            article_html = article_template.format(**article_data)
            
            # Save article
            article_path = f'{category_path}/{slug}.html'
            with open(article_path, 'w') as f:
                f.write(article_html)
            
            all_articles.append({
                'title': title,
                'category': category,
                'slug': slug,
                'url': f'/articles/{category}/{slug}.html',
                'date': article_data['date']
            })
    
    # Generate sitemap
    generate_sitemap(all_articles)

def generate_sitemap(articles):
    """Generate sitemap.xml with all articles"""
    sitemap_template = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://deitheon.com/</loc>
        <lastmod>2025-11-07</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
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
    with open('sitemap.xml', 'w') as f:
        f.write(sitemap_content)

if __name__ == '__main__':
    generate_articles()