/* ============================================================
   cart.js — AJAX Cart Operations
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  const CSRF = getCookie('csrftoken');

  // ── CSRF Helper ────────────────────────────────────────────
  function getCookie(name) {
    let value = '';
    document.cookie.split(';').forEach(c => {
      const [k, v] = c.trim().split('=');
      if (k === name) value = decodeURIComponent(v);
    });
    return value;
  }

  // ── Update Cart Badge ──────────────────────────────────────
  function updateCartBadge(count) {
    const badges = document.querySelectorAll('.cart-badge');
    badges.forEach(badge => {
      badge.textContent = count;
      badge.style.display = count > 0 ? 'flex' : 'none';
      // Pop animation
      badge.style.transform = 'scale(1.5)';
      setTimeout(() => badge.style.transform = '', 200);
    });
  }

  // ── Add to Cart (AJAX) ─────────────────────────────────────
  document.querySelectorAll('.add-to-cart-form').forEach(form => {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      const btn = this.querySelector('[type="submit"]');
      const originalText = btn.innerHTML;

      btn.disabled = true;
      btn.innerHTML = `<svg class="spin" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0"/></svg> Adding...`;

      try {
        const formData = new FormData(this);
        const res = await fetch(this.action, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': CSRF,
          },
          body: formData,
        });

        const data = await res.json();
        if (data.success) {
          updateCartBadge(data.cart_count);
          window.showToast && window.showToast(data.message || 'Added to cart!', 'success');

          // Button feedback
          btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> Added!`;
          btn.style.background = '#4CAF50';
          setTimeout(() => {
            btn.innerHTML = originalText;
            btn.style.background = '';
            btn.disabled = false;
          }, 1800);
        }
      } catch (err) {
        window.showToast && window.showToast('Something went wrong. Please try again.', 'error');
        btn.innerHTML = originalText;
        btn.disabled = false;
      }
    });
  });

  // ── Cart Quantity Update (AJAX) ────────────────────────────
  document.querySelectorAll('.cart-qty-form').forEach(form => {
    const input = form.querySelector('.qty-input');
    if (!input) return;

    let debounceTimer;

    input.addEventListener('change', function() {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(async () => {
        const formData = new FormData(form);
        formData.set('quantity', this.value);

        try {
          const res = await fetch(form.action, {
            method: 'POST',
            headers: {
              'X-Requested-With': 'XMLHttpRequest',
              'X-CSRFToken': CSRF,
            },
            body: formData,
          });

          const data = await res.json();
          if (data.success) {
            // Update subtotal
            const subtotalEl = form.closest('.cart-item')?.querySelector('.cart-item-subtotal');
            if (subtotalEl && data.subtotal) {
              subtotalEl.textContent = `₹${parseFloat(data.subtotal).toLocaleString('en-IN')}`;
            }

            // Update cart total
            const totalEl = document.querySelector('.cart-total-value');
            if (totalEl && data.cart_total) {
              totalEl.textContent = `₹${parseFloat(data.cart_total).toLocaleString('en-IN')}`;
            }

            updateCartBadge(data.cart_count);

            // If quantity was 0, remove the row
            if (parseInt(this.value) < 1) {
              const row = form.closest('.cart-item');
              if (row) {
                row.style.opacity = '0';
                row.style.transform = 'translateX(-20px)';
                row.style.transition = 'all 0.3s ease';
                setTimeout(() => row.remove(), 300);
              }
            }
          }
        } catch (err) {
          console.error('Cart update failed', err);
        }
      }, 400);
    });
  });

  // ── Remove Cart Item (AJAX) ────────────────────────────────
  document.querySelectorAll('.remove-item-form').forEach(form => {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      const row = this.closest('.cart-item');

      try {
        const res = await fetch(this.action, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': CSRF,
          },
        });

        const data = await res.json();
        if (data.success) {
          if (row) {
            row.style.opacity = '0';
            row.style.maxHeight = row.offsetHeight + 'px';
            row.style.overflow = 'hidden';
            row.style.transition = 'opacity 0.3s, max-height 0.4s, padding 0.4s';

            setTimeout(() => {
              row.style.maxHeight = '0';
              row.style.paddingTop = '0';
              row.style.paddingBottom = '0';
            }, 10);

            setTimeout(() => row.remove(), 420);
          }

          // Update totals
          const totalEl = document.querySelector('.cart-total-value');
          if (totalEl && data.cart_total) {
            totalEl.textContent = `₹${parseFloat(data.cart_total).toLocaleString('en-IN')}`;
          }

          updateCartBadge(data.cart_count);
          window.showToast && window.showToast('Item removed from cart.', 'info');

          // Check if cart is empty
          if (data.cart_count === 0) {
            setTimeout(() => window.location.reload(), 600);
          }
        }
      } catch (err) {
        console.error('Remove failed', err);
      }
    });
  });

});

/* Spinner CSS injected by JS */
const spinStyle = document.createElement('style');
spinStyle.textContent = `
  .spin { animation: spin360 0.8s linear infinite; }
  @keyframes spin360 { to { transform: rotate(360deg); } }
`;
document.head.appendChild(spinStyle);
