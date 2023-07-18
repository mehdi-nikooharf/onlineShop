import os

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import CategorySerializer
from .models import Category


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request':request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    def get_object(self,pk):
        try:
            category = Category.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404
        return category
    def put(self, request, pk):
        category = self.get_object(pk=pk)
        serializer = CategorySerializer(category, request.data)
        if serializer.is_valid():
            oldImg = category.avatar.path
            if os.path.exists(oldImg):
                os.remove(oldImg)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk=pk)
        oldImg = category.avatar.path
        if os.path.exists(oldImg):
            os.remove(oldImg)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
