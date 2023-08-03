from django.urls import path, include

from .views import (CategoryListAPIView, CategoryCreateAPIView, CategoryUpdateAPIView, CategoryDeleteAPIView,
                    ProductListAPIView, ProductRetrieveAPIView, ProductUpdateAPIView, ProductDeleteAPIView,
                    BulkDeleteProductImages, ProductCreateAPIView
                    )


urlpatterns = [
    path('categories/', include([
        path('', CategoryListAPIView.as_view(), name='category-list'),
        path('create', CategoryCreateAPIView.as_view(), name='category-create'),
        path('update/<int:pk>', CategoryUpdateAPIView.as_view(), name='category-update'),
        path('delete/<int:pk>', CategoryDeleteAPIView.as_view(), name='category-delete'),
    ])),

    path('products/', include([
        path('', ProductListAPIView.as_view(), name='product-list'),
        path('create', ProductCreateAPIView.as_view(), name='product-create'),
        path('<int:pk>', ProductRetrieveAPIView.as_view(), name='product-detail'),
        path('update/<int:pk>', ProductUpdateAPIView.as_view(), name='category-update'),
        path('delete/<int:pk>', ProductDeleteAPIView.as_view(), name='category-delete'),
        path('<int:product_id>/images', BulkDeleteProductImages.as_view(), name='product-images-delete'),

    ])),

]
