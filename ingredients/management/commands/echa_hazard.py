import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from ingredients.models import Ingredient, ECHACLPHazard


class Command(BaseCommand):
    help = 'Import ECHA CLP hazard data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file containing ECHA CLP hazard data')
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

        self.stdout.write(self.style.SUCCESS(f"Importing ECHA CLP hazard data from {csv_file_path}..."))

        # Count for reporting
        created_count = 0
        updated_count = 0
        error_count = 0
        skipped_count = 0

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
                # Skip the first row (header) and second row (subheader)
                reader = csv.reader(csv_file)
                next(reader)  # Skip main header
                next(reader)  # Skip subheader

                with transaction.atomic():
                    for row in reader:
                        try:
                            # Skip empty rows
                            if not any(cell.strip() for cell in row):
                                continue

                            # Extract data from row based on column positions
                            index_no = row[0].strip()
                            international_chemical_identification = row[1].strip()
                            ec_no = row[2].strip()
                            cas_no = row[3].strip()

                            # Classification fields
                            classification_hazard_class = row[4].strip()
                            classification_hazard_statement = row[5].strip()

                            # Labelling fields
                            labelling_pictogram = row[6].strip()
                            labelling_hazard_statement = row[7].strip()
                            labelling_supplement_hazard = row[8].strip()

                            # Other fields
                            specific_conc_limits = row[9].strip() if len(row) > 9 else ""
                            notes = row[10].strip() if len(row) > 10 else ""
                            atp_inserted_updated = row[11].strip() if len(row) > 11 else ""

                            # Try to find the associated ingredient
                            if len(cas_no) > 15 or len(international_chemical_identification) > 1000:
                                continue
                            ingredient = None
                            if cas_no:
                                ingredient = Ingredient.objects.filter(cas_number=cas_no).first()
                            if not ingredient and ec_no:
                                ingredient = Ingredient.objects.filter(ec_number=ec_no).first()
                            if not ingredient and len(cas_no) < 15:
                                ingredient = Ingredient.objects.create(
                                    name=international_chemical_identification,
                                    cas_number=cas_no,
                                    ec_number=ec_no,
                                    display_name=international_chemical_identification
                                )

                            # Check if hazard record already exists
                            existing_hazard = None
                            if index_no:
                                existing_hazard = ECHACLPHazard.objects.filter(index_no=index_no).first()
                            elif cas_no:
                                existing_hazard = ECHACLPHazard.objects.filter(cas_no=cas_no).first()

                            if existing_hazard and not update_existing:
                                skipped_count += 1
                                self.stdout.write(self.style.WARNING(
                                    f"Skipped existing ECHA CLP hazard: {international_chemical_identification} (Index No: {index_no})"
                                ))
                                continue

                            if existing_hazard:
                                # Update existing hazard record
                                if len(cas_no) > 15:
                                    continue
                                existing_hazard.international_chemical_identification = international_chemical_identification
                                existing_hazard.ec_no = ec_no
                                existing_hazard.cas_no = cas_no
                                existing_hazard.classification_hazard_class_category_codes = classification_hazard_class
                                existing_hazard.classification_hazard_statement_codes = classification_hazard_statement
                                existing_hazard.labelling_pictogram_signal_word_codes = labelling_pictogram
                                existing_hazard.labelling_hazard_statement_codes = labelling_hazard_statement
                                existing_hazard.labelling_suppliment_hazard_statement_codes = labelling_supplement_hazard
                                existing_hazard.specific_conc_limits_m_factors = specific_conc_limits
                                existing_hazard.notes = notes
                                existing_hazard.atp_inserted_updated = atp_inserted_updated

                                if ingredient and existing_hazard.ingredient != ingredient:
                                    existing_hazard.ingredient = ingredient

                                existing_hazard.save()

                                updated_count += 1
                                if updated_count % 100 == 0:
                                    self.stdout.write(self.style.SUCCESS(
                                        f"Updated {updated_count} ECHA CLP hazard records..."
                                    ))
                            else:
                                # Create new hazard record
                                if len(cas_no) > 15:
                                    continue
                                ECHACLPHazard.objects.create(
                                    index_no=index_no,
                                    international_chemical_identification=international_chemical_identification,
                                    ec_no=ec_no,
                                    cas_no=cas_no,
                                    classification_hazard_class_category_codes=classification_hazard_class,
                                    classification_hazard_statement_codes=classification_hazard_statement,
                                    labelling_pictogram_signal_word_codes=labelling_pictogram,
                                    labelling_hazard_statement_codes=labelling_hazard_statement,
                                    labelling_suppliment_hazard_statement_codes=labelling_supplement_hazard,
                                    specific_conc_limits_m_factors=specific_conc_limits,
                                    notes=notes,
                                    atp_inserted_updated=atp_inserted_updated,
                                    ingredient=ingredient
                                )

                                created_count += 1
                                if created_count % 100 == 0:
                                    self.stdout.write(self.style.SUCCESS(
                                        f"Created {created_count} ECHA CLP hazard records..."
                                    ))

                        except Exception as e:
                            error_count += 1

                            self.stdout.write(self.style.ERROR(f"Error processing row: {e}"))
                            self.stdout.write(self.style.ERROR(f"Row data: {row}"))
                            break

            # Print summary
            self.stdout.write(self.style.SUCCESS("\nImport complete."))
            self.stdout.write(self.style.SUCCESS(f"Created: {created_count}"))
            self.stdout.write(self.style.SUCCESS(f"Updated: {updated_count}"))
            self.stdout.write(self.style.SUCCESS(f"Skipped: {skipped_count}"))
            self.stdout.write(self.style.SUCCESS(f"Errors: {error_count}"))

        except Exception as e:
            raise CommandError(f"Error importing CSV: {e}")