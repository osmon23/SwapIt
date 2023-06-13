from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.CharField(default=None)

    class Meta:
        model = Category
        fields = (
            'name',
            'parent',
        )
        read_only_fields = (
            'id',
        )


class ProductImageSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = ProductImage
        fields = (
            'id',
            'product',
            'image',
        )


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(read_only=True)
    image = ProductImageSerializer

    class Meta:
        model = Product
        fields = '__all__'
