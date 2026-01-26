// ===== Typing Animation for Hero =====
const typingText = document.querySelector('.typing-text');
const phrases = [
    "Here's to another year of amazing adventures! 🌟",
    "You make the world brighter just by being in it ✨",
    "Wishing you endless happiness today and always 💖"
];

let phraseIndex = 0;
let charIndex = 0;
let isDeleting = false;

function typeText() {
    const currentPhrase = phrases[phraseIndex];
    
    if (!isDeleting) {
        typingText.textContent = currentPhrase.substring(0, charIndex);
        charIndex++;
        
        if (charIndex > currentPhrase.length) {
            isDeleting = true;
            setTimeout(typeText, 2000);
            return;
        }
    } else {
        typingText.textContent = currentPhrase.substring(0, charIndex);
        charIndex--;
        
        if (charIndex === 0) {
            isDeleting = false;
            phraseIndex = (phraseIndex + 1) % phrases.length;
        }
    }
    
    const typingSpeed = isDeleting ? 50 : 100;
    setTimeout(typeText, typingSpeed);
}

// Start typing animation
setTimeout(typeText, 1000);

// ===== Floating Hearts =====
const heartsContainer = document.getElementById('heartsContainer');
const heartEmojis = ['💖', '💕', '💗', '💓', '💝', '💘'];

function createHeart() {
    const heart = document.createElement('div');
    heart.className = 'heart';
    heart.textContent = heartEmojis[Math.floor(Math.random() * heartEmojis.length)];
    heart.style.left = Math.random() * 100 + '%';
    heart.style.animationDuration = (Math.random() * 3 + 7) + 's';
    heart.style.fontSize = (Math.random() * 15 + 15) + 'px';
    heartsContainer.appendChild(heart);
    
    setTimeout(() => {
        heart.remove();
    }, 10000);
}

// Create hearts periodically
setInterval(createHeart, 800);

// ===== Sparkles =====
const sparklesContainer = document.getElementById('sparkles');
const sparkleEmojis = ['✨', '⭐', '🌟', '💫'];

function createSparkle() {
    const sparkle = document.createElement('div');
    sparkle.className = 'sparkle';
    sparkle.textContent = sparkleEmojis[Math.floor(Math.random() * sparkleEmojis.length)];
    sparkle.style.left = Math.random() * 100 + '%';
    sparkle.style.top = Math.random() * 100 + '%';
    sparkle.style.animationDelay = Math.random() * 2 + 's';
    sparklesContainer.appendChild(sparkle);
    
    setTimeout(() => {
        sparkle.remove();
    }, 3000);
}

// Create sparkles periodically
setInterval(createSparkle, 500);

// ===== Music Player =====
const musicToggle = document.getElementById('musicToggle');
const bgMusic = document.getElementById('bgMusic');
let isMusicPlaying = false;

musicToggle.addEventListener('click', () => {
    if (!isMusicPlaying) {
        bgMusic.play();
        musicToggle.classList.add('playing');
        isMusicPlaying = true;
    } else {
        bgMusic.pause();
        musicToggle.classList.remove('playing');
        isMusicPlaying = false;
    }
});

// ===== Gallery Lightbox =====
const galleryItems = document.querySelectorAll('.gallery-item');
const lightbox = document.getElementById('lightbox');
const lightboxImage = document.querySelector('.lightbox-image');
const lightboxClose = document.querySelector('.lightbox-close');
const lightboxPrev = document.querySelector('.lightbox-prev');
const lightboxNext = document.querySelector('.lightbox-next');

let currentImageIndex = 0;
const images = Array.from(galleryItems).map(item => item.getAttribute('data-image'));

galleryItems.forEach((item, index) => {
    item.addEventListener('click', () => {
        currentImageIndex = index;
        openLightbox();
    });
});

function openLightbox() {
    lightbox.classList.add('active');
    lightboxImage.src = images[currentImageIndex];
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    lightbox.classList.remove('active');
    document.body.style.overflow = 'auto';
}

lightboxClose.addEventListener('click', closeLightbox);

lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) {
        closeLightbox();
    }
});

lightboxPrev.addEventListener('click', (e) => {
    e.stopPropagation();
    currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
    lightboxImage.src = images[currentImageIndex];
});

lightboxNext.addEventListener('click', (e) => {
    e.stopPropagation();
    currentImageIndex = (currentImageIndex + 1) % images.length;
    lightboxImage.src = images[currentImageIndex];
});

// Keyboard navigation for lightbox
document.addEventListener('keydown', (e) => {
    if (!lightbox.classList.contains('active')) return;
    
    if (e.key === 'Escape') {
        closeLightbox();
    } else if (e.key === 'ArrowLeft') {
        currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
        lightboxImage.src = images[currentImageIndex];
    } else if (e.key === 'ArrowRight') {
        currentImageIndex = (currentImageIndex + 1) % images.length;
        lightboxImage.src = images[currentImageIndex];
    }
});

// ===== Slideshow =====
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
let slideshowInterval;
let isPlaying = true;

function showSlide(index) {
    slides.forEach(slide => slide.classList.remove('active'));
    currentSlide = (index + slides.length) % slides.length;
    slides[currentSlide].classList.add('active');
}

function changeSlide(direction) {
    showSlide(currentSlide + direction);
}

function startSlideshow() {
    slideshowInterval = setInterval(() => {
        changeSlide(1);
    }, 4000);
}

function stopSlideshow() {
    clearInterval(slideshowInterval);
}

const playPauseBtn = document.getElementById('playPause');

playPauseBtn.addEventListener('click', () => {
    if (isPlaying) {
        stopSlideshow();
        playPauseBtn.textContent = '▶️';
        isPlaying = false;
    } else {
        startSlideshow();
        playPauseBtn.textContent = '⏸️';
        isPlaying = true;
    }
});

// Start slideshow automatically
startSlideshow();

// ===== Heart Particles in Message Section =====
const heartParticlesContainer = document.getElementById('heartParticles');

function createHeartParticle() {
    const particle = document.createElement('div');
    particle.className = 'heart-particle';
    particle.textContent = '💕';
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = Math.random() * 100 + '%';
    particle.style.animationDelay = Math.random() * 4 + 's';
    heartParticlesContainer.appendChild(particle);
}

// Create multiple heart particles
for (let i = 0; i < 15; i++) {
    createHeartParticle();
}

// ===== Surprise Button with Confetti =====
const surpriseBtn = document.getElementById('surpriseBtn');
const surpriseMessage = document.getElementById('surpriseMessage');

surpriseBtn.addEventListener('click', () => {
    surpriseMessage.classList.remove('hidden');
    createConfetti();
    
    // Scroll to message
    surpriseMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
});

function createConfetti() {
    const colors = ['#FFD1DC', '#E6E6FA', '#B5EAD7', '#FFE5B4', '#C9E4FF', '#D4B5FF', '#FFB3BA'];
    
    for (let i = 0; i < 100; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.top = '-10px';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
            document.body.appendChild(confetti);
            
            setTimeout(() => {
                confetti.remove();
            }, 3000);
        }, i * 30);
    }
}

// ===== Scroll Animations =====
const observerOptions = {
    threshold: 0.2,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

// Observe gallery items
galleryItems.forEach(item => {
    item.classList.add('fade-in');
    observer.observe(item);
});

// Observe sections
const sections = document.querySelectorAll('.gallery-section, .memories-section, .message-section, .fun-section');
sections.forEach(section => {
    observer.observe(section);
});

// ===== Smooth Scroll for Navigation =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===== Parallax Effect on Hero =====
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const heroContent = document.querySelector('.hero-content');
    
    if (heroContent) {
        heroContent.style.transform = `translateY(${scrolled * 0.5}px)`;
        heroContent.style.opacity = 1 - (scrolled / 600);
    }
});

// ===== Add fade-in animation to quotes =====
const quoteItems = document.querySelectorAll('.quotes-list li');
quoteItems.forEach((item, index) => {
    item.style.opacity = '0';
    setTimeout(() => {
        item.style.opacity = '1';
    }, index * 150);
});

// ===== Animate message paragraphs =====
const messageParagraphs = document.querySelectorAll('.message-paragraph');
const messageObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            setTimeout(() => {
                entry.target.style.animation = 'fadeInUp 0.8s ease-out forwards';
            }, index * 200);
        }
    });
}, { threshold: 0.5 });

messageParagraphs.forEach(para => {
    para.style.opacity = '0';
    messageObserver.observe(para);
});

// ===== Add hover effect to navbar on scroll =====
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        navbar.style.padding = '10px 0';
        navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.15)';
    } else {
        navbar.style.padding = '15px 0';
        navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.08)';
    }
    
    lastScroll = currentScroll;
});

// ===== Welcome Animation =====
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 1s ease-in';
        document.body.style.opacity = '1';
    }, 100);
});

// ===== Console Message =====
console.log('%c🎉 Happy Birthday! 🎂', 'font-size: 30px; color: #FFB3BA; font-weight: bold;');
console.log('%cMade with 💖 and lots of JavaScript magic!', 'font-size: 16px; color: #D4B5FF;');
