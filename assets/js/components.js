/**
 * Component Loader for DeiTheon
 * Dynamically loads navbar and footer components across all pages
 */

// Load component HTML from file
async function loadComponent(componentName, targetId) {
    try {
        const response = await fetch(`/components/${componentName}.html`);
        if (!response.ok) throw new Error(`Failed to load ${componentName}`);
        const html = await response.text();
        const target = document.getElementById(targetId);
        if (target) {
            target.innerHTML = html;
        }
    } catch (error) {
        console.error(`Error loading ${componentName}:`, error);
    }
}

// Initialize all components
async function initComponents() {
    await Promise.all([
        loadComponent('navbar', 'navbar-container'),
        loadComponent('footer', 'footer-container')
    ]);
    
    // After components load, initialize interactive features
    initNavbarFeatures();
}

// Initialize navbar interactive features (search, mobile menu, theme toggle)
function initNavbarFeatures() {
    // ========== Theme Toggle ==========
    const themeToggleBtn = document.getElementById('themeToggle');
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            document.documentElement.classList.toggle('dark');
            localStorage.theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
        });
    }

    // ========== Mobile Menu ==========
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            const isHidden = mobileMenu.classList.toggle('hidden');
            mobileMenu.setAttribute('aria-hidden', isHidden);
        });
    }

    // ========== Article Database ==========
    const articles = [
        { title: "Nature of Consciousness", category: "Philosophy", url: "/articles/philosophy/nature-of-consciousness.html" },
        { title: "The Art Revolution: A New Perspective", category: "Culture", url: "/articles/culture/the-art-revolution-a-new-perspective.html" },
        { title: "The Architecture Revolution", category: "Culture", url: "/articles/culture/the-architecture-revolution-a-new-perspective.html" },
        { title: "The Cultural Change Revolution", category: "Culture", url: "/articles/culture/the-cultural-change-revolution-a-new-perspective.html" },
        { title: "The Cultural Identity Revolution", category: "Culture", url: "/articles/culture/the-cultural-identity-revolution-a-new-perspective.html" },
        { title: "The Fashion Revolution", category: "Culture", url: "/articles/culture/the-fashion-revolution-a-new-perspective.html" },
        { title: "The Film Revolution", category: "Culture", url: "/articles/culture/the-film-revolution-a-new-perspective.html" },
        { title: "The Literature Revolution", category: "Culture", url: "/articles/culture/the-literature-revolution-a-new-perspective.html" },
        { title: "The Music Revolution", category: "Culture", url: "/articles/culture/the-music-revolution-a-new-perspective.html" },
        { title: "The Popular Culture Revolution", category: "Culture", url: "/articles/culture/the-popular-culture-revolution-a-new-perspective.html" },
        { title: "The Traditions Revolution", category: "Culture", url: "/articles/culture/the-traditions-revolution-a-new-perspective.html" },
        { title: "The Cooking Techniques Revolution", category: "Food", url: "/articles/food/the-cooking-techniques-revolution-a-new-perspective.html" },
        { title: "The Cuisine Revolution", category: "Food", url: "/articles/food/the-cuisine-revolution-a-new-perspective.html" },
        { title: "The Diet Revolution", category: "Food", url: "/articles/food/the-diet-revolution-a-new-perspective.html" },
        { title: "The Food History Revolution", category: "Food", url: "/articles/food/the-food-history-revolution-a-new-perspective.html" },
        { title: "The Food Science Revolution", category: "Food", url: "/articles/food/the-food-science-revolution-a-new-perspective.html" },
        { title: "The Nutrition Revolution", category: "Food", url: "/articles/food/the-nutrition-revolution-a-new-perspective.html" },
        { title: "The Restaurant Culture Revolution", category: "Food", url: "/articles/food/the-restaurant-culture-revolution-a-new-perspective.html" },
        { title: "The Sustainable Food Revolution", category: "Food", url: "/articles/food/the-sustainable-food-revolution-a-new-perspective.html" },
        { title: "The Aesthetics Revolution", category: "Philosophy", url: "/articles/philosophy/the-aesthetics-revolution-a-new-perspective.html" },
        { title: "The Ancient Philosophy Revolution", category: "Philosophy", url: "/articles/philosophy/the-ancient-philosophy-revolution-a-new-perspective.html" },
        { title: "The Eastern Philosophy Revolution", category: "Philosophy", url: "/articles/philosophy/the-eastern-philosophy-revolution-a-new-perspective.html" },
        { title: "The Epistemology Revolution", category: "Philosophy", url: "/articles/philosophy/the-epistemology-revolution-a-new-perspective.html" },
        { title: "The Ethics Revolution", category: "Philosophy", url: "/articles/philosophy/the-ethics-revolution-a-new-perspective.html" },
        { title: "The Existentialism Revolution", category: "Philosophy", url: "/articles/philosophy/the-existentialism-revolution-a-new-perspective.html" },
        { title: "The Logic Revolution", category: "Philosophy", url: "/articles/philosophy/the-logic-revolution-a-new-perspective.html" },
        { title: "The Metaphysics Revolution", category: "Philosophy", url: "/articles/philosophy/the-metaphysics-revolution-a-new-perspective.html" },
        { title: "The Modern Philosophy Revolution", category: "Philosophy", url: "/articles/philosophy/the-modern-philosophy-revolution-a-new-perspective.html" },
        { title: "The Phenomenology Revolution", category: "Philosophy", url: "/articles/philosophy/the-phenomenology-revolution-a-new-perspective.html" },
        { title: "The Philosophy of Mind Revolution", category: "Philosophy", url: "/articles/philosophy/the-philosophy-of-mind-revolution-a-new-perspective.html" },
        { title: "The Political Philosophy Revolution", category: "Philosophy", url: "/articles/philosophy/the-political-philosophy-revolution-a-new-perspective.html" }
    ];

    // ========== Live Search Functionality ==========
    function performSearch(query, resultsElement) {
        if (!query || query.length < 2) {
            resultsElement.classList.add('hidden');
            return;
        }

        const filteredArticles = articles.filter(article => 
            article.title.toLowerCase().includes(query.toLowerCase()) ||
            article.category.toLowerCase().includes(query.toLowerCase())
        ).slice(0, 8);

        if (filteredArticles.length === 0) {
            resultsElement.innerHTML = '<div class="p-4 text-gray-500 dark:text-gray-400">No articles found</div>';
            resultsElement.classList.remove('hidden');
            return;
        }

        resultsElement.innerHTML = filteredArticles.map(article => `
            <a href="${article.url}" class="block p-4 hover:bg-gray-50 dark:hover:bg-gray-700 transition border-b border-gray-200 dark:border-gray-700 last:border-0">
                <div class="text-xs text-blue-600 dark:text-blue-400 mb-1">${article.category}</div>
                <div class="font-semibold text-gray-800 dark:text-gray-200">${article.title}</div>
            </a>
        `).join('');
        resultsElement.classList.remove('hidden');
    }

    // Desktop search
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    if (searchInput && searchResults) {
        searchInput.addEventListener('input', (e) => performSearch(e.target.value, searchResults));
        searchInput.addEventListener('focus', (e) => {
            if (e.target.value.length >= 2) performSearch(e.target.value, searchResults);
        });
        document.addEventListener('click', (e) => {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.classList.add('hidden');
            }
        });
    }

    // Mobile search
    const mobileSearchInput = document.getElementById('mobileSearchInput');
    const mobileSearchResults = document.getElementById('mobileSearchResults');
    if (mobileSearchInput && mobileSearchResults) {
        mobileSearchInput.addEventListener('input', (e) => performSearch(e.target.value, mobileSearchResults));
        mobileSearchInput.addEventListener('focus', (e) => {
            if (e.target.value.length >= 2) performSearch(e.target.value, mobileSearchResults);
        });
    }
}

// Load components when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initComponents);
} else {
    initComponents();
}
