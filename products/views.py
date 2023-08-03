from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status ,filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from onlineShop.permission import IsProductOwnerOrSuperUser, IsAdminUserOrReadOnly
from .pagination import CustomPageNumberPagination
from .serializers import ImageSerializer, CategorySerializer, ProductReadSerializer, ProductWriteSerializer
from .models import Category, Product, Image

from .tasks import send_mail_fun

#Category
class CategoryListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    model = Category
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CategoryCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CategorySerializer

class CategoryUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CategorySerializer
    def get_queryset(self, pk):
        return self.get_serializer().Meta.model.objects.filter(pk=pk).first()
    def put(self, request, pk):
        category = self.get_queryset(pk)
        if category:
            serializer = self.serializer_class(category, request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'pk'




#Product
class ProductListAPIView(ListAPIView):
    model = Product
    serializer_class = ProductReadSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id', 'name', 'price', 'number_of_sold', 'quantity', 'created_time', 'categories', 'description']
    search_fields = ['id', 'name', 'price']
    pagination_class = CustomPageNumberPagination

class ProductCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly]
    serializer_class = ProductWriteSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            send_mail_fun.delay()  #sending email
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductRetrieveAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductReadSerializer
    lookup_field = 'pk'

class ProductUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsProductOwnerOrSuperUser]
    serializer_class = ProductWriteSerializer
    def get_queryset(self, pk):
        return self.get_serializer().Meta.model.objects.filter(pk=pk).first()
    def put(self, request, pk):
        product = self.get_queryset(pk)
        if product:
            self.check_object_permissions(request, product)
            serializer = self.serializer_class(product, request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsProductOwnerOrSuperUser]
    serializer_class = ProductReadSerializer
    def get_queryset(self, pk):
        return self.get_serializer().Meta.model.objects.filter(number_of_sold=0, pk=pk).first()
    def delete(self, request, pk):
        product = self.get_queryset(pk)
        if product:
            self.check_object_permissions(request, product)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)








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

