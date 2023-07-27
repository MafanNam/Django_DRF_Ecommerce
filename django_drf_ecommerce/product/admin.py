from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Brand, Category, Product, ProductLine, ProductImage, AttributeValue, Attribute, ProductType


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
    list_field = ('name', 'parent')


class AttributeValueInLine(admin.TabularInline):
    model = AttributeValue.product_line_attribute_value.through


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductLineImageInLine, AttributeValueInLine]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    fields = ('name',)


class AttributeInLine(admin.TabularInline):
    model = Attribute.product_type_attribute.through


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        AttributeInLine,
    ]


admin.site.register(Attribute)
admin.site.register(AttributeValue)
