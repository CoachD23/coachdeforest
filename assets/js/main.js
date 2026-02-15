// ============================================
// Coach DeForest — Main JavaScript
// ============================================

document.addEventListener('DOMContentLoaded', () => {

  // --- Mobile Menu Toggle ---
  const toggle = document.getElementById('mobileToggle');
  const nav = document.getElementById('mainNav');

  function openMobileNav() {
    nav.classList.add('active');
    toggle.classList.add('active');
    document.body.classList.add('nav-open');
  }

  function closeMobileNav() {
    nav.classList.remove('active');
    toggle.classList.remove('active');
    document.body.classList.remove('nav-open');
  }

  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      if (nav.classList.contains('active')) {
        closeMobileNav();
      } else {
        openMobileNav();
      }
    });

    // Close menu on link click
    nav.querySelectorAll('.nav-link, .mobile-cta').forEach(link => {
      link.addEventListener('click', closeMobileNav);
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && nav.classList.contains('active')) {
        closeMobileNav();
      }
    });
  }

  // --- Scroll Animations (IntersectionObserver) ---
  const fadeEls = document.querySelectorAll('.fade-in, .fade-in-left, .fade-in-right');
  if (fadeEls.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.05, rootMargin: '0px 0px -20px 0px' });
    fadeEls.forEach(el => observer.observe(el));

    // Fallback: show elements already in viewport on page load
    requestAnimationFrame(() => {
      fadeEls.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {
          el.classList.add('visible');
        }
      });
    });
  } else {
    fadeEls.forEach(el => el.classList.add('visible'));
  }

  // --- Header Shrink on Scroll ---
  const header = document.querySelector('.site-header');
  if (header) {
    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 60);
    });
  }

  // --- Smooth Scroll for Anchor Links ---
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

});
