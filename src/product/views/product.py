from django.http.response import HttpResponse
from django.views import generic
from django.views.generic.base import View
from django.shortcuts import render
from product.models import Variant
import ujson as ujson
from product.models import Variant, Product, ProductImage, ProductVariant, ProductVariantPrice

class CreateProductView(View):
    def get(self, request, *args, **kwargs):
        variants = Variant.objects.filter(active=True).values('id', 'title')
        return render(request, 'products/create.html', {'variants': list(variants.all()), 'product': True})
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title', None)
        sku = request.POST.get('sku', None)
        description = request.POST.get('description', None)
        product_image = request.FILES.getlist('product_image', None)
        product_variant = ujson.loads(request.POST.get('product_variant', None))
        product_variant_prices = ujson.loads(request.POST.get('product_variant_prices', None))
        product = Product.objects.create(title=title, sku=sku, description=description)
        for i in product_variant:
            for j in i['tags']:
                ProductVariant.objects.create(variant_title=j, variant_id=i['option'], product_id=product.pk)
        for i in product_variant_prices:
            product_variance_price = ProductVariantPrice()
            title = i['title'].split('/')
            if title[0]:
                provariance = ProductVariant.objects.get(product=product, variant_title=title[0])
                product_variance_price.product_variant_one_id = provariance.pk
            if title[1]:
                provariance = ProductVariant.objects.get(product=product, variant_title=title[1])
                product_variance_price.product_variant_two_id = provariance.pk
            if title[2]:
                provariance = ProductVariant.objects.get(product=product, variant_title=title[2])
                product_variance_price.product_variant_three_id = provariance.pk
            product_variance_price.price = i['price']
            product_variance_price.stock = i['stock']
            product_variance_price.product_id = product.pk
            product_variance_price.save()
        for i in product_image:
            file = i
            ProductImage(file_path=i, product_id=product.pk).save()
        return HttpResponse(status=200)