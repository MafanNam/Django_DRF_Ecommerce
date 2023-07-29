import factory

from django_drf_ecommerce.product.models import Category, Product, ProductLine, ProductImage, ProductType, \
    Attribute, AttributeValue


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: 'test_category_%d' % n)
    slug = factory.Sequence(lambda n: 'test_slug_%d' % n)



# class AttributeFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Attribute
#
#     name = 'attribute_name_test'
#     description = 'attribute_description_test'
#
#
# class ProductTypeFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = ProductType
#
#     name = 'test type'
#
#     @factory.post_generation
#     def attribute(self, create, extracted, **kwargs):
#         if not create or not extracted:
#             return
#         self.attribute.add(*extracted)
#
#
# class ProductFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Product
#
#     name = 'test_product'
#     description = 'test_description'
#     is_digital = True
#     category = factory.SubFactory(CategoryFactory)
#     product_type = factory.SubFactory(ProductTypeFactory)
#     is_active = True
#
#
# class AttributeValueFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = AttributeValue
#
#     att_value = 'att_test'
#     attribute = factory.SubFactory(AttributeFactory)
#
#
# class ProductLineFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = ProductLine
#
#     price = 10.00
#     sku = "12345"
#     stock_qty = 1
#     product = factory.SubFactory(ProductFactory)
#     is_active = True
#
#     @factory.post_generation
#     def attribute_value(self, create, extracted, **kwargs):
#         if not create or not extracted:
#             return
#         self.attribute_value.add(*extracted)
#
#
# class ProductImageFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = ProductImage
#
#     alternative_text = 'test alternative text'
#     url = 'test.jpg'
#     product_line = factory.SubFactory(ProductLineFactory)
