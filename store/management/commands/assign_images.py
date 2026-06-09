import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand
from store.models import Product


# Map product name → image filename (relative to media/products/ and static/images/products/)
IMAGE_MAP = {
    'Minimal Linen Shirt':          'linen_shirt.png',
    'Structured Blazer':            'blazer.png',
    'Tailored Chinos':              'chinos.png',
    'Minimalist Leather Sneakers':  'leather_sneakers.png',
    'Suede Desert Boots':           'desert_boots.png',
    'Leather Card Holder':          'card_holder.png',
    'Titanium Sunglasses':          'sunglasses.png',
    'Canvas Tote Bag':              'canvas_tote.png',
    'Leather Weekender':            'leather_weekender.png',
    'Hydrating Face Serum':         'face_serum.png',
    'Ceramic Pour-Over Set':        'pour_over.png',
    'Merino Wool Scarf':            'merino_scarf.png',
}


class Command(BaseCommand):
    help = 'Copy product images from static into media, then assign to DB records'

    def handle(self, *args, **kwargs):
        self.stdout.write('Assigning product images...')

        # Ensure the media/products/ directory exists on the server
        media_products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        os.makedirs(media_products_dir, exist_ok=True)

        # Source directory: static/images/products/ (committed to Git → always present)
        static_products_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'products')

        updated = 0

        for name, filename in IMAGE_MAP.items():
            src = os.path.join(static_products_dir, filename)
            dst = os.path.join(media_products_dir, filename)

            # Copy from static → media if not already there
            if os.path.exists(src):
                if not os.path.exists(dst):
                    shutil.copy2(src, dst)
                    self.stdout.write(f'  [COPY] {filename}')
                else:
                    self.stdout.write(f'  [EXISTS] {filename}')
            else:
                self.stdout.write(self.style.WARNING(f'  [MISSING SRC] {src}'))

            # Update the DB record to point at this image
            try:
                product = Product.objects.get(name=name)
                product.image = f'products/{filename}'
                product.save(update_fields=['image'])
                self.stdout.write(f'  [OK] {name}')
                updated += 1
            except Product.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  [SKIP] Product not found: {name}'))

        self.stdout.write(self.style.SUCCESS(f'Done! {updated} products updated with images.'))
