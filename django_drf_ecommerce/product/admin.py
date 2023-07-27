from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Brand, Category, Product, ProductLine, ProductImage


class EditLinkInLine(object):
    def edit(self, instance):
        url = reverse(
            f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change", args=[instance.pk]
        )
        if instance.pk:
            link = mark_safe(f'<a href="{url}">edit</a>')
            return link
        else:
            return ''


class ProductLineInLine(EditLinkInLine, admin.TabularInline):
    model = ProductLine
    readonly_fields = ('edit',)


class ProductLineImageInLine(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'is_digital', 'brand', 'category', 'is_active', 'slug')
    inlines = [ProductLineInLine]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'parent')


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    fields = ('product', 'price', 'sku', 'stock_qty', 'is_active', 'order')
    inlines = [ProductLineImageInLine]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    fields = ('name',)
