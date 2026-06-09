from django.core.management.base import BaseCommand
from store.models import Product


# Map product name → image filename in media/products/
IMAGE_MAP = {
    'Minimal Linen Shirt':          'products/linen_shirt.png',
    'Structured Blazer':            'products/blazer.png',
    'Tailored Chinos':              'products/chinos.png',
    'Minimalist Leather Sneakers':  'products/leather_sneakers.png',
    'Suede Desert Boots':           'products/desert_boots.png',
    'Leather Card Holder':          'products/card_holder.png',
    'Titanium Sunglasses':          'products/sunglasses.png',
    'Canvas Tote Bag':              'products/canvas_tote.png',
    'Leather Weekender':            'products/leather_weekender.png',
    'Hydrating Face Serum':         'products/face_serum.png',
    'Ceramic Pour-Over Set':        'products/pour_over.png',
    'Merino Wool Scarf':            'products/merino_scarf.png',
}


class Command(BaseCommand):
    help = 'Assign generated images to products in the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Assigning product images...')
        updated = 0

        for name, image_path in IMAGE_MAP.items():
            try:
                product = Product.objects.get(name=name)
                product.image = image_path
                product.save(update_fields=['image'])
                self.stdout.write(f'  [OK] {name}')
                updated += 1
            except Product.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  [SKIP] Not found: {name}'))

        self.stdout.write(self.style.SUCCESS(f'Done! {updated} products updated with images.'))
