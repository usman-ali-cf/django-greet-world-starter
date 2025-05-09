import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from ingredients.models import (
    Ingredient, GeneralInformation, AppearancePhysicalState, MeltingPoint, BoilingPoint,
    Density, ParticleSize, VapourPressure, PartitionCoefficient, WaterSolubility,
    OrganicSolventSolubility, SurfaceTension, FlashPoint, AutoFlammability, Flammability,
    Explosiveness, OxidisingProperties, PH, DissociationConstant, Viscosity,
    ToxicokineticsEndpointSummary, BasicToxicokinetics, DermalAbsorption,
    AcuteToxicityEndpointSummary, AcuteToxicityOral, AcuteToxicityInhalation,
    AcuteToxicityDermal, IrritationCorrosionEndpointSummary, SkinIrritationCorrosion,
    EyeIrritation, SensitisationEndpointSummary, SkinSensitisation,
    RepeatedDoseToxicityEndpointSummary, Carcinogenicity
)

class Command(BaseCommand):
    help = 'Import ingredients data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Path to JSON file')

    def handle(self, *args, **options):
        file_path = options['file']
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            with transaction.atomic():
                self.import_ingredients(data)
                
            self.stdout.write(self.style.SUCCESS('Successfully imported ingredients data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {e}'))
    
    def import_ingredients(self, data):
        count = 0
        
        for item in data:
            # Extract basic ingredient info
            name = self.get_value(item, 'General information', 'Name')
            ec_number = self.get_value(item, 'General information', 'EC number')
            cas_number = self.get_value(item, 'General information', 'CAS number')
            display_name = self.get_value(item, 'General information', 'Display Name:')
            
            # Create or update ingredient
            ingredient, created = Ingredient.objects.update_or_create(
                cas_number=cas_number,
                defaults={
                    'name': name,
                    'ec_number': ec_number,
                    'display_name': display_name
                }
            )
            
            # Create or update general information
            self.create_general_information(ingredient, item)
            
            # Create or update physical and chemical properties
            self.create_appearance(ingredient, item)
            self.create_melting_point(ingredient, item)
            self.create_boiling_point(ingredient, item)
            self.create_density(ingredient, item)
            self.create_particle_size(ingredient, item)
            self.create_vapour_pressure(ingredient, item)
            self.create_partition_coefficient(ingredient, item)
            self.create_water_solubility(ingredient, item)
            self.create_organic_solvent_solubility(ingredient, item)
            self.create_surface_tension(ingredient, item)
            self.create_flash_point(ingredient, item)
            self.create_auto_flammability(ingredient, item)
            self.create_flammability(ingredient, item)
            self.create_explosiveness(ingredient, item)
            self.create_oxidising_properties(ingredient, item)
            self.create_ph(ingredient, item)
            self.create_dissociation_constant(ingredient, item)
            self.create_viscosity(ingredient, item)
            
            # Create or update toxicology data
            self.create_toxicokinetics_endpoint(ingredient, item)
            self.create_basic_toxicokinetics(ingredient, item)
            self.create_dermal_absorption(ingredient, item)
            self.create_acute_toxicity_endpoint(ingredient, item)
            self.create_acute_toxicity_oral(ingredient, item)
            self.create_acute_toxicity_inhalation(ingredient, item)
            self.create_acute_toxicity_dermal(ingredient, item)
            self.create_irritation_corrosion_endpoint(ingredient, item)
            self.create_skin_irritation_corrosion(ingredient, item)
            self.create_eye_irritation(ingredient, item)
            self.create_sensitisation_endpoint(ingredient, item)
            self.create_skin_sensitisation(ingredient, item)
            self.create_repeated_dose_toxicity_endpoint(ingredient, item)
            self.create_carcinogenicity(ingredient, item)
            
            count += 1
            if count % 10 == 0:
                self.stdout.write(f'Imported {count} ingredients...')
    
    def get_value(self, data, category, field):
        """Helper method to get a value from the data dictionary"""
        if category in data and field in data[category]:
            return data[category][field]
        return None
    
    def create_general_information(self, ingredient, data):
        """Create or update general information for an ingredient"""
        ec_name = self.get_value(data, 'General information', 'EC Name:')
        molecular_formula = self.get_value(data, 'General information', 'Molecular formula:')
        iupac_name = self.get_value(data, 'General information', 'IUPAC Name:')
        composition = self.get_value(data, 'General information', 'Composition:')
        reference_substance_name = self.get_value(data, 'General information', 'Reference substance name:')
        
        GeneralInformation.objects.update_or_create(
            ingredient=ingredient,
            defaults={
                'ec_name': ec_name,
                'molecular_formula': molecular_formula,
                'iupac_name': iupac_name,
                'composition': composition,
                'reference_substance_name': reference_substance_name
            }
        )
    
    def create_appearance(self, ingredient, data):
        """Create or update appearance information for an ingredient"""
        description = self.get_value(data, 'Appearance / physical state / colour', 'Description of key information')
        physical_state = self.get_value(data, 'Appearance / physical state / colour', 'Physical state at 20°C and 1013 hPa:')
        additional_info = self.get_value(data, 'Appearance / physical state / colour', 'Additional information')
        form = self.get_value(data, 'Appearance / physical state / colour', 'Form:')
        colour = self.get_value(data, 'Appearance / physical state / colour', 'Colour:')
        odour = self.get_value(data, 'Appearance / physical state / colour', 'Odour:')
        interpretation = self.get_value(data, 'Appearance / physical state / colour', 'Interpretation of results:')
        remarks = self.get_value(data, 'Appearance / physical state / colour', 'Remarks:')
        conclusions = self.get_value(data, 'Appearance / physical state / colour', 'Conclusions:')
        executive_summary = self.get_value(data, 'Appearance / physical state / colour', 'Executive summary:')
        
        AppearancePhysicalState.objects.update_or_create(
            ingredient=ingredient,
            defaults={
                'description_of_key_information': description,
                'physical_state_at_20c': physical_state,
                'additional_information': additional_info,
                'form': form,
                'colour': colour,
                'odour': odour,
                'interpretation_of_results': interpretation,
                'remarks': remarks,
                'conclusions': conclusions,
                'executive_summary': executive_summary
            }
        )
    
    # Add similar methods for all other models
    # For brevity, I'm not including all of them in this example
    
    def create_melting_point(self, ingredient, data):
        """Create or update melting point information for an ingredient"""
        description = self.get_value(data, 'Melting point / freezing point', 'Description of key information')
        melting_point = self.get_value(data, 'Melting point / freezing point', 'Melting / freezing point at 101 325 Pa:')
        additional_info = self.get_value(data, 'Melting point / freezing point', 'Additional information')
        melting_pt = self.get_value(data, 'Melting point / freezing point', 'Melting / freezing pt.:')
        atm_press = self.get_value(data, 'Melting point / freezing point', 'Atm. press.:')
        interpretation = self.get_value(data, 'Melting point / freezing point', 'Interpretation of results:')
        remarks = self.get_value(data, 'Melting point / freezing point', 'Remarks:')
        conclusions = self.get_value(data, 'Melting point / freezing point', 'Conclusions:')
        executive_summary = self.get_value(data, 'Melting point / freezing point', 'Executive summary:')
        
        MeltingPoint.objects.update_or_create(
            ingredient=ingredient,
            defaults={
                'description_of_key_information': description,
                'melting_freezing_point': melting_point,
                'additional_information': additional_info,
                'melting_freezing_pt': melting_pt,
                'atm_press': atm_press,
                'interpretation_of_results': interpretation,
                'remarks': remarks,
                'conclusions': conclusions,
                'executive_summary': executive_summary
            }
        )
    
    def create_boiling_point(self, ingredient, data):
        """Create or update boiling point information for an ingredient"""
        # Implementation similar to create_melting_point
        pass
    
    # Implement similar methods for all other models
    def create_density(self, ingredient, data):
        pass
    
    def create_particle_size(self, ingredient, data):
        pass
    
    def create_vapour_pressure(self, ingredient, data):
        pass
    
    def create_partition_coefficient(self, ingredient, data):
        pass
    
    def create_water_solubility(self, ingredient, data):
        pass
    
    def create_organic_solvent_solubility(self, ingredient, data):
        pass
    
    def create_surface_tension(self, ingredient, data):
        pass
    
    def create_flash_point(self, ingredient, data):
        pass
    
    def create_auto_flammability(self, ingredient, data):
        pass
    
    def create_flammability(self, ingredient, data):
        pass
    
    def create_explosiveness(self, ingredient, data):
        pass
    
    def create_oxidising_properties(self, ingredient, data):
        pass
    
    def create_ph(self, ingredient, data):
        pass
    
    def create_dissociation_constant(self, ingredient, data):
        pass
    
    def create_viscosity(self, ingredient, data):
        pass
    
    def create_toxicokinetics_endpoint(self, ingredient, data):
        pass
    
    def create_basic_toxicokinetics(self, ingredient, data):
        pass
    
    def create_dermal_absorption(self, ingredient, data):
        pass
    
    def create_acute_toxicity_endpoint(self, ingredient, data):
        pass
    
    def create_acute_toxicity_oral(self, ingredient, data):
        pass
    
    def create_acute_toxicity_inhalation(self, ingredient, data):
        pass
    
    def create_acute_toxicity_dermal(self, ingredient, data):
        pass
    
    def create_irritation_corrosion_endpoint(self, ingredient, data):
        pass
    
    def create_skin_irritation_corrosion(self, ingredient, data):
        pass
    
    def create_eye_irritation(self, ingredient, data):
        pass
    
    def create_sensitisation_endpoint(self, ingredient, data):
        pass
    
    def create_skin_sensitisation(self, ingredient, data):
        pass
    
    def create_repeated_dose_toxicity_endpoint(self, ingredient, data):
        pass
    
    def create_carcinogenicity(self, ingredient, data):
        pass
