from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Category, Product, ProductLine, ProductImage, AttributeValue, Attribute, ProductType


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


class AttributeValueInLine(admin.TabularInline):
    model = AttributeValue.product_line_attribute_value.through


class AttributeValueProductInLine(admin.TabularInline):
    model = AttributeValue.product_attr_value.through

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_digital', 'category', 'is_active', 'slug')
    inlines = [ProductLineInLine, AttributeValueProductInLine]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_field = ('name', 'parent')


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductLineImageInLine, AttributeValueInLine]


class AttributeInLine(admin.TabularInline):
    model = Attribute.product_type_attribute.through


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        AttributeInLine,
    ]
    list_display = ('id',)


admin.site.register(Attribute)
admin.site.register(AttributeValue)
