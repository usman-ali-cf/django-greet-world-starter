from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Ingredient

def ingredient_list(request):
    """View to display a list of all ingredients"""
    ingredients = Ingredient.objects.all().order_by('name')
    return render(request, 'ingredients/ingredient_list.html', {
        'ingredients': ingredients
    })

def ingredient_detail(request, ingredient_id):
    """View to display detailed information about a specific ingredient"""
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    return render(request, 'ingredients/ingredient_detail.html', {
        'ingredient': ingredient
    })

def search_ingredients(request):
    """API view to search for ingredients by name, EC number, or CAS number"""
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'results': []})
    
    ingredients = Ingredient.objects.filter(
        models.Q(name__icontains=query) | 
        models.Q(display_name__icontains=query) | 
        models.Q(ec_number__icontains=query) | 
        models.Q(cas_number__icontains=query)
    )[:20]  # Limit to 20 results
    
    results = []
    for ingredient in ingredients:
        display_name = ingredient.display_name or ingredient.name or f"Ingredient {ingredient.id}"
        results.append({
            'id': ingredient.id,
            'name': ingredient.name,
            'display_name': display_name,
            'ec_number': ingredient.ec_number,
            'cas_number': ingredient.cas_number
        })
    
    return JsonResponse({'results': results})
