from django.contrib import admin
from .models import (
    Ingredient, GeneralInformation, AppearancePhysicalState, MeltingPoint, BoilingPoint,
    Density, ParticleSize, VapourPressure, PartitionCoefficient, WaterSolubility,
    OrganicSolventSolubility, SurfaceTension, FlashPoint, AutoFlammability, Flammability,
    Explosiveness, OxidisingProperties, PH, DissociationConstant, Viscosity,
    ToxicokineticsEndpointSummary, BasicToxicokinetics, DermalAbsorption,
    AcuteToxicityEndpointSummary, AcuteToxicityOral, AcuteToxicityInhalation,
    AcuteToxicityDermal, IrritationCorrosionEndpointSummary, SkinIrritationCorrosion,
    EyeIrritation, SensitisationEndpointSummary, SkinSensitisation,
    RepeatedDoseToxicityEndpointSummary, Carcinogenicity,
    # New models
    AnnexAllowedByFunction, AnnexIngredient, IUPAC, ECHANanomaterialAllowed,
    IFRAAllFRTransparencyList, IFRAFragranceRPS, EFSAVitaminMinerals, COSMOSTOX,
    CIRReportNOAELDAP, EFSA_JECFAFoodNoNOEAL, TOXRICLD50, ALLRegisteredDossiers,
    SCCSOpinions, ECHACLPHazard
)


class GeneralInformationInline(admin.StackedInline):
    model = GeneralInformation
    can_delete = False
    verbose_name_plural = 'General Information'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'ec_number', 'cas_number')
    search_fields = ('name', 'display_name', 'ec_number', 'cas_number')
    inlines = [GeneralInformationInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'display_name', 'ec_number', 'cas_number')
        }),
    )


@admin.register(GeneralInformation)
class GeneralInformationAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'ec_name', 'molecular_formula', 'iupac_name')
    search_fields = ('ingredient__name', 'ec_name', 'molecular_formula', 'iupac_name')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(AppearancePhysicalState)
class AppearancePhysicalStateAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'physical_state_at_20c', 'form', 'colour', 'odour')
    search_fields = ('ingredient__name', 'physical_state_at_20c', 'form', 'colour', 'odour')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(MeltingPoint)
class MeltingPointAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'melting_freezing_point', 'melting_freezing_pt', 'atm_press')
    search_fields = ('ingredient__name', 'melting_freezing_point', 'melting_freezing_pt')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(BoilingPoint)
class BoilingPointAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'boiling_point', 'boiling_pt', 'atm_press')
    search_fields = ('ingredient__name', 'boiling_point', 'boiling_pt')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(Density)
class DensityAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'relative_density_at_20c', 'density', 'temp')
    search_fields = ('ingredient__name', 'relative_density_at_20c', 'density')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(ParticleSize)
class ParticleSizeAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'percentile', 'mean')
    search_fields = ('ingredient__name', 'percentile', 'mean')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(VapourPressure)
class VapourPressureAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'vapour_pressure', 'temp')
    search_fields = ('ingredient__name', 'vapour_pressure')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(PartitionCoefficient)
class PartitionCoefficientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'log_kow', 'partition_coefficient', 'at_temperature')
    search_fields = ('ingredient__name', 'log_kow', 'partition_coefficient')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(WaterSolubility)
class WaterSolubilityAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'water_solubility', 'at_temperature', 'temp')
    search_fields = ('ingredient__name', 'water_solubility')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(OrganicSolventSolubility)
class OrganicSolventSolubilityAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'description_of_key_information')
    search_fields = ('ingredient__name', 'description_of_key_information')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(SurfaceTension)
class SurfaceTensionAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'surface_tension', 'temp', 'conc')
    search_fields = ('ingredient__name', 'surface_tension')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(FlashPoint)
class FlashPointAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'flash_point_at_101325_pa', 'flash_point', 'atm_press')
    search_fields = ('ingredient__name', 'flash_point_at_101325_pa', 'flash_point')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(AutoFlammability)
class AutoFlammabilityAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'autoflammability_temperature', 'auto_ignition_temperature')
    search_fields = ('ingredient__name', 'autoflammability_temperature', 'auto_ignition_temperature')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(Flammability)
class FlammabilityAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'flammability', 'parameter', 'value')
    search_fields = ('ingredient__name', 'flammability', 'parameter', 'value')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(Explosiveness)
class ExplosivenessAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'explosiveness')
    search_fields = ('ingredient__name', 'explosiveness')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(OxidisingProperties)
class OxidisingPropertiesAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'oxidising_properties', 'sample_tested', 'parameter')
    search_fields = ('ingredient__name', 'oxidising_properties', 'sample_tested')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(PH)
class PHAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'description_of_key_information')
    search_fields = ('ingredient__name', 'description_of_key_information')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(DissociationConstant)
class DissociationConstantAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'description_of_key_information')
    search_fields = ('ingredient__name', 'description_of_key_information')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(Viscosity)
class ViscosityAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'viscosity', 'at_temperature', 'temp', 'parameter', 'value')
    search_fields = ('ingredient__name', 'viscosity', 'parameter', 'value')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(ToxicokineticsEndpointSummary)
class ToxicokineticsEndpointSummaryAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'absorption_rate_oral', 'absorption_rate_dermal', 'absorption_rate_inhalation')
    search_fields = ('ingredient__name', 'absorption_rate_oral', 'absorption_rate_dermal', 'absorption_rate_inhalation')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(BasicToxicokinetics)
class BasicToxicokineticsAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'description_of_key_information')
    search_fields = ('ingredient__name', 'description_of_key_information')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(DermalAbsorption)
class DermalAbsorptionAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'reference_type', 'title', 'author', 'year')
    search_fields = ('ingredient__name', 'reference_type', 'title', 'author', 'year')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(AcuteToxicityEndpointSummary)
class AcuteToxicityEndpointSummaryAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'endpoint_conclusion', 'dose_descriptor', 'value')
    search_fields = ('ingredient__name', 'endpoint_conclusion', 'dose_descriptor', 'value')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(AcuteToxicityOral)
class AcuteToxicityOralAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'reference_type', 'title', 'author', 'year', 'dose_descriptor', 'effect_level')
    search_fields = ('ingredient__name', 'reference_type', 'title', 'author', 'dose_descriptor', 'effect_level')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(AcuteToxicityInhalation)
class AcuteToxicityInhalationAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'reference_type', 'title', 'author', 'year', 'dose_descriptor', 'effect_level')
    search_fields = ('ingredient__name', 'reference_type', 'title', 'author', 'dose_descriptor', 'effect_level')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(AcuteToxicityDermal)
class AcuteToxicityDermalAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'reference_type', 'title', 'author', 'year', 'dose_descriptor', 'effect_level')
    search_fields = ('ingredient__name', 'reference_type', 'title', 'author', 'dose_descriptor', 'effect_level')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(IrritationCorrosionEndpointSummary)
class IrritationCorrosionEndpointSummaryAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'endpoint_conclusion')
    search_fields = ('ingredient__name', 'endpoint_conclusion')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(SkinIrritationCorrosion)
class SkinIrritationCorrosionAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'description_of_key_information')
    search_fields = ('ingredient__name', 'description_of_key_information')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(EyeIrritation)
class EyeIrritationAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'description_of_key_information')
    search_fields = ('ingredient__name', 'description_of_key_information')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(SensitisationEndpointSummary)
class SensitisationEndpointSummaryAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'endpoint_conclusion')
    search_fields = ('ingredient__name', 'endpoint_conclusion')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(SkinSensitisation)
class SkinSensitisationAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'description_of_key_information')
    search_fields = ('ingredient__name', 'description_of_key_information')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(RepeatedDoseToxicityEndpointSummary)
class RepeatedDoseToxicityEndpointSummaryAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'endpoint_conclusion', 'dose_descriptor', 'value', 'study_duration', 'species')
    search_fields = ('ingredient__name', 'endpoint_conclusion', 'dose_descriptor', 'value', 'species')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(Carcinogenicity)
class CarcinogenicityAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'description_of_key_information')
    search_fields = ('ingredient__name', 'description_of_key_information')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


# Admin classes for new models

@admin.register(AnnexAllowedByFunction)
class AnnexAllowedByFunctionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'no_of_ingredients')
    search_fields = ('name', 'description')


class AnnexIngredientInline(admin.TabularInline):
    model = AnnexIngredient
    extra = 1
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(AnnexIngredient)
class AnnexIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredients', 'function_type', 'cas_no', 'ec_no', 'annex_ref', 'is_prohibited', 'is_restricted')
    search_fields = ('ingredients', 'cas_no', 'ec_no', 'annex_ref', 'chemical_iupac_name')
    list_filter = ('function_type', 'is_prohibited', 'is_restricted', 'is_coloraants_allowed', 'is_preservative_allowed', 'is_uv_filter_allowed')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']
    fieldsets = (
        (None, {
            'fields': ('function_type', 'ingredient', 'ingredients', 'cas_no', 'ec_no', 'annex_ref', 'description')
        }),
        ('Regulatory Information', {
            'fields': ('sccs_opinions', 'regulation', 'other_directives', 'chemical_iupac_name', 'indentified_ingredients')
        }),
        ('Classification', {
            'fields': ('cmp', 'cmr', 'update_date', 'is_prohibited', 'is_restricted')
        }),
        ('Usage Information', {
            'fields': ('product_type_body_parts', 'maximum_concentration', 'other', 'wording_of_conditions_use_warning')
        }),
        ('Special Categories', {
            'fields': ('is_coloraants_allowed', 'colour_index_number', 'color', 'is_preservative_allowed', 'is_uv_filter_allowed')
        }),
    )


@admin.register(IUPAC)
class IUPACAdmin(admin.ModelAdmin):
    list_display = ('ingredient_name', 'inn_name', 'cas_number', 'ec_number', 'function')
    search_fields = ('ingredient_name', 'inn_name', 'cas_number', 'ec_number', 'chemical_iupac_name')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(ECHANanomaterialAllowed)
class ECHANanomaterialAllowedAdmin(admin.ModelAdmin):
    list_display = ('name', 'ec_name', 'ec_number', 'cas_number', 'type')
    search_fields = ('name', 'ec_name', 'ec_number', 'cas_number')
    list_filter = ('type',)
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(IFRAAllFRTransparencyList)
class IFRAAllFRTransparencyListAdmin(admin.ModelAdmin):
    list_display = ('name_of_fragrance_ingredients', 'cas_number', 'naturals_ncs_category')
    search_fields = ('name_of_fragrance_ingredients', 'cas_number')
    list_filter = ('naturals_ncs_category',)
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(IFRAFragranceRPS)
class IFRAFragranceRPSAdmin(admin.ModelAdmin):
    list_display = ('title', 'cas_number', 'type')
    search_fields = ('title', 'cas_number')
    list_filter = ('type',)
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(EFSAVitaminMinerals)
class EFSAVitaminMineralsAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'link')
    search_fields = ('name', 'type')
    list_filter = ('type',)
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(COSMOSTOX)
class COSMOSTOXAdmin(admin.ModelAdmin):
    list_display = ('cosmos_name', 'inci_name', 'cas_rn', 'cosmos_id', 'cramer_classes_by_cosmos')
    search_fields = ('cosmos_name', 'inci_name', 'cas_rn', 'cosmos_id')
    list_filter = ('cramer_classes_by_cosmos', 'in_cosmos_inventory', 'study_type', 'species', 'route_of_exposure')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']
    fieldsets = (
        (None, {
            'fields': ('ingredient', 'dataset', 'cosmos_id', 'cas_rn', 'cosmos_name', 'inci_name', 'munro_name')
        }),
        ('Classification', {
            'fields': ('cramer_classes_by_cosmos', 'cramer_class_source', 'in_cosmos_inventory')
        }),
        ('Test Substance', {
            'fields': ('purity', 'active', 'test_substance_comments')
        }),
        ('Study Details', {
            'fields': ('study_type', 'species', 'route_of_exposure', 'duration_with_unit', 'doses_with_unit', 'dose_comments')
        }),
        ('Results', {
            'fields': ('original_noael', 'original_loael', 'noael_loael_owner', 'adjustment_factor_dose_duration',
                      'adjustment_factor_loel_noel_extrapolation', 'calculated_pod', 'pod_base_source')
        }),
        ('Effects', {
            'fields': ('target_sites', 'critical_effects', 'critical_effects_details')
        }),
        ('Quality Control', {
            'fields': ('noael_reliability_method', 'noael_reliability_value', 'study_reliability',
                      'guideline_glp', 'qc_status', 'qc_rationale')
        }),
        ('References', {
            'fields': ('document_source', 'document_number', 'database_source', 'original_study_citation',
                      'study_title', 'primary_reference_type', 'database_report_number')
        }),
    )


@admin.register(CIRReportNOAELDAP)
class CIRReportNOAELDAPAdmin(admin.ModelAdmin):
    list_display = ('ingredient_name_used', 'inci_name')
    search_fields = ('ingredient_name_used', 'inci_name')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(EFSA_JECFAFoodNoNOEAL)
class EFSAJECFAFOODNoNOEALAdmin(admin.ModelAdmin):
    list_display = ('efsa_ingredient_name', 'type', 'cas_no', 'ec_no', 'food_additive_group')
    search_fields = ('efsa_ingredient_name', 'cas_no', 'ec_no', 'synonym_names')
    list_filter = ('type', 'food_additive_group')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(TOXRICLD50)
class TOXRICLD50Admin(admin.ModelAdmin):
    list_display = ('name', 'taid', 'pubchem_cid', 'toxicity_value', 'ld50_toxicity_category', 'is_toxicity')
    search_fields = ('name', 'taid', 'pubchem_cid', 'iupac_name')
    list_filter = ('ld50_toxicity_category', 'is_toxicity')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(ALLRegisteredDossiers)
class ALLRegisteredDossiersAdmin(admin.ModelAdmin):
    list_display = ('ec_list_number', 'cas_number', 'echa_chem_id', 'registration_status', 'registration_type')
    search_fields = ('ec_list_number', 'cas_number', 'echa_chem_id')
    list_filter = ('registration_status', 'registration_type', 'submission_type', 'total_tonnage_band')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(SCCSOpinions)
class SCCSOpinionsAdmin(admin.ModelAdmin):
    list_display = ('sccs_opinion_name', 'ingredient', 'ingredient_name', 'type', 'cas_no', 'ec_no', 'sccs_number', 'adopted_on')
    search_fields = ('sccs_opinion_name', 'ingredient_name', 'cas_no', 'ec_no', 'sccs_number')
    list_filter = ('type', 'adopted_on')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']


@admin.register(ECHACLPHazard)
class ECHACLPHazardAdmin(admin.ModelAdmin):
    list_display = ('international_chemical_identification', 'index_no', 'ec_no', 'cas_no')
    search_fields = ('international_chemical_identification', 'index_no', 'ec_no', 'cas_no')
    raw_id_fields = ('ingredient',)
    autocomplete_fields = ['ingredient']
    fieldsets = (
        (None, {
            'fields': ('ingredient', 'index_no', 'international_chemical_identification', 'ec_no', 'cas_no')
        }),
        ('Classification', {
            'fields': ('classification_hazard_class_category_codes', 'classification_hazard_statement_codes')
        }),
        ('Labelling', {
            'fields': ('labelling_pictogram_signal_word_codes', 'labelling_hazard_statement_codes',
                      'labelling_suppliment_hazard_statement_codes')
        }),
        ('Additional Information', {
            'fields': ('specific_conc_limits_m_factors', 'notes', 'atp_inserted_updated')
        }),
    )
