from rest_framework import serializers

from .models import Category, Product, ProductLine, ProductImage, Attribute, AttributeValue


class CategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='name')

    class Meta:
        model = Category
        fields = ('category', 'slug',)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ('id', 'product_line',)


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ('name', 'id',)


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = ('att_value', 'attribute')


class ProductLineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            'price',
            'sku',
            'stock_qty',
            'order',
            'product_image',
            'attribute_value'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop('attribute_value')

        attr_values = {}
        for key in av_data:
            attr_values.update({key['attribute']['name']: key['att_value']})
        data.update({'specification': attr_values})

        return data


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    product_line = ProductLineSerializer(many=True)
    attribute = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'name',
            'slug',
            'pid',
            'description',
            'category_name',
            'product_line',
            'attribute'
        )

    def get_attribute(self, obj):
        attribute = Attribute.objects.filter(product_type_attribute__product_line_type__product_id=obj.id)
        return AttributeSerializer(attribute, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop('attribute')

        attr_values = {}
        for key in av_data:
            attr_values.update({key['id']: key['name']})
        data.update({'type_specification': attr_values})

        return data


class ProductLineCategorySerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            'price',
            'product_image',
        )


class ProductCategorySerializer(serializers.ModelSerializer):
    product_line = ProductLineCategorySerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'name',
            'slug',
            'pid',
            'created_at',
            'product_line',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        x = data.pop('product_line')

        if x:
            price = x[0]['price']
            image = x[0]['product_image']
            data.update({'price': price})
            data.update({'image': image})

        return data
