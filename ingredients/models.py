from django.db import models


class Ingredient(models.Model):
    """
    Main ingredient model that stores basic identification information.
    All other ingredient data models reference this model.
    """
    name = models.TextField(blank=True, null=True, verbose_name="Name")
    ec_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="EC Number")
    cas_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="CAS Number")
    display_name = models.TextField(blank=True, null=True, verbose_name="Display Name")

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        ordering = ['name']

    def __str__(self):
        if self.display_name:
            return self.display_name
        return self.name or self.cas_number or "Unnamed Ingredient"


class GeneralInformation(models.Model):
    """
    General information about the ingredient
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='general_information',
        verbose_name="Ingredient"
    )
    ec_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="EC Name")
    molecular_formula = models.CharField(max_length=255, blank=True, null=True, verbose_name="Molecular Formula")
    iupac_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="IUPAC Name")
    composition = models.TextField(blank=True, null=True, verbose_name="Composition")
    reference_substance_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Reference Substance Name")
    image = models.ImageField(upload_to='ingredients/', blank=True, null=True, verbose_name="Image")

    class Meta:
        verbose_name = "General Information"
        verbose_name_plural = "General Information"

    def __str__(self):
        return f"General Information for {self.ingredient}"


class AppearancePhysicalState(models.Model):
    """
    Appearance, physical state, and color information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='appearance',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    physical_state_at_20c = models.CharField(max_length=255, blank=True, null=True, verbose_name="Physical State at 20°C and 1013 hPa")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    form = models.CharField(max_length=255, blank=True, null=True, verbose_name="Form")
    colour = models.CharField(max_length=255, blank=True, null=True, verbose_name="Colour")
    odour = models.CharField(max_length=255, blank=True, null=True, verbose_name="Odour")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Appearance / Physical State"
        verbose_name_plural = "Appearance / Physical State"

    def __str__(self):
        return f"Appearance for {self.ingredient}"


class MeltingPoint(models.Model):
    """
    Melting point / freezing point information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='melting_point',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    melting_freezing_point = models.CharField(max_length=255, blank=True, null=True, verbose_name="Melting / Freezing Point at 101 325 Pa")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    melting_freezing_pt = models.CharField(max_length=255, blank=True, null=True, verbose_name="Melting / Freezing Pt.")
    atm_press = models.CharField(max_length=255, blank=True, null=True, verbose_name="Atm. Press.")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Melting Point / Freezing Point"
        verbose_name_plural = "Melting Points / Freezing Points"

    def __str__(self):
        return f"Melting Point for {self.ingredient}"


class BoilingPoint(models.Model):
    """
    Boiling point information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='boiling_point',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    boiling_point = models.CharField(max_length=255, blank=True, null=True, verbose_name="Boiling Point at 101 325 Pa")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    boiling_pt = models.CharField(max_length=255, blank=True, null=True, verbose_name="Boiling Pt.")
    atm_press = models.CharField(max_length=255, blank=True, null=True, verbose_name="Atm. Press.")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Boiling Point"
        verbose_name_plural = "Boiling Points"

    def __str__(self):
        return f"Boiling Point for {self.ingredient}"


class Density(models.Model):
    """
    Density information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='density',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    relative_density_at_20c = models.CharField(max_length=255, blank=True, null=True, verbose_name="Relative Density at 20C")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    density = models.CharField(max_length=255, blank=True, null=True, verbose_name="Density")
    temp = models.CharField(max_length=255, blank=True, null=True, verbose_name="Temp.")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Density"
        verbose_name_plural = "Densities"

    def __str__(self):
        return f"Density for {self.ingredient}"


class ParticleSize(models.Model):
    """
    Particle size distribution information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='particle_size',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    percentile = models.CharField(max_length=255, blank=True, null=True, verbose_name="Percentile")
    mean = models.CharField(max_length=255, blank=True, null=True, verbose_name="Mean")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Particle Size Distribution"
        verbose_name_plural = "Particle Size Distributions"

    def __str__(self):
        return f"Particle Size for {self.ingredient}"


class VapourPressure(models.Model):
    """
    Vapour pressure information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='vapour_pressure',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    vapour_pressure = models.CharField(max_length=255, blank=True, null=True, verbose_name="Vapour Pressure")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    temp = models.CharField(max_length=255, blank=True, null=True, verbose_name="Temp.")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Vapour Pressure"
        verbose_name_plural = "Vapour Pressures"

    def __str__(self):
        return f"Vapour Pressure for {self.ingredient}"


class PartitionCoefficient(models.Model):
    """
    Partition coefficient information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='partition_coefficient',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    log_kow = models.CharField(max_length=255, blank=True, null=True, verbose_name="Log Kow (Log Pow)")
    at_temperature = models.CharField(max_length=255, blank=True, null=True, verbose_name="At the Temperature of")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Type")
    partition_coefficient = models.CharField(max_length=255, blank=True, null=True, verbose_name="Partition Coefficient")
    temp = models.CharField(max_length=255, blank=True, null=True, verbose_name="Temp.")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Partition Coefficient"
        verbose_name_plural = "Partition Coefficients"

    def __str__(self):
        return f"Partition Coefficient for {self.ingredient}"


class WaterSolubility(models.Model):
    """
    Water solubility information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='water_solubility',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    water_solubility = models.CharField(max_length=255, blank=True, null=True, verbose_name="Water Solubility")
    at_temperature = models.CharField(max_length=255, blank=True, null=True, verbose_name="At the Temperature of")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    temp = models.CharField(max_length=255, blank=True, null=True, verbose_name="Temp.")
    remarks_on_result = models.TextField(blank=True, null=True, verbose_name="Remarks on Result")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")

    class Meta:
        verbose_name = "Water Solubility"
        verbose_name_plural = "Water Solubilities"

    def __str__(self):
        return f"Water Solubility for {self.ingredient}"


class OrganicSolventSolubility(models.Model):
    """
    Solubility in organic solvents / fat solubility information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='organic_solvent_solubility',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Solubility in Organic Solvents / Fat"
        verbose_name_plural = "Solubilities in Organic Solvents / Fat"

    def __str__(self):
        return f"Organic Solvent Solubility for {self.ingredient}"


class SurfaceTension(models.Model):
    """
    Surface tension information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='surface_tension',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    surface_tension = models.CharField(max_length=255, blank=True, null=True, verbose_name="Surface Tension")
    temp = models.CharField(max_length=255, blank=True, null=True, verbose_name="Temp.")
    conc = models.CharField(max_length=255, blank=True, null=True, verbose_name="Conc.")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Surface Tension"
        verbose_name_plural = "Surface Tensions"

    def __str__(self):
        return f"Surface Tension for {self.ingredient}"


class FlashPoint(models.Model):
    """
    Flash point information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='flash_point',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    flash_point_at_101325_pa = models.CharField(max_length=255, blank=True, null=True, verbose_name="Flash Point at 101 325 Pa")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    flash_point = models.CharField(max_length=255, blank=True, null=True, verbose_name="Flash Point")
    atm_press = models.CharField(max_length=255, blank=True, null=True, verbose_name="Atm. Press.")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Flash Point"
        verbose_name_plural = "Flash Points"

    def __str__(self):
        return f"Flash Point for {self.ingredient}"


class AutoFlammability(models.Model):
    """
    Auto flammability information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='auto_flammability',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    autoflammability_temperature = models.CharField(max_length=255, blank=True, null=True, verbose_name="Autoflammability / Self-ignition Temperature at 101 325 Pa")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    auto_ignition_temperature = models.CharField(max_length=255, blank=True, null=True, verbose_name="Auto-ignition Temperature")
    atm_press = models.CharField(max_length=255, blank=True, null=True, verbose_name="Atm. Press.")
    relative_self_ignition_temperature = models.CharField(max_length=255, blank=True, null=True, verbose_name="Relative Self-ignition Temperature")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Auto Flammability"
        verbose_name_plural = "Auto Flammabilities"

    def __str__(self):
        return f"Auto Flammability for {self.ingredient}"


class Flammability(models.Model):
    """
    Flammability information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='flammability',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    flammability = models.CharField(max_length=255, blank=True, null=True, verbose_name="Flammability")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    parameter = models.CharField(max_length=255, blank=True, null=True, verbose_name="Parameter")
    value = models.CharField(max_length=255, blank=True, null=True, verbose_name="Value")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Flammability"
        verbose_name_plural = "Flammabilities"

    def __str__(self):
        return f"Flammability for {self.ingredient}"


class Explosiveness(models.Model):
    """
    Explosiveness information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='explosiveness',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    explosiveness = models.CharField(max_length=255, blank=True, null=True, verbose_name="Explosiveness")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Explosiveness"
        verbose_name_plural = "Explosivenesses"

    def __str__(self):
        return f"Explosiveness for {self.ingredient}"


class OxidisingProperties(models.Model):
    """
    Oxidising properties information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='oxidising_properties',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    oxidising_properties = models.CharField(max_length=255, blank=True, null=True, verbose_name="Oxidising Properties")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    sample_tested = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sample Tested")
    parameter = models.CharField(max_length=255, blank=True, null=True, verbose_name="Parameter")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Oxidising Properties"
        verbose_name_plural = "Oxidising Properties"

    def __str__(self):
        return f"Oxidising Properties for {self.ingredient}"


class PH(models.Model):
    """
    pH information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='ph',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "pH"
        verbose_name_plural = "pH Values"

    def __str__(self):
        return f"pH for {self.ingredient}"


class DissociationConstant(models.Model):
    """
    Dissociation constant information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='dissociation_constant',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Dissociation Constant"
        verbose_name_plural = "Dissociation Constants"

    def __str__(self):
        return f"Dissociation Constant for {self.ingredient}"


class Viscosity(models.Model):
    """
    Viscosity information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='viscosity',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    viscosity = models.CharField(max_length=255, blank=True, null=True, verbose_name="Viscosity")
    at_temperature = models.CharField(max_length=255, blank=True, null=True, verbose_name="At the Temperature of")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    temp = models.CharField(max_length=255, blank=True, null=True, verbose_name="Temp.")
    parameter = models.CharField(max_length=255, blank=True, null=True, verbose_name="Parameter")
    value = models.CharField(max_length=255, blank=True, null=True, verbose_name="Value")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Viscosity"
        verbose_name_plural = "Viscosities"

    def __str__(self):
        return f"Viscosity for {self.ingredient}"


class ToxicokineticsEndpointSummary(models.Model):
    """
    Toxicokinetics, metabolism and distribution - Endpoint summary
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='toxicokinetics_endpoint',
        verbose_name="Ingredient"
    )
    absorption_rate_oral = models.CharField(max_length=255, blank=True, null=True, verbose_name="Absorption Rate - Oral (%)")
    absorption_rate_dermal = models.CharField(max_length=255, blank=True, null=True, verbose_name="Absorption Rate - Dermal (%)")
    absorption_rate_inhalation = models.CharField(max_length=255, blank=True, null=True, verbose_name="Absorption Rate - Inhalation (%)")

    class Meta:
        verbose_name = "Toxicokinetics Endpoint Summary"
        verbose_name_plural = "Toxicokinetics Endpoint Summaries"

    def __str__(self):
        return f"Toxicokinetics Endpoint Summary for {self.ingredient}"


class BasicToxicokinetics(models.Model):
    """
    Basic toxicokinetics information
    """
    ingredient = models.OneToOneField(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name='basic_toxicokinetics',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")

    class Meta:
        verbose_name = "Basic Toxicokinetics"
        verbose_name_plural = "Basic Toxicokinetics"

    def __str__(self):
        return f"Basic Toxicokinetics for {self.ingredient}"


class DermalAbsorption(models.Model):
    """
    Dermal absorption information
    """
    ingredient = models.OneToOneField(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='dermal_absorption',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    reference_type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Reference Type")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Title")
    author = models.CharField(max_length=255, blank=True, null=True, verbose_name="Author")
    year = models.CharField(max_length=50, blank=True, null=True, verbose_name="Year")
    bibliographic_source = models.TextField(blank=True, null=True, verbose_name="Bibliographic Source")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Dermal Absorption"
        verbose_name_plural = "Dermal Absorptions"

    def __str__(self):
        return f"Dermal Absorption for {self.ingredient}"


class AcuteToxicityEndpointSummary(models.Model):
    """
    Acute Toxicity - Endpoint summary
    """
    ingredient = models.OneToOneField(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='acute_toxicity_endpoint',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    endpoint_conclusion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Endpoint Conclusion")
    dose_descriptor = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dose Descriptor")
    value = models.CharField(max_length=255, blank=True, null=True, verbose_name="Value")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    justification = models.TextField(blank=True, null=True, verbose_name="Justification for Classification or Non-classification")

    class Meta:
        verbose_name = "Acute Toxicity Endpoint Summary"
        verbose_name_plural = "Acute Toxicity Endpoint Summaries"

    def __str__(self):
        return f"Acute Toxicity Endpoint Summary for {self.ingredient}"


class AcuteToxicityOral(models.Model):
    """
    Acute Toxicity: oral information
    """
    ingredient = models.OneToOneField(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='acute_toxicity_oral',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    reference_type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Reference Type")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Title")
    author = models.CharField(max_length=255, blank=True, null=True, verbose_name="Author")
    year = models.CharField(max_length=50, blank=True, null=True, verbose_name="Year")
    bibliographic_source = models.TextField(blank=True, null=True, verbose_name="Bibliographic Source")
    dose_descriptor = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dose Descriptor")
    effect_level = models.CharField(max_length=255, blank=True, null=True, verbose_name="Effect Level")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Acute Toxicity: Oral"
        verbose_name_plural = "Acute Toxicity: Oral"

    def __str__(self):
        return f"Acute Toxicity: Oral for {self.ingredient}"


class AcuteToxicityInhalation(models.Model):
    """
    Acute Toxicity: inhalation information
    """
    ingredient = models.OneToOneField(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='acute_toxicity_inhalation',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    reference_type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Reference Type")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Title")
    author = models.CharField(max_length=255, blank=True, null=True, verbose_name="Author")
    year = models.CharField(max_length=50, blank=True, null=True, verbose_name="Year")
    bibliographic_source = models.TextField(blank=True, null=True, verbose_name="Bibliographic Source")
    dose_descriptor = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dose Descriptor")
    effect_level = models.CharField(max_length=255, blank=True, null=True, verbose_name="Effect Level")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Acute Toxicity: Inhalation"
        verbose_name_plural = "Acute Toxicity: Inhalation"

    def __str__(self):
        return f"Acute Toxicity: Inhalation for {self.ingredient}"


class AcuteToxicityDermal(models.Model):
    """
    Acute Toxicity: dermal information
    """
    ingredient = models.OneToOneField(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='acute_toxicity_dermal',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    reference_type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Reference Type")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Title")
    author = models.CharField(max_length=255, blank=True, null=True, verbose_name="Author")
    year = models.CharField(max_length=50, blank=True, null=True, verbose_name="Year")
    bibliographic_source = models.TextField(blank=True, null=True, verbose_name="Bibliographic Source")
    dose_descriptor = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dose Descriptor")
    effect_level = models.CharField(max_length=255, blank=True, null=True, verbose_name="Effect Level")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Acute Toxicity: Dermal"
        verbose_name_plural = "Acute Toxicity: Dermal"

    def __str__(self):
        return f"Acute Toxicity: Dermal for {self.ingredient}"


class IrritationCorrosionEndpointSummary(models.Model):
    """
    Irritation / corrosion - Endpoint summary
    """
    ingredient = models.OneToOneField(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='irritation_corrosion_endpoint',
        verbose_name="Ingredient"
    )
    endpoint_conclusion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Endpoint Conclusion")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    justification = models.TextField(blank=True, null=True, verbose_name="Justification for Classification or Non-classification")

    class Meta:
        verbose_name = "Irritation / Corrosion Endpoint Summary"
        verbose_name_plural = "Irritation / Corrosion Endpoint Summaries"

    def __str__(self):
        return f"Irritation / Corrosion Endpoint Summary for {self.ingredient}"


class SkinIrritationCorrosion(models.Model):
    """
    Skin irritation / corrosion information
    """
    ingredient = models.OneToOneField(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='skin_irritation_corrosion',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Skin Irritation / Corrosion"
        verbose_name_plural = "Skin Irritation / Corrosion"

    def __str__(self):
        return f"Skin Irritation / Corrosion for {self.ingredient}"


class EyeIrritation(models.Model):
    """
    Eye irritation information
    """
    ingredient = models.OneToOneField(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='eye_irritation',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Eye Irritation"
        verbose_name_plural = "Eye Irritations"

    def __str__(self):
        return f"Eye Irritation for {self.ingredient}"


class SensitisationEndpointSummary(models.Model):
    """
    Sensitisation - Endpoint summary
    """
    ingredient = models.OneToOneField(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='sensitisation_endpoint',
        verbose_name="Ingredient"
    )
    endpoint_conclusion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Endpoint Conclusion")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    justification = models.TextField(blank=True, null=True, verbose_name="Justification for Classification or Non-classification")

    class Meta:
        verbose_name = "Sensitisation Endpoint Summary"
        verbose_name_plural = "Sensitisation Endpoint Summaries"

    def __str__(self):
        return f"Sensitisation Endpoint Summary for {self.ingredient}"


class SkinSensitisation(models.Model):
    """
    Skin sensitisation information
    """
    ingredient = models.OneToOneField(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='skin_sensitisation',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Skin Sensitisation"
        verbose_name_plural = "Skin Sensitisations"

    def __str__(self):
        return f"Skin Sensitisation for {self.ingredient}"


class RepeatedDoseToxicityEndpointSummary(models.Model):
    """
    Repeated dose toxicity - Endpoint summary
    """
    ingredient = models.OneToOneField(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='repeated_dose_toxicity_endpoint',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    endpoint_conclusion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Endpoint Conclusion")
    dose_descriptor = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dose Descriptor")
    value = models.CharField(max_length=255, blank=True, null=True, verbose_name="Value")
    study_duration = models.CharField(max_length=255, blank=True, null=True, verbose_name="Study Duration")
    species = models.CharField(max_length=255, blank=True, null=True, verbose_name="Species")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    justification = models.TextField(blank=True, null=True, verbose_name="Justification for Classification or Non-classification")

    class Meta:
        verbose_name = "Repeated Dose Toxicity Endpoint Summary"
        verbose_name_plural = "Repeated Dose Toxicity Endpoint Summaries"

    def __str__(self):
        return f"Repeated Dose Toxicity Endpoint Summary for {self.ingredient}"


class Carcinogenicity(models.Model):
    """
    Carcinogenicity information
    """
    ingredient = models.OneToOneField(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='carcinogenicity',
        verbose_name="Ingredient"
    )
    description_of_key_information = models.TextField(blank=True, null=True, verbose_name="Description of Key Information")
    additional_information = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    interpretation_of_results = models.TextField(blank=True, null=True, verbose_name="Interpretation of Results")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    conclusions = models.TextField(blank=True, null=True, verbose_name="Conclusions")
    executive_summary = models.TextField(blank=True, null=True, verbose_name="Executive Summary")

    class Meta:
        verbose_name = "Carcinogenicity"
        verbose_name_plural = "Carcinogenicities"

    def __str__(self):
        return f"Carcinogenicity for {self.ingredient}"


# Sheet 2 Models

class AnnexAllowedByFunction(models.Model):
    """
    Annex allowed by function information
    """
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    ingredients_link = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ingredients Link")
    no_of_ingredients = models.IntegerField(blank=True, null=True, verbose_name="Number of Ingredients")

    class Meta:
        verbose_name = "Annex Allowed By Function"
        verbose_name_plural = "Annex Allowed By Functions"

    def __str__(self):
        return self.name or f"Annex Function {self.id}"


class AnnexIngredient(models.Model):
    """
    Annex ingredient information
    """
    function_type = models.ForeignKey(
        AnnexAllowedByFunction,
        on_delete=models.CASCADE,
        related_name='annex_ingredients',
        verbose_name="Function Type"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='annex_entries',
        verbose_name="Ingredient",
        blank=True,
        null=True
    )
    ingredients = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ingredients")
    cas_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="CAS Number")
    ec_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="EC Number")
    annex_ref = models.CharField(max_length=100, blank=True, null=True, verbose_name="Annex Reference")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    sccs_opinions = models.TextField(blank=True, null=True, verbose_name="SCCS Opinions")
    regulation = models.CharField(max_length=255, blank=True, null=True, verbose_name="Regulation")
    other_directives = models.TextField(blank=True, null=True, verbose_name="Other Directives")
    chemical_iupac_name = models.TextField(blank=True, null=True, verbose_name="Chemical IUPAC Name")
    indentified_ingredients = models.TextField(blank=True, null=True, verbose_name="Identified Ingredients")
    cmp = models.CharField(max_length=255, blank=True, null=True, verbose_name="CMP")
    cmr = models.CharField(max_length=255, blank=True, null=True, verbose_name="CMR")
    update_date = models.DateField(blank=True, null=True, verbose_name="Update Date")
    is_prohibited = models.BooleanField(default=False, verbose_name="Is Prohibited")
    is_restricted = models.BooleanField(default=False, verbose_name="Is Restricted")
    product_type_body_parts = models.TextField(blank=True, null=True, verbose_name="Product Type, Body Parts")
    maximum_concentration = models.CharField(max_length=255, blank=True, null=True, verbose_name="Maximum Concentration in Ready for Use Preparation")
    other = models.TextField(blank=True, null=True, verbose_name="Other")
    wording_of_conditions_use_warning = models.TextField(blank=True, null=True, verbose_name="Wording of Conditions Use Warning")
    is_coloraants_allowed = models.BooleanField(default=False, verbose_name="Is Colorants Allowed")
    colour_index_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="Colour Index Number / Name of Common Ingredients Glossary")
    color = models.CharField(max_length=100, blank=True, null=True, verbose_name="Color")
    is_preservative_allowed = models.BooleanField(default=False, verbose_name="Is Preservative Allowed")
    is_uv_filter_allowed = models.BooleanField(default=False, verbose_name="Is UV Filter Allowed")

    class Meta:
        verbose_name = "Annex Ingredient"
        verbose_name_plural = "Annex Ingredients"

    def __str__(self):
        return f"{self.ingredients or self.ingredient} - {self.function_type}"


class IUPAC(models.Model):
    """
    IUPAC information
    """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='iupac_entries',
        verbose_name="Ingredient",
        blank=True,
        null=True
    )
    ingredient_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ingredient Name")
    inn_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="INN Name")
    ph_eur_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ph. Eur. Name")
    cas_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="CAS Number")
    ec_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="EC Number")
    einecs_elincs_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="EINECS/ELINCS Number")
    chemical_iupac_name = models.TextField(blank=True, null=True, verbose_name="Chemical IUPAC Name")
    restriction = models.TextField(blank=True, null=True, verbose_name="Restriction")
    function = models.CharField(max_length=255, blank=True, null=True, verbose_name="Function")

    class Meta:
        verbose_name = "IUPAC"
        verbose_name_plural = "IUPAC Entries"

    def __str__(self):
        return self.ingredient_name or f"IUPAC Entry {self.id}"


class ECHANanomaterialAllowed(models.Model):
    """
    ECHA nanomaterial allowed information
    """
    ec_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="EC Name")
    ec_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="EC Number")
    cas_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="CAS Number")
    type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Type")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Name")
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='echa_nanomaterials',
        verbose_name="Ingredient",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "ECHA Nanomaterial Allowed"
        verbose_name_plural = "ECHA Nanomaterials Allowed"

    def __str__(self):
        return self.name or self.ec_name or f"ECHA Nanomaterial {self.id}"


class IFRAAllFRTransparencyList(models.Model):
    """
    IFRA all FR transparency list information
    """
    cas_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="CAS Number")
    name_of_fragrance_ingredients = models.CharField(max_length=255, blank=True, null=True, verbose_name="Name of Fragrance Ingredients")
    naturals_ncs_category = models.CharField(max_length=255, blank=True, null=True, verbose_name="NATURALS NCS CATEGORY")
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ifra_transparency_entries',
        verbose_name="Ingredient",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "IFRA All FR Transparency List"
        verbose_name_plural = "IFRA All FR Transparency Lists"

    def __str__(self):
        return self.name_of_fragrance_ingredients or f"IFRA Transparency Entry {self.id}"


class IFRAFragranceRPS(models.Model):
    """
    IFRA fragrance RPS information
    """
    cas_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="CAS Number")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Title")
    type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Type")
    amendments = models.TextField(blank=True, null=True, verbose_name="Amendments")
    link = models.URLField(blank=True, null=True, verbose_name="Link")
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ifra_fragrance_rps',
        verbose_name="Ingredient",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "IFRA Fragrance RPS"
        verbose_name_plural = "IFRA Fragrance RPS"

    def __str__(self):
        return self.title or f"IFRA Fragrance RPS {self.id}"


class EFSAVitaminMinerals(models.Model):
    """
    EFSA vitamin minerals information
    """
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Name")
    type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Type")
    link = models.URLField(blank=True, null=True, verbose_name="Link")
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='efsa_vitamin_minerals',
        verbose_name="Ingredient",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "EFSA Vitamin Mineral"
        verbose_name_plural = "EFSA Vitamin Minerals"

    def __str__(self):
        return self.name or f"EFSA Vitamin/Mineral {self.id}"


class COSMOSTOX(models.Model):
    """
    COSMOS TOX information
    """
    dataset = models.CharField(max_length=255, blank=True, null=True, verbose_name="DATASET")
    cosmos_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="COSMOS ID")
    cas_rn = models.CharField(max_length=100, blank=True, null=True, verbose_name="CAS RN")
    cosmos_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="COSMOS Name")
    inci_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="INCI Name")
    munro_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Munro Name")
    cramer_classes_by_cosmos = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cramer Classes by COSMOS")
    cramer_class_source = models.CharField(max_length=255, blank=True, null=True, verbose_name="CRAMER CLASS SOURCE")
    in_cosmos_inventory = models.BooleanField(default=False, verbose_name="In COSMOS Inventory?")
    purity = models.CharField(max_length=100, blank=True, null=True, verbose_name="Purity (%)")
    active = models.CharField(max_length=100, blank=True, null=True, verbose_name="Active (%)")
    test_substance_comments = models.TextField(blank=True, null=True, verbose_name="Test Substance Comments")
    study_type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Study Type")
    species = models.CharField(max_length=255, blank=True, null=True, verbose_name="Species")
    route_of_exposure = models.CharField(max_length=255, blank=True, null=True, verbose_name="Route of Exposure")
    duration_with_unit = models.CharField(max_length=255, blank=True, null=True, verbose_name="Duration with Unit")
    doses_with_unit = models.CharField(max_length=255, blank=True, null=True, verbose_name="Doses with Unit")
    dose_comments = models.TextField(blank=True, null=True, verbose_name="Dose Comments")
    original_noael = models.CharField(max_length=255, blank=True, null=True, verbose_name="Original NOAEL (mg/kg-bw/day)")
    original_loael = models.CharField(max_length=255, blank=True, null=True, verbose_name="Original LOAEL (mg/kg-bw/day)")
    noael_loael_owner = models.CharField(max_length=255, blank=True, null=True, verbose_name="NOAEL/LOAEL Owner")
    adjustment_factor_dose_duration = models.CharField(max_length=255, blank=True, null=True, verbose_name="Adjustment Factor: Dose Duration")
    adjustment_factor_loel_noel_extrapolation = models.CharField(max_length=255, blank=True, null=True, verbose_name="Adjustment Factor: LOEL-NOEL Extrapolation")
    calculated_pod = models.CharField(max_length=255, blank=True, null=True, verbose_name="Calculated POD (NOAEL/LOAEL) for COSMOS TTC")
    pod_base_source = models.CharField(max_length=255, blank=True, null=True, verbose_name="POD BASE SOURCE")
    target_sites = models.TextField(blank=True, null=True, verbose_name="Target Sites")
    critical_effects = models.TextField(blank=True, null=True, verbose_name="Critical Effects")
    critical_effects_details = models.TextField(blank=True, null=True, verbose_name="Critical Effects")
    critical_effects_details = models.TextField(blank=True, null=True, verbose_name="Critical Effects Details")
    noael_reliability_method = models.CharField(max_length=255, blank=True, null=True, verbose_name="NOAEL Reliability Method")
    noael_reliability_value = models.CharField(max_length=255, blank=True, null=True, verbose_name="NOAEL Reliability Value")
    study_reliability = models.CharField(max_length=255, blank=True, null=True, verbose_name="Study Reliability")
    guideline_glp = models.CharField(max_length=255, blank=True, null=True, verbose_name="Guideline / GLP")
    qc_status = models.CharField(max_length=255, blank=True, null=True, verbose_name="QC Status")
    qc_rationale = models.TextField(blank=True, null=True, verbose_name="QC Rationale")
    document_source = models.CharField(max_length=255, blank=True, null=True, verbose_name="Document Source")
    document_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="Document Number")
    database_source = models.CharField(max_length=255, blank=True, null=True, verbose_name="Database Source")
    original_study_citation = models.TextField(blank=True, null=True, verbose_name="Original Study Citation")
    study_title = models.TextField(blank=True, null=True, verbose_name="Study Title")
    primary_reference_type = models.CharField(max_length=255, blank=True, null=True, verbose_name="PRIMARY REFERENCE TYPE")
    database_report_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="DATABASE REPORT NUMBER")
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='cosmos_tox_entries',
        verbose_name="Ingredient",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "COSMOS TOX"
        verbose_name_plural = "COSMOS TOX Entries"

    def __str__(self):
        return self.cosmos_name or self.inci_name or f"COSMOS TOX Entry {self.id}"


class CIRReportNOAELDAP(models.Model):
    """
    CIR report NOAEL DAP information
    """
    ingredient_name_used = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ingredient Name Used")
    inci_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="INCI Name")
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='cir_report_entries',
        verbose_name="Ingredient",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "CIR Report NOAEL DAP"
        verbose_name_plural = "CIR Report NOAEL DAP Entries"

    def __str__(self):
        return self.ingredient_name_used or self.inci_name or f"CIR Report Entry {self.id}"


class EFSA_JECFAFoodNoNOEAL(models.Model):
    """
    EFSA JECFA FOOD No NOEAL information
    """
    type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Type")
    cas_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="CAS No.")
    ec_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="EC No.")
    food_additive_group = models.CharField(max_length=255, blank=True, null=True, verbose_name="Food Additive Group")
    efsa_ingredient_name = models.TextField(blank=True, null=True, verbose_name="EFSA Ingredient Name")
    synonym_names = models.TextField(blank=True, null=True, verbose_name="Synonym Name(s) (From EFSA Datasheet)")
    conditions_of_use = models.TextField(blank=True, null=True, verbose_name="Conditions of use (From EFSA Datasheet)")
    legislations = models.TextField(blank=True, null=True, verbose_name="Legislations (From EFSA datasheet, specifically for GROUPS)")
    fl_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="FL No.")
    coe_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="CoE No.")
    un_fao = models.CharField(max_length=255, blank=True, null=True, verbose_name="UN-FAO")
    jecfa_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="JECFA No")
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='efsa_jecfa_entries',
        verbose_name="Ingredient",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "EFSA JECFA FOOD No NOEAL"
        verbose_name_plural = "EFSA JECFA FOOD No NOEAL Entries"

    def __str__(self):
        return self.efsa_ingredient_name or f"EFSA JECFA Entry {self.id}"


class TOXRICLD50(models.Model):
    """
    TOXRIC LD50 information
    """
    taid = models.CharField(max_length=100, blank=True, null=True, verbose_name="TAID")
    name = models.TextField(blank=True, null=True, verbose_name="Name")
    iupac_name = models.TextField(blank=True, null=True, verbose_name="IUPAC Name")
    pubchem_cid = models.CharField(max_length=100, blank=True, null=True, verbose_name="PubChem CID")
    canonical_smiles = models.TextField(blank=True, null=True, verbose_name="Canonical SMILES")
    inchikey = models.CharField(max_length=255, blank=True, null=True, verbose_name="InChIKey")
    toxicity_value = models.CharField(max_length=255, blank=True, null=True, verbose_name="Toxicity Value")
    ld50_toxicity_category = models.CharField(max_length=255, blank=True, null=True, verbose_name="LD50 Toxicity Category")
    is_toxicity = models.BooleanField(default=False, verbose_name="Is Toxicity", null=True)
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='toxric_ld50_entries',
        verbose_name="Ingredient",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "TOXRIC LD50"
        verbose_name_plural = "TOXRIC LD50 Entries"

    def __str__(self):
        return self.name or f"TOXRIC LD50 Entry {self.id}"


class ALLRegisteredDossiers(models.Model):
    """
    ALL registered dossiers information
    """
    ec_list_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="EC / List Number")
    cas_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="CAS Number")
    echa_chem_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="ECHA CHEM ID")
    registration_status = models.CharField(max_length=255, blank=True, null=True, verbose_name="Registration Status")
    registration_type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Registration Type")
    submission_type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Submission Type")
    total_tonnage_band = models.CharField(max_length=255, blank=True, null=True, verbose_name="Total Tonnage Band")
    tonnage_band_min = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tonnage Band Min")
    tonnage_band_max = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tonnage Band Max")
    last_updated = models.DateField(blank=True, null=True, verbose_name="Last Updated")
    factsheet_url = models.URLField(blank=True, null=True, verbose_name="Factsheet URL COMPLEX COMPONENTS + PHYS/CHEM PROPS + TOX")
    substance_information_page = models.URLField(blank=True, null=True, verbose_name="Substance Information Page")
    echa_chem_dossier = models.URLField(blank=True, null=True, verbose_name="ECHA CHEM DOSSIER")
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='registered_dossiers',
        verbose_name="Ingredient",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "ALL Registered Dossier"
        verbose_name_plural = "ALL Registered Dossiers"

    def __str__(self):
        return f"Dossier {self.echa_chem_id or self.ec_list_number or self.id}"


class SCCSOpinions(models.Model):
    """
    SCCS opinions information
    """
    sccs_opinion_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="SCCS Opinion Name")
    ingredient_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ingredient Name")
    type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Type")
    cas_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="CAS No.")
    ec_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="EC No.")
    sccs_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="SCCS Number")
    adopted_on = models.CharField(blank=True, null=True, verbose_name="Adopted on")
    link = models.URLField(blank=True, null=True, verbose_name="Link")
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='sccs_opinions',
        verbose_name="Ingredient",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "SCCS Opinion"
        verbose_name_plural = "SCCS Opinions"

    def __str__(self):
        return self.sccs_opinion_name or self.ingredient_name or f"SCCS Opinion {self.id}"


class ECHACLPHazard(models.Model):
    """
    ECHA CLP hazard information
    """
    index_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Index No")
    international_chemical_identification = models.TextField(blank=True, null=True, verbose_name="International Chemical Identification")
    ec_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="EC No")
    cas_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="CAS No")
    classification_hazard_class_category_codes = models.TextField(blank=True, null=True, verbose_name="Classification Hazard Class and Category Code(s)")
    classification_hazard_statement_codes = models.TextField(blank=True, null=True, verbose_name="Classification Hazard Statement Code(s)")
    labelling_pictogram_signal_word_codes = models.TextField(blank=True, null=True, verbose_name="Labelling Pictogram, Signal Word Code(s)")
    labelling_hazard_statement_codes = models.TextField(blank=True, null=True, verbose_name="Labelling Hazard Statement Code(s)")
    labelling_suppliment_hazard_statement_codes = models.TextField(blank=True, null=True, verbose_name="Labelling Suppliment Hazard Statement Code(s)")
    specific_conc_limits_m_factors = models.TextField(blank=True, null=True, verbose_name="Specific Conc. Limits, M-factors")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    atp_inserted_updated = models.CharField(max_length=255, blank=True, null=True, verbose_name="ATP inserted/ATP Updated")
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='echa_clp_hazards',
        verbose_name="Ingredient",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "ECHA CLP Hazard"
        verbose_name_plural = "ECHA CLP Hazards"

    def __str__(self):
        return self.international_chemical_identification or f"ECHA CLP Hazard {self.id}"
