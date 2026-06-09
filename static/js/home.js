/* ============================================================
   home.js — Testimonial Slider & Home Page Interactions
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ── Testimonial Slider ─────────────────────────────────────
  const track = document.querySelector('.testimonials-track');
  const dots  = document.querySelectorAll('.slider-dot');
  const prevBtn = document.querySelector('.slider-btn-prev');
  const nextBtn = document.querySelector('.slider-btn-next');

  if (track && track.children.length > 0) {
    let current = 0;
    let autoPlay;
    const cards = Array.from(track.children);
    const total = cards.length;
    const visibleCount = window.innerWidth > 900 ? 3 : window.innerWidth > 640 ? 2 : 1;

    function getSlideWidth() {
      if (!cards[0]) return 0;
      const card = cards[0];
      const style = window.getComputedStyle(card);
      const marginRight = parseInt(style.marginRight) || 24;
      return card.offsetWidth + marginRight;
    }

    function goTo(index) {
      const max = Math.max(0, total - visibleCount);
      current = Math.min(Math.max(index, 0), max);
      const slideWidth = getSlideWidth();
      track.style.transform = `translateX(-${current * slideWidth}px)`;

      dots.forEach((dot, i) => dot.classList.toggle('active', i === current));
    }

    prevBtn && prevBtn.addEventListener('click', () => {
      goTo(current - 1);
      resetAutoPlay();
    });

    nextBtn && nextBtn.addEventListener('click', () => {
      goTo(current + 1);
      resetAutoPlay();
    });

    dots.forEach((dot, i) => {
      dot.addEventListener('click', () => {
        goTo(i);
        resetAutoPlay();
      });
    });

    function startAutoPlay() {
      autoPlay = setInterval(() => {
        const max = Math.max(0, total - visibleCount);
        goTo(current >= max ? 0 : current + 1);
      }, 4500);
    }

    function resetAutoPlay() {
      clearInterval(autoPlay);
      startAutoPlay();
    }

    // Touch/swipe support
    let startX = 0;
    track.addEventListener('touchstart', e => { startX = e.touches[0].clientX; }, { passive: true });
    track.addEventListener('touchend', e => {
      const diff = startX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 50) {
        goTo(diff > 0 ? current + 1 : current - 1);
        resetAutoPlay();
      }
    });

    goTo(0);
    startAutoPlay();

    window.addEventListener('resize', () => goTo(current));
  }

  // ── Newsletter Form ────────────────────────────────────────
  const newsletterForm = document.querySelector('.newsletter-form');
  if (newsletterForm) {
    newsletterForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const input = this.querySelector('input[type="email"]');
      const btn   = this.querySelector('button');

      if (!input?.value) return;

      const origText = btn.textContent;
      btn.textContent = 'Subscribed! ✓';
      btn.style.background = '#4CAF50';
      btn.disabled = true;
      input.value = '';

      setTimeout(() => {
        btn.textContent = origText;
        btn.style.background = '';
        btn.disabled = false;
      }, 3000);
    });
  }

  // ── Hero Parallax ──────────────────────────────────────────
  const heroVisual = document.querySelector('.hero-visual');
  if (heroVisual) {
    window.addEventListener('scroll', () => {
      const scrollY = window.scrollY;
      const img = heroVisual.querySelector('img');
      if (img) {
        img.style.transform = `scale(1.05) translateY(${scrollY * 0.15}px)`;
      }
    }, { passive: true });
  }

  // ── Category Chips Scroll ──────────────────────────────────
  const categoryGrid = document.querySelector('.categories-grid');
  if (categoryGrid) {
    let isDown = false;
    let startX;
    let scrollLeft;

    categoryGrid.addEventListener('mousedown', e => {
      isDown = true;
      startX = e.pageX - categoryGrid.offsetLeft;
      scrollLeft = categoryGrid.scrollLeft;
      categoryGrid.style.cursor = 'grabbing';
    });

    categoryGrid.addEventListener('mouseleave', () => { isDown = false; categoryGrid.style.cursor = ''; });
    categoryGrid.addEventListener('mouseup', () => { isDown = false; categoryGrid.style.cursor = ''; });
    categoryGrid.addEventListener('mousemove', e => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - categoryGrid.offsetLeft;
      const walk = (x - startX) * 1.5;
      categoryGrid.scrollLeft = scrollLeft - walk;
    });
  }

  // ── Hero Counter Animation ─────────────────────────────────
  const statValues = document.querySelectorAll('.hero-stat-value[data-target]');
  if (statValues.length > 0) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.dataset.target);
          const suffix = el.dataset.suffix || '';
          let start = 0;
          const duration = 1800;
          const step = timestamp => {
            if (!start) start = timestamp;
            const progress = Math.min((timestamp - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            el.textContent = Math.floor(eased * target) + suffix;
            if (progress < 1) requestAnimationFrame(step);
          };
          requestAnimationFrame(step);
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.5 });

    statValues.forEach(el => observer.observe(el));
  }

});
