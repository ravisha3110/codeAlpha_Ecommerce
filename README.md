# LUXE E-Commerce — Premium Django Store

A premium, minimal luxury e-commerce website built with Django, HTML, CSS and JavaScript.
Inspired by Apple, Nike, Zara and Aesop.

## Tech Stack
- **Backend:** Django 6.0 (Python 3.13)
- **Database:** SQLite
- **Frontend:** HTML5, Vanilla CSS, Vanilla JS
- **Fonts:** Cormorant Garamond + Inter (Google Fonts)

## Quick Start

```bash
# 1. Install dependencies
py -m pip install -r requirements.txt

# 2. Run migrations
py manage.py migrate

# 3. Seed sample data (creates admin user + 16 products)
py manage.py seed_data

# 4. Start the server
py manage.py runserver
```

Visit: **http://127.0.0.1:8000**

## Admin Panel
- URL: http://127.0.0.1:8000/admin/
- Username: `admin`
- Password: `admin123`

> Upload product images via the Admin Panel for best visual results.

## Features
- ✅ User Registration, Login, Logout
- ✅ Session-based guest cart (merges on login)
- ✅ Product listing with category filter & search
- ✅ Product detail with add-to-cart
- ✅ AJAX cart with live quantity updates
- ✅ Checkout with shipping form
- ✅ Order history with status badges
- ✅ Premium UI: glassmorphism, scroll reveal, masonry grid, testimonial slider
- ✅ Fully responsive (mobile-first)

## Folder Structure
```
├── ecommerce/      ← Django project config
├── store/          ← Products, cart, orders
├── accounts/       ← User auth
├── templates/      ← HTML templates
├── static/
│   ├── css/        ← base, navbar, home, store
│   └── js/         ← main, cart, home
└── media/          ← Uploaded product images
```

## Color Palette
| Color | Hex |
|-------|-----|
| Background | `#FAF8F5` |
| Primary | `#1F1F1F` |
| Accent (Gold) | `#C59D5F` |
| Secondary | `#EAE4DC` |
| Text | `#2B2B2B` |
