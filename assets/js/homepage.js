/**
 * Homepage-specific scripts for DeiTheon
 * Includes carousel, newsletter form, and scroll animations
 */

// ========== Loading Screen ==========
window.addEventListener('load', () => {
    const loadingScreen = document.getElementById('loadingScreen');
    if (loadingScreen) {
        setTimeout(() => {
            loadingScreen.style.opacity = '0';
            setTimeout(() => {
                loadingScreen.style.display = 'none';
            }, 500);
        }, 800);
    }
});

// ========== Featured Carousel ==========
const carouselTrack = document.getElementById('carouselTrack');
const carouselPrev = document.getElementById('carouselPrev');
const carouselNext = document.getElementById('carouselNext');
let currentSlide = 0;
const totalSlides = carouselTrack ? carouselTrack.children.length : 0;

function getVisibleSlides() {
    if (window.innerWidth >= 1024) return 3;
    if (window.innerWidth >= 768) return 2;
    return 1;
}

function updateCarousel() {
    if (!carouselTrack) return;
    const visibleSlides = getVisibleSlides();
    const maxSlide = Math.max(0, totalSlides - visibleSlides);
    currentSlide = Math.min(currentSlide, maxSlide);
    const offset = -(currentSlide * (100 / visibleSlides));
    carouselTrack.style.transform = `translateX(${offset}%)`;
}

if (carouselPrev) {
    carouselPrev.addEventListener('click', () => {
        currentSlide = Math.max(0, currentSlide - 1);
        updateCarousel();
    });
}

if (carouselNext) {
    carouselNext.addEventListener('click', () => {
        const visibleSlides = getVisibleSlides();
        const maxSlide = totalSlides - visibleSlides;
        currentSlide = Math.min(maxSlide, currentSlide + 1);
        updateCarousel();
    });
}

window.addEventListener('resize', updateCarousel);
updateCarousel();

// Auto-rotate carousel every 5 seconds
setInterval(() => {
    if (carouselTrack) {
        const visibleSlides = getVisibleSlides();
        const maxSlide = totalSlides - visibleSlides;
        currentSlide = currentSlide >= maxSlide ? 0 : currentSlide + 1;
        updateCarousel();
    }
}, 5000);

// ========== Scroll Animations ==========
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));

// ========== Newsletter Form ==========
const newsletterForm = document.getElementById('newsletterForm');
const newsletterMessage = document.getElementById('newsletterMessage');

if (newsletterForm) {
    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('newsletterEmail').value;
        
        // Simulate subscription (replace with actual API call)
        newsletterMessage.textContent = `Thanks for subscribing with ${email}! Check your inbox for confirmation.`;
        newsletterMessage.style.opacity = '1';
        newsletterForm.reset();
        
        setTimeout(() => {
            newsletterMessage.style.opacity = '0';
        }, 5000);
    });
}

// ========== Smooth Scroll for Anchor Links ==========
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});
