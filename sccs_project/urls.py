from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products import views as product_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product_views.product_selection_form, name='product_selection_form'),
    path('api/subcategories/', product_views.get_subcategories, name='get_subcategories'),
    path('api/product-types/', product_views.get_product_types, name='get_product_types'),
    path('api/products/', product_views.get_products, name='get_products'),
    path('api/formulations/', product_views.get_formulations, name='get_formulations'),
]

# Add media URL patterns for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Customize admin site
admin.site.site_header = 'SCCS Product Management'
admin.site.site_title = 'SCCS Admin Portal'
admin.site.index_title = 'Welcome to SCCS Product Management Portal'
