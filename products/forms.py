from django import forms
from .models import (
    ProductCategory, 
    ProductSubCategory, 
    ProductType, 
    Product, 
    AgeCategory
)

class ProductSelectionForm(forms.Form):
    product_category = forms.ModelChoiceField(
        queryset=ProductCategory.objects.all(),
        label="Product Category",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_product_category'})
    )
    
    product_subcategory = forms.ModelChoiceField(
        queryset=ProductSubCategory.objects.none(),
        label="Product Sub-Category",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_product_subcategory'})
    )
    
    product_type = forms.ModelChoiceField(
        queryset=ProductType.objects.none(),
        label="Product Type",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_product_type'})
    )
    
    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),
        label="Product",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_product'})
    )
    
    age_category = forms.ModelChoiceField(
        queryset=AgeCategory.objects.all(),
        label="Age Category (Optional)",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_age_category'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If form is bound and has initial data for product_category
        if 'product_category' in self.data:
            try:
                category_id = int(self.data.get('product_category'))
                self.fields['product_subcategory'].queryset = ProductSubCategory.objects.filter(
                    sccs_product_category_id=category_id
                ).order_by('name')
            except (ValueError, TypeError):
                pass
        
        # If form is bound and has initial data for product_subcategory
        if 'product_subcategory' in self.data:
            try:
                subcategory_id = int(self.data.get('product_subcategory'))
                # Get product types related to the selected category
                category_id = int(self.data.get('product_category'))
                self.fields['product_type'].queryset = ProductType.objects.filter(
                    sccs_prod_cat_id=category_id
                ).order_by('name')
            except (ValueError, TypeError):
                pass
        
        # If form is bound and has initial data for product_type
        if 'product_type' in self.data:
            try:
                product_type_id = int(self.data.get('product_type'))
                self.fields['product'].queryset = Product.objects.filter(
                    sccs_primary_prod_type_id=product_type_id
                ).order_by('unique_id')
            except (ValueError, TypeError):
                pass

