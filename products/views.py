from django.shortcuts import render
from django.http import JsonResponse
from .models import (
    ProductSubCategory,
    ProductType,
    Product,
    FrameFormulation,
    IngredientType,
    AgeCategory
)
from .forms import ProductSelectionForm
import json


def product_selection_form(request):
    """View to display the product selection form"""
    form = ProductSelectionForm()

    if request.method == 'POST':
        form = ProductSelectionForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            age_category = form.cleaned_data['age_category']

            # Get the product's subcategory
            product_type = product.sccs_primary_prod_type
            category = product_type.sccs_prod_cat

            # Find related subcategories for this category
            subcategories = ProductSubCategory.objects.filter(sccs_product_category=category)

            # Find frame formulations for these subcategories
            formulations = FrameFormulation.objects.filter(sccs_product_sub_cat__in=subcategories)

            # Get ingredients for these formulations
            ingredients_by_formulation = {}
            for formulation in formulations:
                ingredients = IngredientType.objects.filter(frame_formulation=formulation)
                ingredients_by_formulation[formulation] = ingredients

            # If age category is selected, filter further
            age_specific_info = None
            if age_category:
                # Check if this product is allowed for this age category
                allowed_for_age = product.allowed_age_types.filter(age_category=age_category).exists()
                age_specific_info = {
                    'category': age_category,
                    'allowed': allowed_for_age,
                    'body_weight': age_category.body_weight,
                    'surface_area': age_category.surface_area
                }

            return render(request, 'products/results.html', {
                'product': product,
                'product_type': product_type,
                'category': category,
                'formulations': formulations,
                'ingredients_by_formulation': ingredients_by_formulation,
                'age_specific_info': age_specific_info,
            })

    return render(request, 'products/form.html', {'form': form})


def get_subcategories(request):
    """AJAX view to get subcategories based on selected category"""
    category_id = request.GET.get('category_id')
    subcategories = ProductSubCategory.objects.filter(
        sccs_product_category_id=category_id
    ).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)


def get_product_types(request):
    """AJAX view to get product types based on selected category"""
    category_id = request.GET.get('category_id')
    product_types = ProductType.objects.filter(
        sccs_prod_cat_id=category_id
    ).values('id', 'name')
    return JsonResponse(list(product_types), safe=False)


def get_products(request):
    """AJAX view to get products based on selected product type"""
    product_type_id = request.GET.get('product_type_id')
    products = Product.objects.filter(
        sccs_primary_prod_type_id=product_type_id
    ).values('id', 'unique_id', 'product_name')

    # Format the display text to include product name if available
    formatted_products = []
    for product in products:
        display_text = product['unique_id']
        if product['product_name']:
            display_text += f" - {product['product_name']}"

        formatted_products.append({
            'id': product['id'],
            'unique_id': product['unique_id'],
            'display_text': display_text
        })

    return JsonResponse(formatted_products, safe=False)


def get_formulations(request):
    """AJAX view to get formulations and ingredients for a selected product"""
    product_id = request.GET.get('product_id')
    age_category_id = request.GET.get('age_category_id')

    try:
        product = Product.objects.get(id=product_id)
        product_type = product.sccs_primary_prod_type
        category = product_type.sccs_prod_cat

        # Find related subcategories for this category
        subcategories = ProductSubCategory.objects.filter(sccs_product_category=category)

        # Find frame formulations for these subcategories
        formulations = FrameFormulation.objects.filter(sccs_product_sub_cat__in=subcategories)

        # Prepare response data
        response_data = {
            'product': {
                'id': product.id,
                'unique_id': product.unique_id,
                'product_name': product.product_name or 'N/A',
                'primary_exposure_route': product.primary_exposure_route,
                'foreseeable_exposure_route': product.foreseeable_exposure_route,
                'leave_on_or_rinse_off_status': product.get_leave_on_or_rinse_off_status_display(),
            },
            'product_type': {
                'name': product_type.name,
                'code': product_type.code,
                'estimated_daily_amount_applied_qx': product_type.estimated_daily_amount_applied_qx or 'N/A',
                'relative_daily_amount_applied_qx': str(
                    product_type.relative_daily_amount_applied_qx) if product_type.relative_daily_amount_applied_qx is not None else 'N/A',
                'retention_factor_fret': str(
                    product_type.retention_factor_fret) if product_type.retention_factor_fret is not None else 'N/A',
                'calculated_daily_exposure_product': str(
                    product_type.calculated_daily_exposure_product) if product_type.calculated_daily_exposure_product is not None else 'N/A',
                'calculated_relative_daily_exposure_product': str(
                    product_type.calculated_relative_daily_exposure_product) if product_type.calculated_relative_daily_exposure_product is not None else 'N/A',
                'frequency_of_application': product_type.frequency_of_application or 'N/A',
                'surface_area_for_application': str(
                    product_type.surface_area_for_application) if product_type.surface_area_for_application is not None else 'N/A',
            },
            'category': {
                'name': category.name,
                'code': category.code,
            },
            'formulations': []
        }

        # Add age category info if provided
        if age_category_id:
            try:
                age_category = AgeCategory.objects.get(id=age_category_id)
                allowed_for_age = product.allowed_age_types.filter(age_category=age_category).exists()
                response_data['age_category'] = {
                    'category': age_category.category,
                    'body_weight': str(age_category.body_weight),
                    'surface_area': str(age_category.surface_area),
                    'allowed': allowed_for_age,
                }
            except AgeCategory.DoesNotExist:
                pass

        # Add formulations and ingredients
        for formulation in formulations:
            formulation_data = {
                'id': formulation.id,
                'name': formulation.name,
                'formulation_num': formulation.formulation_num,
                'link': formulation.link,
                'subcategory': formulation.sccs_product_sub_cat.name,
                'ingredients': []
            }

            # Get ingredients for this formulation
            ingredients = IngredientType.objects.filter(frame_formulation=formulation)
            for ingredient in ingredients:
                ingredient_data = {
                    'type': ingredient.type,
                    'example': ingredient.example or 'N/A',
                    'concentration': ingredient.concentration or 'N/A',
                }
                formulation_data['ingredients'].append(ingredient_data)

            response_data['formulations'].append(formulation_data)

        return JsonResponse(response_data)

    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
