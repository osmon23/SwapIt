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
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    image = ProductImageSerializer(many=True, read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'created_by',
            'name',
            'description',
            'quantity',
            'image',
        )
        read_only_fields = (
            'id',
            'created_by',
        )
