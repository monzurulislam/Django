from django.urls import path
from django.views.generic import TemplateView
from product.models import Product

from product.views.product import CreateProductView
from product.views.variant import VariantView, VariantCreateView, VariantEditView

app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', CreateProductView.as_view(), name='create.product'),
    path('list/', TemplateView.as_view(template_name='products/list.html', extra_context={
        'products':   Product.objects.prefetch_related('product_variant_price__product_variant_one__variant',
                                                    'product_variant_price__product_variant_two__variant',
                                                    'product_variant_price__product_variant_three__variant')
    }), name='list.product'),
]
