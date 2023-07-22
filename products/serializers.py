from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import serializers
from .models import Category, Image, Product



class CategorySerializer(serializers.ModelSerializer):
    # parent_id = serializers.PrimaryKeyRelatedField(queryset=Parent.objects.all(),source='parent.id')
    class Meta:
        model = Category
        fields = ('id', 'title', 'avatar', 'parent')
        depth = 1


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']



class ProductReadSerializer(serializers.HyperlinkedModelSerializer):

    categories = CategorySerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class  Meta:
        model = Product
        fields = [ 'id', 'author', 'name', 'description', 'categories', 'images', 'quantity', 'number_of_sold', 'created_time']
        depth = 1

    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user.username')
    author = serializers.PrimaryKeyRelatedField(source='user.username', read_only=True)





class ProductWriteSerializer(serializers.ModelSerializer):
    selected_categories = serializers.ListField(child=serializers.CharField(allow_blank=False), write_only=True, required=True)
    author = serializers.PrimaryKeyRelatedField(source='user.username', read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault(), write_only=True)
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )


    class  Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'quantity',
            'number_of_sold', 'created_time', 'images',
            'uploaded_images', 'categories', 'selected_categories',
            'user', 'author'
        ]
        depth = 1



    def create(self, validated_data):
        uploaded_images = None
        selected_categories = None
        user = validated_data.pop('user')
        selected_categories = validated_data.pop('selected_categories', [])

        if 'uploaded_images' in validated_data:
            uploaded_images = validated_data.pop("uploaded_images")


        product = Product.objects.create(
            user=user,
            **validated_data,
        )

        if selected_categories and len(selected_categories):
            category_objs = []
            for category_id in selected_categories:
                category_obj = get_object_or_404(Category, id=category_id)
                category_objs.append(category_obj)
                product.categories.add(category_obj)

        if uploaded_images:
            for image in uploaded_images:
                newproduct_image = Image.objects.create(product=product, image=image)
        return product






