import csv
import re
from django.core.management.base import BaseCommand
from django.db import transaction
from products.models import (
    ProductCategory,
    ProductSubCategory,
    ProductType,
    FrameFormulation
)
import requests
from io import StringIO


class Command(BaseCommand):
    help = 'Import products from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, help='URL to CSV file')
        parser.add_argument('--file', type=str, help='Path to CSV file')

    def handle(self, *args, **options):
        # Get CSV data either from URL or local file
        csv_data = None

        if options['url']:
            self.stdout.write(self.style.SUCCESS(f'Downloading CSV from {options["url"]}'))
            response = requests.get(options['url'])
            if response.status_code == 200:
                csv_data = StringIO(response.text)
            else:
                self.stdout.write(self.style.ERROR(f'Failed to download CSV: {response.status_code}'))
                return
        elif options['file']:
            self.stdout.write(self.style.SUCCESS(f'Reading CSV from {options["file"]}'))
            try:
                csv_data = open(options['file'], 'r', encoding='utf-8')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to open file: {e}'))
                return
        else:
            self.stdout.write(self.style.ERROR('Please provide either --url or --file'))
            return

        # Process the CSV data
        try:
            with transaction.atomic():
                self.import_csv(csv_data)
            self.stdout.write(self.style.SUCCESS('Successfully imported products from CSV'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing CSV: {e}'))
        finally:
            if options['file'] and csv_data:
                csv_data.close()

    def import_csv(self, csv_data):
        reader = csv.reader(csv_data)

        # Skip header row if it exists
        try:
            header = next(reader)
            if not any(cell.strip().startswith(('1', '2', '3', '4')) for cell in header if cell.strip()):
                # This was a header row, continue
                pass
            else:
                # This was actually data, reset the reader
                csv_data.seek(0)
                reader = csv.reader(csv_data)
        except StopIteration:
            self.stdout.write(self.style.ERROR('CSV file is empty'))
            return

        # Variables to track current category, subcategory, and product type
        current_category = None
        current_subcategory = None
        current_product_type = None

        # Counters for reporting
        categories_created = 0
        subcategories_created = 0
        product_types_created = 0
        formulations_created = 0

        # Process each row
        for row in reader:
            # Skip empty rows
            if not any(cell.strip() for cell in row):
                continue

            # Find the first non-empty cell to determine the level
            level = None
            value = None
            for i, cell in enumerate(row):
                if cell.strip():
                    level = i
                    value = cell.strip()
                    break

            if level is None:
                continue

            # Process based on the level
            if level == 0:  # Category
                # Extract code and name
                match = re.match(r'(\d+)\s+(.*)', value)
                if match:
                    code = match.group(1)
                    name = match.group(2)

                    # Create or get category
                    category, created = ProductCategory.objects.get_or_create(
                        code=code,
                        defaults={
                            'name': name,
                            'unique_id': f'CAT{code}',
                            'category_num': code
                        }
                    )

                    if created:
                        categories_created += 1
                        self.stdout.write(f'Created category: {category.name}')

                    current_category = category
                    current_subcategory = None
                    current_product_type = None

            elif level == 1 and current_category:  # Subcategory
                # Extract code and name
                match = re.match(r'(\d+\.\d+)\s+(.*)', value)
                if match:
                    code = match.group(1)
                    name = match.group(2)

                    # Create or get subcategory
                    subcategory, created = ProductSubCategory.objects.get_or_create(
                        code=code,
                        defaults={
                            'name': name,
                            'unique_id': f'SUBCAT{code.replace(".", "")}',
                            'sub_category_num': code,
                            'sccs_product_category': current_category
                        }
                    )

                    if created:
                        subcategories_created += 1
                        self.stdout.write(f'  Created subcategory: {subcategory.name}')

                    current_subcategory = subcategory
                    current_product_type = None

            elif level == 2 and current_subcategory:  # Product Type
                # Extract code and name
                match = re.match(r'(\d+\.\d+\.\d+)\s+(.*)', value)
                if match:
                    code = match.group(1)
                    name = match.group(2)

                    # Create or get product type
                    product_type, created = ProductType.objects.get_or_create(
                        code=code,
                        defaults={
                            'name': name,
                            'unique_id': f'PRODTYPE{code.replace(".", "")}',
                            'sccs_prod_cat': current_category,
                            'estimated_daily_amount_applied_qx': ''
                            # Default empty string for estimated_daily_amount_applied_qx
                        }
                    )

                    if created:
                        product_types_created += 1
                        self.stdout.write(f'    Created product type: {product_type.name}')

                    current_product_type = product_type

            elif level == 3 and current_subcategory:  # Frame Formulation
                # Extract code and name
                match = re.match(r'(FORM\S+)\s+(.*)', value)
                if match:
                    code = match.group(1)
                    name = match.group(2)

                    # Create or get frame formulation
                    formulation, created = FrameFormulation.objects.get_or_create(
                        formulation_num=code,
                        defaults={
                            'name': name,
                            'unique_id': f'FORM{code.replace(".", "")}',
                            'sccs_product_sub_cat': current_subcategory,
                            'link': ''  # Default empty string for link
                        }
                    )

                    if created:
                        formulations_created += 1
                        self.stdout.write(f'      Created formulation: {formulation.name}')

        # Print summary
        self.stdout.write(self.style.SUCCESS(
            f'Import complete. Created {categories_created} categories, {subcategories_created} subcategories, {product_types_created} product types, and {formulations_created} formulations.'))
