import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from ingredients.models import Ingredient, TOXRICLD50


class Command(BaseCommand):
    help = 'Import toxicity LD50 data from a CSV file into TOXRICLD50 model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file containing toxicity LD50 data')
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing records if they exist',
        )

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        update_existing = options['update']

        if not os.path.exists(csv_file_path):
            raise CommandError(f"File not found: {csv_file_path}")

        self.stdout.write(self.style.SUCCESS(f"Importing toxicity LD50 data from {csv_file_path}..."))

        # Count for reporting
        created_count = 0
        updated_count = 0
        error_count = 0
        skipped_count = 0

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)

                with transaction.atomic():
                    for row in reader:
                        try:
                            # Skip empty rows
                            if not any(value.strip() for value in row.values()):
                                continue

                            # Extract data from row
                            taid = row.get('TAID', '').strip()
                            name = row.get('Name', '').strip()
                            iupac_name = row.get('IUPAC Name', '').strip()
                            pubchem_cid = row.get('PubChem CID', '').strip()
                            canonical_smiles = row.get('Canonical SMILES', '').strip()
                            inchikey = row.get('InChIKey', '').strip()
                            toxicity_value = row.get('Toxicity Value', '0').strip()
                            ld50_toxicity_category = row.get('LD50 Toxicity Category', '').strip()



                            # Try to find the associated ingredient
                            ingredient = None


                            # Check if toxicity record already exists
                            existing_toxicity = None

                            if existing_toxicity and not update_existing:
                                skipped_count += 1
                                self.stdout.write(self.style.WARNING(
                                    f"Skipped existing toxicity record: {name} (TAID: {taid})"
                                ))
                                continue

                            if existing_toxicity:
                                # Update existing toxicity record
                                existing_toxicity.name = name
                                existing_toxicity.iupac_name = iupac_name
                                existing_toxicity.pubchem_cid = pubchem_cid
                                existing_toxicity.canonical_smiles = canonical_smiles
                                existing_toxicity.inchikey = inchikey
                                existing_toxicity.is_toxicity = True if toxicity_value == '1' else False
                                existing_toxicity.ld50_toxicity_category = ld50_toxicity_category
                                # existing_toxicity.is_toxicity = True if toxicity_value_float else False

                                if ingredient and existing_toxicity.ingredient != ingredient:
                                    existing_toxicity.ingredient = ingredient

                                existing_toxicity.save()

                                updated_count += 1
                                if updated_count % 50 == 0:
                                    self.stdout.write(self.style.SUCCESS(
                                        f"Updated {updated_count} toxicity LD50 records..."
                                    ))
                            else:
                                # Create new toxicity record
                                TOXRICLD50.objects.create(
                                    taid=taid,
                                    name=name,
                                    iupac_name=iupac_name,
                                    pubchem_cid=pubchem_cid,
                                    canonical_smiles=canonical_smiles,
                                    inchikey=inchikey,
                                    toxicity_value=0,
                                    ld50_toxicity_category=ld50_toxicity_category,
                                    is_toxicity=True if toxicity_value == '1' else False,
                                    ingredient=ingredient
                                )

                                created_count += 1
                                if created_count % 50 == 0:
                                    self.stdout.write(self.style.SUCCESS(
                                        f"Created {created_count} toxicity LD50 records..."
                                    ))

                        except Exception as e:
                            error_count += 1
                            print(e)
                            break
                            self.stdout.write(self.style.ERROR(f"Error processing row: {e}"))
                            self.stdout.write(self.style.ERROR(f"Row data: {row}"))

            # Print summary
            self.stdout.write(self.style.SUCCESS("\nImport complete."))
            self.stdout.write(self.style.SUCCESS(f"Created: {created_count}"))
            self.stdout.write(self.style.SUCCESS(f"Updated: {updated_count}"))
            self.stdout.write(self.style.SUCCESS(f"Skipped: {skipped_count}"))
            self.stdout.write(self.style.SUCCESS(f"Errors: {error_count}"))

        except Exception as e:
            raise CommandError(f"Error importing CSV: {e}")