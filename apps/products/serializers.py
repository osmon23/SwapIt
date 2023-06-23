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
        read_only_fields = (
            'id',
            'product',
        )


class ProductImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            'image',
        )


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    images = ProductImageCreateSerializer(many=True, required=False)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES  # Получаем данные изображений из запроса
        validated_data.pop('images', None)  # Удаляем поле images из validated_data

        product = Product.objects.create(**validated_data)

        for image_data in images_data.values():
            ProductImage.objects.create(product=product, image=image_data)

        return product

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'created_by',
            'name',
            'description',
            'quantity',
            'images',
        )
        read_only_fields = (
            'id',
            'created_by',
        )
