import csv
import datetime
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from ingredients.models import Ingredient, SCCSOpinions


class Command(BaseCommand):
    help = 'Import SCCS opinions from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file containing SCCS opinions')
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing records if they exist',
        )

    def get_or_create_ingredient(self, name, cas_no, ec_no):
        """Get or create an Ingredient with the given details"""
        # Handle multiple CAS numbers (take the first one for lookup)
        primary_cas = cas_no.split('/')[0].strip() if cas_no else None

        # Try to find existing ingredient by CAS number
        ingredient = None
        if primary_cas:
            ingredient = Ingredient.objects.filter(cas_number=primary_cas).first()

        # If not found by CAS, try by name
        if not ingredient and name:
            ingredient = Ingredient.objects.filter(name=name).first()

        # If still not found, create a new ingredient
        if not ingredient:
            ingredient = Ingredient.objects.create(
                name=name,
                cas_number=cas_no,
                ec_number=ec_no,
                display_name=name
            )
            self.stdout.write(self.style.SUCCESS(f"Created new ingredient: {name}"))
        else:
            # Update existing ingredient if needed
            updated = False
            if not ingredient.name and name:
                ingredient.name = name
                updated = True
            if not ingredient.ec_number and ec_no:
                ingredient.ec_number = ec_no
                updated = True
            if updated:
                ingredient.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Updated existing ingredient: {ingredient.name or ingredient.cas_number}"))

        return ingredient

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        update_existing = options['update']

        if not os.path.exists(csv_file_path):
            raise CommandError(f"File not found: {csv_file_path}")

        self.stdout.write(self.style.SUCCESS(f"Importing SCCS opinions from {csv_file_path}..."))

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
                            # Extract data from row
                            sccs_opinion_name = row.get('SCCS Opinion Name', '').strip()
                            ingredient_name = row.get('Ingredient Name', '').strip()
                            opinion_type = row.get('Type', '').strip()
                            cas_no = row.get('CAS No.', '').strip()
                            ec_no = row.get('EC No.', '').strip()
                            sccs_number = row.get('SCCS Number', '').strip()
                            adopted_on_str = row.get('Adopted on', '').strip()
                            link = row.get('Link', '').strip()

                            # Skip empty rows
                            if not sccs_opinion_name and not ingredient_name:
                                continue

                            adopted_on = adopted_on_str

                            # Get or create the ingredient
                            ingredient = self.get_or_create_ingredient(ingredient_name, cas_no, ec_no)

                            # Check if opinion already exists
                            existing_opinion = None

                            if existing_opinion and not update_existing:
                                skipped_count += 1
                                self.stdout.write(self.style.WARNING(
                                    f"Skipped existing SCCS opinion: {sccs_opinion_name} (SCCS Number: {sccs_number})"
                                ))
                                continue

                            if existing_opinion:
                                # Update existing opinion
                                existing_opinion.sccs_opinion_name = sccs_opinion_name
                                existing_opinion.ingredient_name = ingredient_name
                                existing_opinion.type = opinion_type
                                existing_opinion.cas_no = cas_no
                                existing_opinion.ec_no = ec_no
                                existing_opinion.adopted_on = adopted_on
                                existing_opinion.link = link
                                existing_opinion.ingredient = ingredient
                                existing_opinion.save()

                                updated_count += 1
                                self.stdout.write(self.style.SUCCESS(
                                    f"Updated SCCS opinion: {sccs_opinion_name} (SCCS Number: {sccs_number})"
                                ))
                            else:
                                # Create new opinion
                                SCCSOpinions.objects.create(
                                    sccs_opinion_name=sccs_opinion_name,
                                    ingredient_name=ingredient_name,
                                    type=opinion_type,
                                    cas_no=cas_no,
                                    ec_no=ec_no,
                                    sccs_number=sccs_number,
                                    adopted_on=adopted_on,
                                    link=link,
                                    ingredient=ingredient
                                )

                                created_count += 1
                                self.stdout.write(self.style.SUCCESS(
                                    f"Created SCCS opinion: {sccs_opinion_name} (SCCS Number: {sccs_number})"
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
