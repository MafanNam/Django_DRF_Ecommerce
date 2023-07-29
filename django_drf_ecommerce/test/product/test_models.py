import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from django_drf_ecommerce.product.models import ProductTypeAttribute, Category, Product, ProductLine

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


class TestProductModel:
    def test_str_output(self, product_factory):
        obj = product_factory(name='test_product')
        assert obj.__str__() == 'test_product'

    def test_name_max_length(self, product_factory):
        name = 'x' * 236
        obj = product_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_slug_max_length(self, product_factory):
        slug = 'x' * 256
        obj = product_factory(slug=slug)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_pid_max_length(self, product_factory):
        pid = 'x' * 11
        obj = product_factory(pid=pid)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_name_unique_field(self, product_factory):
        product_factory(name='test_name')
        with pytest.raises(IntegrityError):
            product_factory(name='test_name')

    def test_slug_unique_field(self, product_factory):
        product_factory(slug='test_slug')
        with pytest.raises(IntegrityError):
            product_factory(slug='test_slug')

    def test_pid_unique_field(self, product_factory):
        product_factory(pid='test_pid')
        with pytest.raises(IntegrityError):
            product_factory(pid='test_pid')

    def test_is_active_false_default(self, product_factory):
        obj = product_factory()
        assert obj.is_active is False

    def test_is_digital_false_default(self, product_factory):
        obj = product_factory()
        assert obj.is_digital is False

    def test_fk_product_on_delete_protect(self, product_type_factory, product_factory):
        obj1 = product_type_factory()
        product_factory(product_type=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_return_product_active_only_true(self, product_factory):
        product_factory(is_active=True)
        product_factory(is_active=False)
        qs = Product.objects.is_active().count()
        assert qs == 1

    def test_return_product_active_only_false(self, product_factory):
        product_factory(is_active=True)
        product_factory(is_active=False)
        qs = Product.objects.count()
        assert qs == 2


class TestProductLineModel:
    def test_str_output(self, product_line_factory):
        obj = product_line_factory(sku='12345')
        assert obj.__str__() == '12345'

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(order=1, product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj).clean()

    def test_field_decimal_places(self, product_line_factory):
        price = 1.0001
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_field_sku_max_length(self, product_line_factory):
        sku = 'x' * 11
        with pytest.raises(ValidationError):
            product_line_factory(sku=sku)

    def test_is_active_false_default(self, product_line_factory):
        obj = product_line_factory()
        assert obj.is_active is False

    def test_fk_product_line_on_delete_protect(self, product_type_factory, product_line_factory):
        obj1 = product_type_factory()
        product_line_factory(product_type=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_return_product_line_active_only_true(self, product_line_factory):
        product_line_factory(is_active=True)
        product_line_factory(is_active=False)
        qs = ProductLine.objects.is_active().count()
        assert qs == 1

    def test_return_product_line_active_only_false(self, product_line_factory):
        product_line_factory(is_active=True)
        product_line_factory(is_active=False)
        qs = ProductLine.objects.count()
        assert qs == 2


class TestProductImageModel:
    def test_str_output(self, product_image_factory, product_line_factory):
        obj1 = product_line_factory(sku='12345')
        obj2 = product_image_factory(product_line=obj1)
        assert obj2.__str__() == f"{obj1.sku}_img"

    def test_alternative_text_max_length(self, product_image_factory):
        alternative_text = 'x' * 101
        with pytest.raises(ValidationError):
            product_image_factory(alternative_text=alternative_text)

    def test_duplicate_order_values(self, product_image_factory, product_line_factory):
        obj = product_line_factory()
        product_image_factory(order=1, product_line=obj)
        with pytest.raises(ValidationError):
            product_image_factory(order=1, product_line=obj).clean()


class TestProductTypeModel:
    def test_str_output(self, product_type_factory):
        obj = product_type_factory.create(name='test_type')
        assert obj.__str__() == 'test_type'

    def test_name_field_max_length(self, product_type_factory):
        name = 'x' * 101
        obj = product_type_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()




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

