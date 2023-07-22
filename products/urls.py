from django.urls import path, include

from .views import CategoryListView, CategoryDetailView, ProductListView


urlpatterns = [
    path('categories/', include([
        path('', CategoryListView.as_view(), name='category-list'),
        path('<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
    ])),
    path('products/', include([
        path('', ProductListView.as_view(), name='product-list'),
    ])),

]
