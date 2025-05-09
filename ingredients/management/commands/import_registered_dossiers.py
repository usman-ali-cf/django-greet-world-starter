import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from ingredients.models import Ingredient, ALLRegisteredDossiers


class Command(BaseCommand):
    help = 'Import registered dossiers data from a CSV file into ALLRegisteredDossiers model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file containing registered dossiers data')
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

        self.stdout.write(self.style.SUCCESS(f"Importing registered dossiers data from {csv_file_path}..."))

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
                            name = row.get('Name', '').strip()
                            ec_list_number = row.get('EC / List Number', '').strip()
                            cas_number = row.get('Cas Number', '').strip()
                            echa_chem_id = row.get('ECHA CHEM ID', '').strip()
                            registration_status = row.get('Registration Status', '').strip()
                            registration_type = row.get('Registration Type', '').strip()
                            submission_type = row.get('Submission Type', '').strip()
                            total_tonnage_band = row.get('Total tonnage Band', '').strip()
                            tonnage_band_min = row.get('Tonnage Band Min', '').strip()
                            tonnage_band_max = row.get('Tonnage Band Max', '').strip()

                            # Parse date if available
                            last_updated_str = row.get('Last Updated', '').strip()
                            last_updated = None
                            if last_updated_str:
                                try:
                                    # Assuming date format is DD-MM-YYYY
                                    last_updated = datetime.strptime(last_updated_str, '%d-%m-%Y').date()
                                except ValueError:
                                    self.stdout.write(self.style.WARNING(
                                        f"Invalid date format for Last Updated: {last_updated_str}. Skipping date conversion."
                                    ))

                            factsheet_url = row.get('Factsheet URL COMPLEX COMPONENTS + PHYS/CHEM PROPS + TOX',
                                                    '').strip()
                            substance_information_page = row.get('Substance Information Page', '').strip()
                            echa_chem_dossier = row.get('ECHA CHEM DOSSIER', '').strip()
                            reference = row.get('REFERENCE', '').strip()

                            # Try to find the associated ingredient
                            ingredient = None
                            if cas_number and cas_number != '-':
                                ingredient = Ingredient.objects.filter(cas_number=cas_number).first()
                            if not ingredient and ec_list_number and ec_list_number != '-':
                                ingredient = Ingredient.objects.filter(ec_number=ec_list_number).first()

                            # Check if dossier record already exists
                            existing_dossier = None
                            # if echa_chem_id:
                            #     existing_dossier = ALLRegisteredDossiers.objects.filter(
                            #         echa_chem_id=echa_chem_id,
                            #         registration_type=registration_type
                            #     ).first()

                            if existing_dossier and not update_existing:
                                skipped_count += 1
                                self.stdout.write(self.style.WARNING(
                                    f"Skipped existing dossier: {name} (ECHA CHEM ID: {echa_chem_id}, Type: {registration_type})"
                                ))
                                continue

                            if existing_dossier:
                                # Update existing dossier record
                                existing_dossier.ec_list_number = ec_list_number
                                existing_dossier.cas_number = cas_number
                                existing_dossier.registration_status = registration_status
                                existing_dossier.submission_type = submission_type
                                existing_dossier.total_tonnage_band = total_tonnage_band
                                existing_dossier.tonnage_band_min = tonnage_band_min
                                existing_dossier.tonnage_band_max = tonnage_band_max

                                if last_updated:
                                    existing_dossier.last_updated = last_updated

                                existing_dossier.factsheet_url = factsheet_url
                                existing_dossier.substance_information_page = substance_information_page
                                existing_dossier.echa_chem_dossier = echa_chem_dossier

                                if ingredient and existing_dossier.ingredient != ingredient:
                                    existing_dossier.ingredient = ingredient

                                existing_dossier.save()

                                updated_count += 1
                                if updated_count % 50 == 0:
                                    self.stdout.write(self.style.SUCCESS(
                                        f"Updated {updated_count} registered dossier records..."
                                    ))
                            else:
                                # Create new dossier record
                                ALLRegisteredDossiers.objects.create(
                                    ec_list_number=ec_list_number,
                                    cas_number=cas_number,
                                    echa_chem_id=echa_chem_id,
                                    registration_status=registration_status,
                                    registration_type=registration_type,
                                    submission_type=submission_type,
                                    total_tonnage_band=total_tonnage_band,
                                    tonnage_band_min=tonnage_band_min,
                                    tonnage_band_max=tonnage_band_max,
                                    last_updated=last_updated,
                                    factsheet_url=factsheet_url,
                                    substance_information_page=substance_information_page,
                                    echa_chem_dossier=echa_chem_dossier,
                                    ingredient=ingredient
                                )

                                created_count += 1
                                if created_count % 50 == 0:
                                    self.stdout.write(self.style.SUCCESS(
                                        f"Created {created_count} registered dossier records..."
                                    ))

                        except Exception as e:
                            error_count += 1
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