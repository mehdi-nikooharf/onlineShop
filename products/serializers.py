from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from rest_framework import serializers


from .models import Category, Image, Product



class CategorySerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if self.instance and 'selected_parent' in attrs:
            if self.instance.id == attrs['selected_parent'].id:
                raise serializers.ValidationError('category can not be self parent')
        return attrs

    selected_parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, required=False)
    def create(self, validated_data):
        selected_parent = None
        if 'selected_parent' in validated_data:
            selected_parent = validated_data.pop("selected_parent").id
        category = Category.objects.create(
            parent_id=selected_parent,
            **validated_data,
        )
        return category

    class Meta:
        model = Category
        fields = ('id', 'title', 'avatar', 'parent', 'selected_parent')
        depth = 1


    def update(self, instance, validated_data):
        selected_parent = None
        if 'selected_parent' in validated_data:
            selected_parent = validated_data.pop("selected_parent").id
        validated_data['parent_id'] = selected_parent

        if 'avatar' not in validated_data:
            validated_data['avatar'] = None

        fields = ['title', 'avatar', 'parent_id']
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:
                pass
        instance.save()

        return instance


    def validate_avatar(self, image):
        # 12MB
        MAX_FILE_SIZE = 12000000
        if image.size > MAX_FILE_SIZE:
            raise ValidationError("File size too big!")
        return image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']



class ProductReadSerializer(serializers.HyperlinkedModelSerializer):

    categories = CategorySerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class  Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'quantity',
            'number_of_sold', 'created_time', 'images',
            'categories', 'avatar', 'price', 'author'
        ]
        depth = 1

    author = serializers.PrimaryKeyRelatedField(source='user.username', read_only=True)


class ProductWriteSerializer(serializers.ModelSerializer):
    selected_categories = serializers.ListField(child=serializers.IntegerField(allow_null=False), write_only=True, required=True)
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
            'user', 'author', 'avatar', 'price'
        ]
        depth = 1

    def validate_uploaded_images(self, images):
        # 12MB
        MAX_FILE_SIZE = 12000000
        for image in images:
            if image.size > MAX_FILE_SIZE:
                raise ValidationError("File size too big!")
        return images

    def validate_avatar(self, image):
        # 12MB
        MAX_FILE_SIZE = 12000000
        if image.size > MAX_FILE_SIZE:
            raise ValidationError("File size too big!")
        return image

    def validate_selected_categories(self, categories):
        categories_object = Category.objects.all()
        for category in categories:
            if not categories_object.filter(pk=category).exists():
                raise ValidationError("this category does not exist")
        return categories


    def validate_price(self, price):
        if price < 0:
            raise ValidationError("Price should be positive!")
        return price

    def validate_quantity(self, quantity):
        if quantity < 0:
            raise ValidationError("Quantity should be positive!")
        return quantity



    def create(self, validated_data):
        uploaded_images = None
        # selected_categories = None
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



    def update(self, instance, validated_data):
        uploaded_images = None
        selected_categories = validated_data.pop('selected_categories', [])

        if 'uploaded_images' in validated_data:
            uploaded_images = validated_data.pop("uploaded_images")

        if 'avatar' not in validated_data:
            validated_data['avatar'] = None

        fields = ['name', 'description', 'quantity', 'avatar']
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:
                pass
        instance.save()

        if selected_categories and len(selected_categories):
            category_objs = []
            for category_id in selected_categories:
                category_obj = get_object_or_404(Category, id=category_id)
                category_objs.append(category_obj)
            instance.categories.set(category_objs)


        if uploaded_images:
            for image in uploaded_images:
                newproduct_image = Image.objects.create(product=instance, image=image)
        return instance









