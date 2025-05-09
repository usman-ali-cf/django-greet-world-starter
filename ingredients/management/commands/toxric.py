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
                            toxicity_value = row.get('Toxicity Value', '').strip()
                            ld50_toxicity_category = row.get('LD50 Toxicity Category', '').strip()

                            # Convert toxicity_value to float if possible
                            try:
                                toxicity_value_float = float(toxicity_value) if toxicity_value else None
                            except ValueError:
                                toxicity_value_float = None
                                self.stdout.write(self.style.WARNING(
                                    f"Invalid toxicity value: {toxicity_value} for {name}. Keeping as string."
                                ))

                            # Try to find the associated ingredient
                            ingredient = None
                            # if name:
                            #     # Try exact match on name
                            #     ingredient = Ingredient.objects.filter(name__iexact=name).first()
                            #
                            #     # If not found, try partial match
                            #     if not ingredient:
                            #         ingredient = Ingredient.objects.filter(name__icontains=name).first()

                            # If still not found, try with IUPAC name
                            # if not ingredient and iupac_name:
                            #     ingredient = Ingredient.objects.filter(
                            #         general_information__iupac_name__icontains=iupac_name
                            #     ).first()

                            # Check if toxicity record already exists
                            existing_toxicity = None
                            # if taid:
                            #     existing_toxicity = TOXRICLD50.objects.filter(taid=taid).first()
                            # elif name and ld50_toxicity_category:
                            #     existing_toxicity = TOXRICLD50.objects.filter(
                            #         name=name,
                            #         ld50_toxicity_category=ld50_toxicity_category
                            #     ).first()

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
                                existing_toxicity.toxicity_value = toxicity_value
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
                                    toxicity_value=toxicity_value,
                                    ld50_toxicity_category=ld50_toxicity_category,
                                    is_toxicity=None,
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