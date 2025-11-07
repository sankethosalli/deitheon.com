#!/usr/bin/env python3
"""
Update all HTML pages to use component system
"""
import re
import os

def update_html_file(filepath, page_title="DeiTheon"):
    """Update an HTML file to use component-based navbar and footer"""
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Don't update if already using components
    if 'navbar-container' in content:
        print(f"   ⏭️  {filepath} already uses components, skipping")
        return False
    
    # Extract the head section (keep meta tags, title, etc.)
    head_match = re.search(r'<head>(.*?)</head>', content, re.DOTALL)
    if not head_match:
        print(f"   ❌ Could not find <head> in {filepath}")
        return False
    
    head_content = head_match.group(1)
    
    # Ensure favicon is present
    if 'favicon' not in head_content:
        # Find the viewport meta tag and add favicon after it
        head_content = re.sub(
            r'(<meta name="viewport"[^>]+>)',
            r'\1\n    <link rel="icon" href="/assets/images/favicon.png" type="image/x-icon">',
            head_content
        )
    
    # Extract main content (between navbar and footer)
    # Find the start of main content (after </header> or after navbar)
    main_start = content.find('</header>')
    if main_start == -1:
        main_start = content.find('</nav>')
    if main_start == -1:
        main_start = content.find('<main')
        
    # Find the start of footer
    footer_start = content.find('<footer')
    if footer_start == -1:
        footer_start = content.find('<!-- Footer')
    
    if main_start == -1 or footer_start == -1:
        print(f"   ❌ Could not locate main content in {filepath}")
        return False
    
    # Extract main content
    main_content = content[main_start:footer_start].strip()
    
    # Remove opening </header> or </nav> tag from main content
    main_content = re.sub(r'^</header>\s*', '', main_content)
    main_content = re.sub(r'^</nav>\s*', '', main_content)
    
    # Find all <script> tags at the end (before </body>)
    script_match = re.search(r'(<script.*?</script>)\s*</body>', content, re.DOTALL)
    custom_scripts = ''
    if script_match:
        scripts = script_match.group(1)
        # Only keep custom scripts, not the navbar/footer scripts
        if 'themeToggle' not in scripts and 'components.js' not in scripts:
            custom_scripts = scripts
    
    # Build new HTML
    new_html = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
{head_content}
</head>
<body class="bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-200 min-h-screen flex flex-col">
    <!-- Navbar Container -->
    <div id="navbar-container"></div>

{main_content}

    <!-- Footer Container -->
    <div id="footer-container"></div>

    <!-- Component Loader -->
    <script src="/assets/js/components.js"></script>
{custom_scripts}
</body>
</html>"""
    
    # Write the updated content
    with open(filepath, 'w') as f:
        f.write(new_html)
    
    print(f"   ✅ Updated {filepath}")
    return True

def main():
    """Update all main pages to use components"""
    pages = [
        '/home/un6/github/sankethosalli/deitheon.com/categories.html',
        '/home/un6/github/sankethosalli/deitheon.com/about.html',
        '/home/un6/github/sankethosalli/deitheon.com/contact.html',
        '/home/un6/github/sankethosalli/deitheon.com/articles/index.html',
    ]
    
    print("🔄 Updating pages to use component system...")
    updated = 0
    for page in pages:
        if os.path.exists(page):
            if update_html_file(page):
                updated += 1
        else:
            print(f"   ⚠️  File not found: {page}")
    
    print(f"\n✨ Updated {updated} pages to use components!")

if __name__ == '__main__':
    main()
