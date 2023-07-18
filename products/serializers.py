from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    # parent_id = serializers.PrimaryKeyRelatedField(queryset=Parent.objects.all(),source='parent.id')
    class Meta:
        model = Category
        fields = ('id', 'title', 'avatar', 'parent')
        depth = 1

