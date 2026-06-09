from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from store.models import Category, Product


CATEGORIES = [
    {'name': 'Clothing', 'description': 'Timeless wardrobe essentials crafted with precision.'},
    {'name': 'Footwear', 'description': 'Step into comfort and style.'},
    {'name': 'Accessories', 'description': 'The finishing touch to every look.'},
    {'name': 'Bags', 'description': 'Carry your world in effortless style.'},
    {'name': 'Skincare', 'description': 'Rituals for radiant, healthy skin.'},
    {'name': 'Lifestyle', 'description': 'Objects that elevate everyday living.'},
]

PRODUCTS = [
    # Clothing
    {'name': 'Minimal Linen Shirt', 'category': 'Clothing', 'price': 2499, 'compare_price': 3499, 'stock': 50, 'featured': True,
     'description': 'Crafted from 100% stonewashed linen, this shirt embodies relaxed sophistication. Its natural texture and breathable weave make it the perfect companion for warm days and balmy evenings. The relaxed fit drapes beautifully, offering effortless elegance.'},
    {'name': 'Structured Blazer', 'category': 'Clothing', 'price': 5999, 'compare_price': 8999, 'stock': 30, 'featured': True,
     'description': 'A modern interpretation of the classic blazer. Cut from premium wool-blend fabric, it features clean lines, a tailored silhouette, and subtle details that speak volumes. Dress it up or down with equal confidence.'},
    {'name': 'Essential Crew Tee', 'category': 'Clothing', 'price': 1299, 'stock': 100, 'featured': False,
     'description': 'The perfect tee, perfected. Made from 200gsm supima cotton, this crew neck tee is the foundation of any great wardrobe. Soft, durable, and cut to flatter every body type.'},
    {'name': 'Tailored Chinos', 'category': 'Clothing', 'price': 3299, 'compare_price': 4499, 'stock': 45, 'featured': True,
     'description': 'Precision-cut chinos in a versatile mid-weight cotton twill. The refined taper and clean finish make these the most stylish pair you will own. Available in a palette of muted, sophisticated tones.'},

    # Footwear
    {'name': 'Minimalist Leather Sneakers', 'category': 'Footwear', 'price': 7499, 'compare_price': 9999, 'stock': 25, 'featured': True,
     'description': 'Clean, low-profile sneakers in full-grain Italian leather. Hand-finished edges and a cushioned leather insole make these as comfortable as they are beautiful. The design is timeless — nothing superfluous, nothing missing.'},
    {'name': 'Suede Desert Boots', 'category': 'Footwear', 'price': 6499, 'stock': 20, 'featured': True,
     'description': 'A wardrobe cornerstone. These desert boots are made from premium suede with a natural crepe rubber sole for all-day comfort. The minimalist silhouette pairs seamlessly with almost everything in your wardrobe.'},
    {'name': 'Knit Running Shoes', 'category': 'Footwear', 'price': 4999, 'compare_price': 6499, 'stock': 35, 'featured': False,
     'description': 'Performance and aesthetics united. The breathable engineered knit upper wraps your foot in adaptive comfort, while the responsive foam midsole propels every stride. A shoe that works as hard as you do.'},

    # Accessories
    {'name': 'Merino Wool Scarf', 'category': 'Accessories', 'price': 1899, 'stock': 60, 'featured': False,
     'description': 'Spun from the finest merino wool, this scarf is exceptionally soft and naturally temperature-regulating. Its generous proportions allow for a multitude of styling options, from a classic drape to a cozy wrap.'},
    {'name': 'Leather Card Holder', 'category': 'Accessories', 'price': 1499, 'compare_price': 1999, 'stock': 80, 'featured': True,
     'description': 'Minimalism, perfected. This slim card holder is crafted from a single piece of full-grain leather that will develop a beautiful patina over time. Holds up to 8 cards and a few folded notes.'},
    {'name': 'Titanium Sunglasses', 'category': 'Accessories', 'price': 8999, 'stock': 15, 'featured': True,
     'description': 'Feather-light titanium frames paired with polarised lenses that block 100% of UVA/UVB rays. These sunglasses are as functional as they are beautiful, designed for those who appreciate the precision in fine details.'},

    # Bags
    {'name': 'Canvas Tote Bag', 'category': 'Bags', 'price': 2299, 'compare_price': 2999, 'stock': 40, 'featured': True,
     'description': 'A utilitarian icon, elevated. This heavyweight canvas tote features reinforced handles, an internal zip pocket, and a generous main compartment. The washed canvas develops a beautiful character with use.'},
    {'name': 'Leather Weekender', 'category': 'Bags', 'price': 12999, 'stock': 10, 'featured': True,
     'description': 'Your companion for spontaneous escapes. Handcrafted from full-grain leather with brass hardware, this weekender bag is spacious enough for a two-night trip while remaining sophisticated enough for a business meeting.'},

    # Skincare
    {'name': 'Hydrating Face Serum', 'category': 'Skincare', 'price': 3499, 'compare_price': 4499, 'stock': 55, 'featured': True,
     'description': 'A concentrated cocktail of hyaluronic acid, niacinamide, and botanical extracts that delivers deep hydration and visible radiance. Lightweight, fast-absorbing, and formulated for all skin types. Your skin\'s daily ritual.'},
    {'name': 'Botanical Face Oil', 'category': 'Skincare', 'price': 2999, 'stock': 30, 'featured': False,
     'description': 'A luxurious dry oil blend of rosehip, jojoba, and squalane that nourishes deeply without clogging pores. Rich in essential fatty acids and antioxidants, it restores suppleness and promotes a natural glow.'},

    # Lifestyle
    {'name': 'Ceramic Pour-Over Set', 'category': 'Lifestyle', 'price': 4499, 'compare_price': 5999, 'stock': 20, 'featured': True,
     'description': 'Transform your morning ritual. This hand-thrown ceramic pour-over dripper and carafe set is both a functional brewing instrument and a sculptural object. The matte glaze and organic form make it a beautiful addition to any kitchen.'},
    {'name': 'Linen Pillowcase Set', 'category': 'Lifestyle', 'price': 2799, 'stock': 45, 'featured': False,
     'description': 'Sleep in pure luxury. These pillowcases are woven from stonewashed French linen that gets softer with every wash. The natural fibres are breathable and moisture-wicking, ensuring a cool, comfortable night\'s sleep.'},
]


class Command(BaseCommand):
    help = 'Seed the database with sample categories and products'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@luxe.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superuser created: admin / admin123'))

        # Create categories
        cat_map = {}
        for cat_data in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            cat_map[cat_data['name']] = cat
            if created:
                self.stdout.write(f'  Category: {cat.name}')

        # Create products
        for p in PRODUCTS:
            if Product.objects.filter(name=p['name']).exists():
                continue
            product = Product(
                name=p['name'],
                category=cat_map[p['category']],
                price=p['price'],
                compare_price=p.get('compare_price'),
                stock=p['stock'],
                is_featured=p.get('featured', False),
                description=p['description'],
            )
            product.save()
            self.stdout.write(f'  Product: {product.name}')

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write(self.style.WARNING('Note: Add product images via Django admin at /admin/'))
        self.stdout.write(self.style.SUCCESS('Admin login: admin / admin123'))
