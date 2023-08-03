from django.urls import path, include

from .views import ProductListView, ProductDetailView, ListOrBulkDeleteProductImages
from .views import (CategoryListAPIView, CategoryCreateAPIView, CategoryUpdateAPIView, CategoryDeleteAPIView,

                    )


urlpatterns = [
    path('categories/', include([
        path('', CategoryListAPIView.as_view(), name='category-list'),
        path('create', CategoryCreateAPIView.as_view(), name='category-create'),
        path('update/<int:pk>', CategoryUpdateAPIView.as_view(), name='category-update'),
        path('delete/<int:pk>', CategoryDeleteAPIView.as_view(), name='category-delete'),
    ])),
    
    path('products/', include([
        path('', ProductListView.as_view(), name='product-list'),
        path('<int:pk>', ProductDetailView.as_view(), name='product-detail'),

        path('<int:product_id>/images', ListOrBulkDeleteProductImages.as_view(), name='product-images-delete'),
    ])),

]
