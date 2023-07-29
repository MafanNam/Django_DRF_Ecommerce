import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from django_drf_ecommerce.product.models import ProductTypeAttribute, Category

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_output(self, category_factory):
        obj = category_factory(name='test_cat')

        assert obj.__str__() == 'test_cat'

    def test_name_max_length(self, category_factory):
        name = "x" * 236
        obj = category_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_slug_max_length(self, category_factory):
        slug = "x" * 256
        obj = category_factory(slug=slug)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_name_unique_field(self, category_factory):
        category_factory(name='test_cat')
        with pytest.raises(IntegrityError):
            category_factory(name='test_cat')

    def test_slug_unique_field(self, category_factory):
        category_factory(slug='test_slug')
        with pytest.raises(IntegrityError):
            category_factory(slug='test_slug')

    def test_is_active_false_default(self, category_factory):
        obj = category_factory()
        assert obj.is_active is False

    def test_parent_category_on_delete_protect(self, category_factory):
        obj1 = category_factory()
        category_factory(parent=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_parent_field_null(self, category_factory):
        obj1 = category_factory()
        assert obj1.parent is None

    def test_return_category_active_only_true(self, category_factory):
        category_factory(is_active=True)
        category_factory(is_active=False)
        qs = Category.objects.is_active().count()
        assert qs == 1

    def test_return_category_active_only_false(self, category_factory):
        category_factory(is_active=True)
        category_factory(is_active=False)
        qs = Category.objects.count()
        assert qs == 2


# class TestProductModel:
#     def test_str_method(self, product_factory):
#         # Act
#         obj = product_factory()
#
#         # Assert
#         assert obj.__str__() == 'test_product'
#
#
# class TestProductLineModel:
#     def test_str_method(self, product_line_factory, attribute_value_factory):
#         # Act
#         attr = attribute_value_factory(att_value='test')
#         obj = product_line_factory.create(sku='12345', attribute_value=(attr,))
#         # Assert
#         assert obj.__str__() == '12345'
#
#     def test_duplicate_order_values(self, product_line_factory, product_factory):
#         obj = product_factory()
#         product_line_factory(order=1, product=obj)
#         with pytest.raises(ValidationError):
#             product_line_factory(order=1, product=obj).clean()
#
#
# class TestProductTypeModel:
#     def test_str_method(self, product_type_factory, attribute_factory):
#         # Act
#         test = attribute_factory(name='test')
#         obj = product_type_factory.create(name='test_type', attribute=(test,))
#
#         x = ProductTypeAttribute.objects.get(id=1)
#
#
#         # Assert
#         assert obj.__str__() == 'test_type'
#
#
# class TestAttributeModel:
#     def test_str_method(self, attribute_factory):
#         # Act
#         obj = attribute_factory(name='test_attribute')
#         # Assert
#         assert obj.__str__() == 'test_attribute'
#
#
# class TestAttributeValueModel:
#     def test_str_method(self, attribute_value_factory, attribute_factory):
#         # Act
#         obj_a = attribute_factory(name='test_attribute')
#         obj_b = attribute_value_factory(att_value='test_value', attribute=obj_a)
#         # Assert
#         assert obj_b.__str__() == 'test_attribute-test_value'
#
#
# class TestProductImageModel:
#     def test_str_method(self, product_image_factory):
#         # Act
#         obj = product_image_factory(order=1)
#         # Assert
#         assert obj.__str__() == '1'
