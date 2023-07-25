from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

from onlineShop.permission import IsProductOwnerOrSuperUser, IsAdminUserOrReadOnly
from .pagination import CustomPageNumberPagination
from .serializers import ImageSerializer, CategorySerializer, ProductReadSerializer, ProductWriteSerializer
from .models import Category, Product, Image


class CategoryListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self,pk):
        try:
            category = Category.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404
        return category
    def put(self, request, pk):
        category = self.get_object(pk=pk)
        serializer = CategorySerializer(category, request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListView(APIView, CustomPageNumberPagination):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly]

    def get(self, request, **kwargs):
        order_by_fields = ['id', '-id', 'name', '-name', 'price', '-price', 'created_time', '-created_time']
        order_by = list(filter(lambda x: x != '', request.GET.get('order_by').split(','))) if request.GET.get('order_by') else []


        options = {}
        options['id__in'] = list(filter(lambda x: x != '' and x.isnumeric(), request.GET.get('ids').split(','))) if request.GET.get('ids') else None
        options['name__icontains'] = request.GET.get('name')
        options['user__username__icontains'] = request.GET.get('author')
        options['price'] = request.GET.get('price') if request.GET.get('price') and request.GET.get('price').isnumeric() else None
        options['price__gte'] = request.GET.get('price_greater_than') if request.GET.get('price_greater_than') and request.GET.get('price_greater_than').isnumeric() else None
        options['price__lte'] = request.GET.get('price_less_than') if request.GET.get('price_less_than') and request.GET.get('price_less_than').isnumeric() else None
        options['number_of_sold'] = request.GET.get('number_of_sold') if request.GET.get('number_of_sold') and request.GET.get('number_of_sold').isnumeric() else None
        options['number_of_sold__gte'] = request.GET.get('number_of_sold_greater_than') if request.GET.get('number_of_sold_greater_than') and request.GET.get('number_of_sold_greater_than').isnumeric() else None
        options['number_of_sold__lte'] = request.GET.get('number_of_sold_less_than') if request.GET.get('number_of_sold_less_than') and request.GET.get('number_of_sold_less_than').isnumeric() else None
        options['quantity'] = request.GET.get('quantity') if request.GET.get('quantity') and request.GET.get('quantity').isnumeric() else None
        options['quantity__gte'] = request.GET.get('quantity_greater_than') if request.GET.get('quantity_greater_than') and request.GET.get('quantity_greater_than').isnumeric() else None
        options['quantity__lte'] = request.GET.get('quantity_less_than') if request.GET.get('quantity_less_than') and request.GET.get('quantity_less_than').isnumeric() else None
        # options['created_time__gte'] = request.GET.get('date_from')
        # options['created_time__lte'] = request.GET.get('date_to')
        options['categories__id__in'] = list(filter(lambda x: x != '' and x.isnumeric(), request.GET.get('categories').split(','))) if request.GET.get('categories') else None


        for order_by_item in order_by:
            if order_by_item not in order_by_fields:
                order_by.remove(order_by_item)


        for option in list(options):
            if options[option] is None:
                del(options[option])

        products = Product.objects.filter(**options).order_by(*order_by)


        if request.user.is_staff:  #Admins have different page_size
            self.page_size = 3  #1000
        result_page = self.paginate_queryset(products, request)
        serializer = ProductReadSerializer(result_page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductWriteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsProductOwnerOrSuperUser]
    def get_object(self, pk, **kwargs):
        try:
            product = Product.objects.get(pk=pk, **kwargs)
        except ObjectDoesNotExist:
            raise Http404
        return product


    def get(self, request, pk):
        product = self.get_object(pk=pk)
        serializer = ProductReadSerializer(product, context={'request': request})
        return Response(serializer.data)
    def put(self, request, pk):
        product = self.get_object(pk=pk)
        if product:
            self.check_object_permissions(request, product)

        serializer = ProductWriteSerializer(product, request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        product = self.get_object(pk=pk, number_of_sold=0)
        if product:
            self.check_object_permissions(request, product)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class ListOrBulkDeleteProductImages(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly, IsProductOwnerOrSuperUser]
    # def get(self, request, product_id, *args, **kwargs):
    #     ids = request.query_params.get('ids').split(',')
    #     queryset = Image.objects.filter(id__in=ids, product_id=product_id)
    #     serializer = ImageSerializer(queryset, many=True)
    #     return Response(serializer.data)

    def delete(self, request, product_id, *args, **kwargs):
        ids = request.query_params.get('ids').split(',')
        try:
            product = Product.objects.get(pk=product_id)
        except ObjectDoesNotExist:
            raise Http404
        if product:
            self.check_object_permissions(request, product)

        if ids:
            queryset = Image.objects.filter(id__in=ids, product_id=product_id)
            if queryset:
                queryset.delete()
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)

