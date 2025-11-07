// Theme Management
const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;

// Check for saved theme preference
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    html.classList.add(savedTheme);
    updateThemeIcon(savedTheme);
}

// Theme toggle functionality
themeToggle.addEventListener('click', () => {
    if (html.classList.contains('dark')) {
        html.classList.remove('dark');
        localStorage.setItem('theme', 'light');
        updateThemeIcon('light');
    } else {
        html.classList.add('dark');
        localStorage.setItem('theme', 'dark');
        updateThemeIcon('dark');
    }
});

function updateThemeIcon(theme) {
    const sunPath = themeToggle.querySelector('.sun');
    const moonPath = themeToggle.querySelector('.moon');
    
    if (theme === 'dark') {
        sunPath.classList.remove('hidden');
        moonPath.classList.add('hidden');
    } else {
        sunPath.classList.add('hidden');
        moonPath.classList.remove('hidden');
    }
}

// Mobile Menu
const mobileMenuButton = document.getElementById('mobileMenuButton');
const mobileMenu = document.getElementById('mobileMenu');
const openIcon = mobileMenuButton.querySelector('.open');
const closeIcon = mobileMenuButton.querySelector('.close');

mobileMenuButton.addEventListener('click', () => {
    const isExpanded = mobileMenuButton.getAttribute('aria-expanded') === 'true';
    
    mobileMenuButton.setAttribute('aria-expanded', !isExpanded);
    mobileMenu.classList.toggle('hidden');
    openIcon.classList.toggle('hidden');
    closeIcon.classList.toggle('hidden');
});

// Scroll to Top Button
const scrollToTopBtn = document.getElementById('scrollToTop');

window.addEventListener('scroll', () => {
    if (window.scrollY > 500) {
        scrollToTopBtn.classList.remove('hidden');
    } else {
        scrollToTopBtn.classList.add('hidden');
    }
});

scrollToTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Search Functionality
const searchInput = document.querySelector('input[type="search"]');
searchInput.addEventListener('input', debounce(handleSearch, 300));

function handleSearch(e) {
    const searchTerm = e.target.value.toLowerCase();
    // TODO: Implement search functionality
    console.log('Searching for:', searchTerm);
}

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add loading indicator for navigation
document.addEventListener('click', (e) => {
    const link = e.target.closest('a');
    if (link && link.href && !link.target && !e.ctrlKey && !e.shiftKey) {
        const loadingIndicator = document.createElement('div');
        loadingIndicator.classList.add('loading-indicator');
        document.body.appendChild(loadingIndicator);
    }
});