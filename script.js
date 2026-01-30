// DOM Elements
const header = document.querySelector('header');
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');
const navItems = document.querySelectorAll('.nav-links a');
const form = document.querySelector('.contact-form');

// Sticky Header on Scroll
window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Mobile Menu Toggle
hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('active');

    // Animate hamburger icon
    const icon = hamburger.querySelector('i');
    if (navLinks.classList.contains('active')) {
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-times');
    } else {
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
    }
});

// Close Mobile Menu when a link is clicked
navItems.forEach(item => {
    item.addEventListener('click', () => {
        navLinks.classList.remove('active');
        const icon = hamburger.querySelector('i');
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
    });
});

// Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);

        if (targetElement) {
            const headerOffset = 80;
            const elementPosition = targetElement.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: "smooth"
            });
        }
    });
});

// Contact Form Simulation
form.addEventListener('submit', (e) => {
    e.preventDefault();

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerText;

    submitBtn.innerText = 'Mengirim...';
    submitBtn.disabled = true;
    submitBtn.style.opacity = '0.7';

    setTimeout(() => {
        submitBtn.innerHTML = '<i class="fas fa-check"></i> Terkirim!';
        submitBtn.style.background = '#24b47e'; // Success green
        submitBtn.style.borderColor = '#24b47e'; // Success green
        submitBtn.style.color = '#fff';

        form.reset();

        setTimeout(() => {
            submitBtn.innerText = originalText;
            submitBtn.disabled = false;
            submitBtn.style.opacity = '1';
            submitBtn.style = '';
        }, 3000);
    }, 1500);
});

// Intersection Observer for Fade-in Animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px"
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.project-card, .about-card, .blog-card, .section-title').forEach((el, index) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
    // Add staggering only if elements are siblings (simple check)
    if (el.classList.contains('project-card') || el.classList.contains('blog-card')) {
        // rough staggering based on index mod
        el.style.transitionDelay = `${(index % 3) * 100}ms`;
    }
    observer.observe(el);
});

/* 
   --------------------------------------------------
   n8n Style Workflow Background Animation (Canvas)
   --------------------------------------------------
*/
const canvas = document.createElement('canvas');
const heroSection = document.querySelector('.hero');
const bgWrapper = document.querySelector('.hero-background-elements');

// Replace old blob divs with Canvas
if (bgWrapper) {
    bgWrapper.innerHTML = '';
    bgWrapper.appendChild(canvas);
}

const ctx = canvas.getContext('2d');
let width, height;
let nodes = [];
const nodeCount = 30; // Number of floating nodes
const connectionDistance = 150;

// Node Class
class Node {
    constructor() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.vx = (Math.random() - 0.5) * 0.5;
        this.vy = (Math.random() - 0.5) * 0.5;
        this.size = Math.random() * 2 + 1;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;

        // Bounce off edges
        if (this.x < 0 || this.x > width) this.vx *= -1;
        if (this.y < 0 || this.y > height) this.vy *= -1;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 109, 90, 0.4)'; // Coral color
        ctx.fill();
    }
}

function initAnimation() {
    if (!heroSection) return;
    width = canvas.width = heroSection.offsetWidth;
    height = canvas.height = heroSection.offsetHeight;
    nodes = [];
    for (let i = 0; i < nodeCount; i++) {
        nodes.push(new Node());
    }
}

function animate() {
    ctx.clearRect(0, 0, width, height);

    nodes.forEach((node, i) => {
        node.update();
        node.draw();

        // Connect nodes
        for (let j = i + 1; j < nodes.length; j++) {
            const other = nodes[j];
            const dist = Math.hypot(node.x - other.x, node.y - other.y);

            if (dist < connectionDistance) {
                ctx.beginPath();
                ctx.moveTo(node.x, node.y);
                ctx.lineTo(other.x, other.y);
                // Opacity based on distance
                const alpha = 1 - dist / connectionDistance;
                ctx.strokeStyle = `rgba(255, 255, 255, ${alpha * 0.15})`;
                ctx.lineWidth = 1;
                ctx.stroke();
            }
        }
    });

    requestAnimationFrame(animate);
}

// Init
window.addEventListener('resize', initAnimation);
if (heroSection) {
    initAnimation();
    animate();
}

// Track mouse interaction with nodes (optional subtle effect)
let mouseX = 0, mouseY = 0;
document.addEventListener('mousemove', (e) => {
    // Update CSS variables for hover effects globally
    document.body.style.setProperty('--mouse-x', `${e.clientX}px`);
    document.body.style.setProperty('--mouse-y', `${e.clientY}px`);
});

// Update cards on mousemove for hover effect
const cards = document.querySelectorAll('.about-card');
document.addEventListener('mousemove', e => {
    cards.forEach(card => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
    });
});
