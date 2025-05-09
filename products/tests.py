from django.test import TestCase
from django.urls import reverse
from .models import (
    ProductCategory, 
    ProductSubCategory, 
    ProductType, 
    Product, 
    AgeCategory, 
    IFRACategory,
    FrameFormulation,
    IngredientType
)

class ProductFormTests(TestCase):
    def setUp(self):
        # Create test data
        self.category = ProductCategory.objects.create(
            unique_id="CAT001",
            code="C001",
            name="Test Category",
            category_num="1"
        )
        
        self.subcategory = ProductSubCategory.objects.create(
            unique_id="SUBCAT001",
            code="SC001",
            name="Test Subcategory",
            sub_category_num="1.1",
            sccs_product_category=self.category
        )
        
        self.product_type = ProductType.objects.create(
            unique_id="PT001",
            code="PT001",
            name="Test Product Type",
            sccs_prod_cat=self.category,
            est_qx="estimated_daily_amount_applied_qx"
        )
        
        self.age_category = AgeCategory.objects.create(
            unique_id="AGE001",
            category="Adult",
            body_weight=70.0,
            surface_area=1.8
        )
        
        self.ifra_category = IFRACategory.objects.create(
            unique_id="IFRA001",
            description="Test IFRA Category",
            code="IFRA001",
            category="Category 1",
            type_of_prod="Skin"
        )
        
        self.product = Product.objects.create(
            unique_id="PROD001",
            sccs_primary_prod_type=self.product_type,
            age_category=self.age_category,
            primary_exposure_route="Dermal",
            foreseeable_exposure_route="Oral",
            ifra_ora_category=self.ifra_category,
            leave_on_or_rinse_off_status="LEAVE_ON"
        )
        
        self.formulation = FrameFormulation.objects.create(
            unique_id="FORM001",
            name="Test Formulation",
            link="https://example.com",
            sccs_product_sub_cat=self.subcategory,
            formulation_num="F001"
        )
        
        self.ingredient = IngredientType.objects.create(
            unique_id="ING001",
            type="Test Ingredient",
            example="Example ingredient",
            concentration="10%",
            frame_formulation=self.formulation
        )
    
    def test_form_view(self):
        """Test that the form view loads correctly"""
        response = self.client.get(reverse('product_selection_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/form.html')
    
    def test_get_subcategories_api(self):
        """Test the API endpoint for getting subcategories"""
        response = self.client.get(
            reverse('get_subcategories'), 
            {'category_id': self.category.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{'id': self.subcategory.id, 'name': 'Test Subcategory'}]
        )
    
    def test_get_product_types_api(self):
        """Test the API endpoint for getting product types"""
        response = self.client.get(
            reverse('get_product_types'), 
            {'category_id': self.category.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{'id': self.product_type.id, 'name': 'Test Product Type'}]
        )
    
    def test_get_products_api(self):
        """Test the API endpoint for getting products"""
        response = self.client.get(
            reverse('get_products'), 
            {'product_type_id': self.product_type.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{'id': self.product.id, 'unique_id': 'PROD001'}]
        )

