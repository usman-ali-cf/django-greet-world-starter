from django.db import models


class ProductCategory(models.Model):
    unique_id = models.CharField(max_length=50, unique=True, verbose_name="Unique ID")
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    category_num = models.CharField(max_length=50, verbose_name="Category Number")

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductSubCategory(models.Model):
    unique_id = models.CharField(max_length=50, unique=True, verbose_name="Unique ID")
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    sub_category_num = models.CharField(max_length=50, verbose_name="Sub-Category Number")
    sccs_product_category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name="Product Category"
    )

    class Meta:
        verbose_name = "Product Sub-Category"
        verbose_name_plural = "Product Sub-Categories"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.sccs_product_category.name})"


class ProductType(models.Model):
    unique_id = models.CharField(max_length=50, unique=True, verbose_name="Unique ID")
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    sccs_prod_cat = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='product_types',
        verbose_name="Product Category"
    )
    estimated_daily_amount_applied_qx = models.CharField(max_length=50, blank=True, null=True,
                                                         verbose_name="Estimated Daily Amount Applied")
    relative_daily_amount_applied_qx = models.FloatField(blank=True, null=True, verbose_name="Relative Amount")
    retention_factor_fret = models.FloatField(blank=True, null=True, verbose_name="Retention Factor")
    calculated_daily_exposure_product = models.FloatField(blank=True, null=True,
                                                          verbose_name="Calculated Daily Exposure Product")
    calculated_relative_daily_exposure_product = models.FloatField(blank=True, null=True,
                                                                   verbose_name="Calculated Relative Daily Exposure Product")
    frequency_of_application = models.CharField(max_length=50, blank=True, null=True,
                                                verbose_name="Frequency of Application")
    surface_area_for_application = models.FloatField(blank=True, null=True, verbose_name="Surface Area for Application")

    class Meta:
        verbose_name = "Product Type"
        verbose_name_plural = "Product Types"
        ordering = ['name']

    def __str__(self):
        return self.name


class AgeCategory(models.Model):
    unique_id = models.CharField(max_length=50, unique=True, verbose_name="Unique ID")
    category = models.CharField(max_length=100)
    body_weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Body Weight")
    surface_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")

    class Meta:
        verbose_name = "Age Category"
        verbose_name_plural = "Age Categories"
        ordering = ['category']

    def __str__(self):
        return self.category


class IFRACategory(models.Model):
    unique_id = models.CharField(max_length=50, unique=True, verbose_name="Unique ID")
    description = models.TextField()
    code = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    type_of_prod = models.CharField(max_length=100, verbose_name="Type of Product")

    class Meta:
        verbose_name = "IFRA Category"
        verbose_name_plural = "IFRA Categories"
        ordering = ['category']

    def __str__(self):
        return f"{self.category} - {self.description}"


class Product(models.Model):
    LEAVE_ON_CHOICES = [
        ('LEAVE_ON', 'Leave On'),
        ('RINSE-OFF', 'Rinse Off'),
    ]

    unique_id = models.CharField(max_length=50, unique=True, verbose_name="Unique ID")
    product_name = models.CharField(max_length=100, verbose_name="Product Name", null=True, blank=True)
    sccs_primary_prod_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name='primary_products',
        verbose_name="Primary Product Type"
    )
    age_category = models.ForeignKey(
        AgeCategory,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Age Category"
    )
    primary_exposure_route = models.CharField(max_length=100, verbose_name="Primary Exposure Route")
    foreseeable_exposure_route = models.CharField(max_length=100, verbose_name="Foreseeable Exposure Route")
    ifra_ora_category = models.ForeignKey(
        IFRACategory,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="IFRA/ORA Category"
    )
    sccs_secondary_prod_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name='secondary_products',
        verbose_name="Secondary Product Type",
        blank=True,
        null=True
    )
    leave_on_or_rinse_off_status = models.CharField(
        max_length=10,
        choices=LEAVE_ON_CHOICES,
        verbose_name="Leave On or Rinse-Off Status"
    )

    class Meta:
        verbose_name = "SCCS Product"
        verbose_name_plural = "SCCS Products"
        ordering = ['unique_id']

    def __str__(self):
        product_name_display = f" - {self.product_name}" if self.product_name else ""
        return f"Product {self.unique_id}{product_name_display} - {self.sccs_primary_prod_type.name}"


class AllowedProductTypeByAge(models.Model):
    unique_id = models.CharField(max_length=50, unique=True, verbose_name="Unique ID")
    sccs_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='allowed_age_types',
        verbose_name="SCCS Product"
    )
    age_category = models.ForeignKey(
        AgeCategory,
        on_delete=models.CASCADE,
        related_name='allowed_product_types',
        verbose_name="Age Category"
    )

    class Meta:
        verbose_name = "Allowed Product Type By Age"
        verbose_name_plural = "Allowed Product Types By Age"
        unique_together = ('sccs_product', 'age_category')

    def __str__(self):
        return f"{self.sccs_product} - {self.age_category}"


class FrameFormulation(models.Model):
    unique_id = models.CharField(max_length=50, unique=True, verbose_name="Unique ID")
    name = models.CharField(max_length=100)
    link = models.URLField(blank=True, null=True)
    sccs_product_sub_cat = models.ForeignKey(
        ProductSubCategory,
        on_delete=models.CASCADE,
        related_name='frame_formulations',
        verbose_name="Product Sub-Category"
    )
    formulation_num = models.CharField(max_length=50, verbose_name="Formulation Number")

    class Meta:
        verbose_name = "Frame Formulation"
        verbose_name_plural = "Frame Formulations"
        ordering = ['name']

    def __str__(self):
        return self.name


class IngredientType(models.Model):
    unique_id = models.CharField(max_length=50, unique=True, verbose_name="Unique ID")
    type = models.CharField(max_length=100)
    example = models.TextField(blank=True, null=True)
    concentration = models.CharField(max_length=50, blank=True, null=True)
    frame_formulation = models.ForeignKey(
        FrameFormulation,
        on_delete=models.CASCADE,
        related_name='ingredient_types',
        verbose_name="Frame Formulation"
    )

    class Meta:
        verbose_name = "Ingredient Type"
        verbose_name_plural = "Ingredient Types"
        ordering = ['type']

    def __str__(self):
        return f"{self.type} - {self.frame_formulation.name}"
