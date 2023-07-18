from django.urls import path, include

from .views import CategoryListView, CategoryDetailView


urlpatterns = [
    # path('', ProductListView.as_view(), name= 'product-list'),
    # path('<int:pk>', ProductDetailView.as_view(), name='product-detail'),

    path('categories/', include([
        path('', CategoryListView.as_view(), name='category-list'),
        path('<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
    ])),



    # path('<int:product_id>/files', FileListView.as_view(), name='file-list'),   #show  all file of one product
    # path('<int:product_id>/files/<int:pk>', FileDetailView.as_view(), name='file-detail'),


]
