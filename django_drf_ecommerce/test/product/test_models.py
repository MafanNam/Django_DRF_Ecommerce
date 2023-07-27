import pytest
from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Arrange

        # Act
        obj = category_factory(name='test_category')

        # Assert
        assert obj.__str__() == 'test_category'


class TestBrandModel:
    def test_str_method(self, brand_factory):
        # Arrange

        # Act
        obj = brand_factory(name='test_brand')

        # Assert
        assert obj.__str__() == 'test_brand'


class TestProductModel:
    def test_str_method(self, product_factory):
        # Arrange

        # Act
        obj = product_factory()

        # Assert
        assert obj.__str__() == 'test_product'


class TestProductLineModel:
    def test_str_method(self, product_line_factory):
        # Arrange

        # Act
        obj = product_line_factory(sku='12345')
        # Assert
        assert obj.__str__() == '12345'

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(order=1, product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj).clean()


class TestProductImage:
    def test_str_method(self, product_image_factory):
        # Act
        obj = product_image_factory(order=1)
        # Assert
        assert obj.__str__() == '1'

