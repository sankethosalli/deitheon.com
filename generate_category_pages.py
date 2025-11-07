import os
import glob
import json
from datetime import datetime

def create_category_index(category):
    """Create index.html for a specific category"""
    
    # Get all articles in this category
    articles = []
    for article_path in glob.glob(f'articles/{category}/*.html'):
        if 'index.html' in article_path:
            continue
            
        with open(article_path, 'r') as f:
            content = f.read()
            
        # Extract title and description from meta tags
        title = content.split('<title>')[1].split('</title>')[0].split(' - ')[0]
        description = content.split('<meta name="description" content="')[1].split('">')[0]
        date = content.split('<time datetime="')[1].split('"')[0]
        
        articles.append({
            'title': title,
            'description': description,
            'url': f'/articles/{category}/{os.path.basename(article_path)}',
            'date': date
        })
    
    # Sort articles by date
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    # Generate article cards HTML
    article_cards = []
    for article in articles:
        card = f"""
            <article class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
                <div class="p-6">
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
        article_cards.append(card)
    
    # Create the category index page
    category_title = category.title()
    index_html = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category_title} Articles - Deitheon</title>
    <meta name="description" content="Explore our collection of articles about {category_title.lower()}.">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://deitheon.com/articles/{category}/">
    <meta property="og:title" content="{category_title} Articles - Deitheon">
    <meta property="og:description" content="Explore our collection of articles about {category_title.lower()}.">
    
    <!-- Styles -->
    <link rel="stylesheet" href="/assets/css/styles.css">
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
</head>
<body class="min-h-screen bg-white dark:bg-gray-900">
    <!-- Navbar (same as other pages) -->
    <nav class="navbar">
        <!-- ... navbar content ... -->
    </nav>

    <!-- Main Content -->
    <main class="container-custom pt-20">
        <!-- Breadcrumbs -->
        <nav class="text-sm mb-8" aria-label="Breadcrumb">
            <ol class="list-none p-0 flex flex-wrap items-center space-x-2">
                <li><a href="/" class="text-blue-600 dark:text-blue-400">Home</a></li>
                <li class="text-gray-500 dark:text-gray-400">/</li>
                <li><a href="/articles" class="text-blue-600 dark:text-blue-400">Articles</a></li>
                <li class="text-gray-500 dark:text-gray-400">/</li>
                <li class="text-gray-600 dark:text-gray-300">{category_title}</li>
            </ol>
        </nav>

        <!-- Category Header -->
        <header class="mb-12">
            <h1 class="text-4xl md:text-5xl font-bold mb-4">{category_title} Articles</h1>
            <p class="text-xl text-gray-600 dark:text-gray-300">
                Explore our collection of articles about {category_title.lower()}.
            </p>
        </header>

        <!-- Articles Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {''.join(article_cards)}
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-100 dark:bg-gray-800 mt-20">
        <!-- ... footer content ... -->
    </footer>

    <!-- Scripts -->
    <script src="/assets/js/main.js" defer></script>
</body>
</html>"""
    
    # Write the index file
    with open(f'articles/{category}/index.html', 'w') as f:
        f.write(index_html)

def main():
    """Generate index pages for all categories"""
    categories = ['philosophy', 'science', 'psychology', 'society', 'culture', 'food', 'tech', 'politics']
    for category in categories:
        create_category_index(category)

if __name__ == '__main__':
    main()