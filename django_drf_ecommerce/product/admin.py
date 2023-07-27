from django.contrib import admin

from .models import Brand, Category, Product, ProductLine


class ProductLineInLine(admin.TabularInline):
    model = ProductLine


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'is_digital', 'brand', 'category', 'is_active')
    inlines = [ProductLineInLine]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'parent')


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    fields = ('product', 'price', 'sku', 'stock_qty', 'is_active')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    fields = ('name',)
