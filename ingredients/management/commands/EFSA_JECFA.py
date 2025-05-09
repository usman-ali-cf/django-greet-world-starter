import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from ingredients.models import Ingredient, EFSA_JECFAFoodNoNOEAL


class Command(BaseCommand):
    help = 'Import EFSA/JECFA food additives data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Path to CSV file')

    def handle(self, *args, **options):
        file_path = options['file']

        if not file_path:
            self.stdout.write(self.style.ERROR('Please provide a file path using --file'))
            return

        try:
            # Process the CSV file
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                self.import_efsa_data(csv_file)

            self.stdout.write(self.style.SUCCESS('Successfully imported EFSA/JECFA food additives data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {e}'))

    def import_efsa_data(self, csv_file):
        reader = csv.DictReader(csv_file)

        # Track statistics
        records_created = 0
        records_skipped = 0
        ingredients_created = 0

        # Process each row in the CSV
        with transaction.atomic():
            for row in reader:
                # Skip rows with empty essential data
                if not row.get('EFSA Ingredient Name'):
                    records_skipped += 1
                    continue

                # Extract key data
                efsa_name = row.get('EFSA Ingredient Name', '').strip()
                cas_no = row.get('CAS No.', '').strip()

                # Clean up the E number (remove extra dots)
                ec_no = row.get('E No.', '').strip()
                if ec_no in ['.', '..', '...', '....', '.....', '......']:
                    ec_no = ''

                # Try to find a matching ingredient by name or CAS number
                ingredient = None

                if cas_no and cas_no not in ['.', '..', '...', '....', '.....', '......']:
                    # Try to find by CAS number first (more reliable)
                    ingredient = Ingredient.objects.filter(cas_number=cas_no).first()

                # If not found by CAS, try by name
                if not ingredient and efsa_name:
                    ingredient = Ingredient.objects.filter(name__icontains=efsa_name).first()
                    if not ingredient:
                        # Try with display name
                        ingredient = Ingredient.objects.filter(display_name__icontains=efsa_name).first()

                # If still no ingredient found, create a new one
                if not ingredient:
                    # Only create if we have at least a CAS number or EC number
                    valid_cas = cas_no and cas_no not in ['.', '..', '...', '....', '.....', '......']
                    valid_ec = ec_no and ec_no not in ['.', '..', '...', '....', '.....', '......']

                    if valid_cas or valid_ec:
                        ingredient = Ingredient.objects.create(
                            name=efsa_name,
                            display_name=efsa_name,
                            cas_number=cas_no if valid_cas else None,
                            ec_number=ec_no if valid_ec else None
                        )
                        ingredients_created += 1
                        self.stdout.write(f"Created new ingredient: {efsa_name}")

                # Always create a new EFSA/JECFA record
                EFSA_JECFAFoodNoNOEAL.objects.create(
                    efsa_ingredient_name=efsa_name,
                    type=row.get('Type', '').strip(),
                    cas_no=cas_no,
                    ec_no=ec_no,
                    food_additive_group=row.get('Food Additive Group', '').strip(),
                    synonym_names=row.get('Synonym Name(s) (From EFSA Datasheet)', '').strip(),
                    conditions_of_use=row.get('Conditions of use (From EFSA Datasheet)', '').strip(),
                    legislations=row.get('Legislations (From EFSA datasheet, specifically for GROUPS)', '').strip(),
                    fl_no=row.get('FL No.', '').strip(),
                    coe_no=row.get('CoE No.', '').strip(),
                    un_fao=row.get('UN-FAO JECFA No', '').strip(),
                    ingredient=ingredient,
                )

                records_created += 1

                # Log progress periodically
                if records_created % 100 == 0:
                    self.stdout.write(f"Processed {records_created} records...")

        self.stdout.write(self.style.SUCCESS(
            f"Import complete. Created: {records_created}, Skipped: {records_skipped}, "
            f"New ingredients created: {ingredients_created}"
        ))