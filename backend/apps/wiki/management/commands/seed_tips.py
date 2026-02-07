"""
Django management command to seed the database with curated hygiene tips.

This command imports tips from the curated data file and creates
categories and tips in the database.

Usage:
    python manage.py seed_tips
    python manage.py seed_tips --clear-existing
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from apps.wiki.models import Category, Tip


class Command(BaseCommand):
    help = "Seed the database with curated hygiene tips from Reddit communities"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear-existing",
            action="store_true",
            dest="clear_existing",
            help="Clear existing categories and tips before seeding",
        )

    def handle(self, *args, **options):
        # Import tips data
        from apps.wiki.fixtures.tips_data import TIPS_DATA, CATEGORIES

        clear_existing = options.get("clear_existing", False)

        if clear_existing:
            self.stdout.write(self.style.WARNING("Clearing existing data..."))
            Tip.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Existing data cleared."))

        self.stdout.write("Starting to seed database with hygiene tips...\n")

        # Create categories
        categories_created = 0
        categories_map = {}

        self.stdout.write("Creating categories...")
        for category_name in CATEGORIES:
            slug = slugify(category_name)
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={
                    "slug": slug,
                    "description": f"Tips and advice related to {category_name.lower()}",
                },
            )
            categories_map[category_name] = category
            if created:
                categories_created += 1
                self.stdout.write(f"  ✓ Created category: {category_name}")
            else:
                self.stdout.write(f"  - Category already exists: {category_name}")

        self.stdout.write(
            f"\nCategories: {categories_created} created, {len(CATEGORIES) - categories_created} already exist\n"
        )

        # Create tips
        tips_created = 0
        tips_skipped = 0

        self.stdout.write("Creating tips...")
        for tip_data in TIPS_DATA:
            category_name = tip_data["category"]
            title = tip_data["title"]
            description = tip_data["description"]

            # Get or skip if category doesn't exist
            if category_name not in categories_map:
                self.stdout.write(
                    self.style.WARNING(
                        f'  ✗ Skipping tip "{title}" - category "{category_name}" not found'
                    )
                )
                tips_skipped += 1
                continue

            category = categories_map[category_name]

            # Check if tip already exists
            existing_tip = Tip.objects.filter(
                title=title, description=description
            ).first()

            if existing_tip:
                self.stdout.write(f"  - Tip already exists: {title[:50]}...")
                tips_skipped += 1
                continue

            # Create tip
            tip = Tip.objects.create(
                title=title,
                description=description,
                category=category,
                slug=slugify(title),
                effectiveness_avg=0.0,
                difficulty_avg=0.0,
                success_rate=0.0,
            )
            tips_created += 1
            self.stdout.write(f"  ✓ Created tip: {title[:50]}...")

        self.stdout.write(f"\nTips: {tips_created} created, {tips_skipped} skipped\n")

        # Summary
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("DATABASE SEEDING COMPLETE"))
        self.stdout.write("=" * 70)
        self.stdout.write(f"Total categories: {Category.objects.count()}")
        self.stdout.write(f"Total tips: {Tip.objects.count()}")
        self.stdout.write(f"New categories created: {categories_created}")
        self.stdout.write(f"New tips created: {tips_created}")
        self.stdout.write("=" * 70)

        # Display category breakdown
        self.stdout.write("\nCategory breakdown:")
        for category in Category.objects.all():
            tip_count = category.tips.count()
            self.stdout.write(f"  • {category.name}: {tip_count} tips")

        self.stdout.write("\n" + self.style.SUCCESS("Done!"))
