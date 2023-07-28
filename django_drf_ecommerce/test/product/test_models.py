import pytest
from django.core.exceptions import ValidationError

from django_drf_ecommerce.product.models import ProductTypeAttribute

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Act
        obj = category_factory(name='test_category')

        # Assert
        assert obj.__str__() == 'test_category'


class TestBrandModel:
    def test_str_method(self, brand_factory):
        # Act
        obj = brand_factory(name='test_brand')

        # Assert
        assert obj.__str__() == 'test_brand'


class TestProductModel:
    def test_str_method(self, product_factory):
        # Act
        obj = product_factory()

        # Assert
        assert obj.__str__() == 'test_product'


class TestProductLineModel:
    def test_str_method(self, product_line_factory, attribute_value_factory):
        # Act
        attr = attribute_value_factory(att_value='test')
        obj = product_line_factory.create(sku='12345', attribute_value=(attr,))
        # Assert
        assert obj.__str__() == '12345'

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(order=1, product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj).clean()


class TestProductTypeModel:
    def test_str_method(self, product_type_factory, attribute_factory):
        # Act
        test = attribute_factory(name='test')
        obj = product_type_factory.create(name='test_type', attribute=(test,))

        x = ProductTypeAttribute.objects.get(id=1)


        # Assert
        assert obj.__str__() == 'test_type'


class TestAttributeModel:
    def test_str_method(self, attribute_factory):
        # Act
        obj = attribute_factory(name='test_attribute')
        # Assert
        assert obj.__str__() == 'test_attribute'


class TestAttributeValueModel:
    def test_str_method(self, attribute_value_factory, attribute_factory):
        # Act
        obj_a = attribute_factory(name='test_attribute')
        obj_b = attribute_value_factory(att_value='test_value', attribute=obj_a)
        # Assert
        assert obj_b.__str__() == 'test_attribute-test_value'


class TestProductImageModel:
    def test_str_method(self, product_image_factory):
        # Act
        obj = product_image_factory(order=1)
        # Assert
        assert obj.__str__() == '1'
