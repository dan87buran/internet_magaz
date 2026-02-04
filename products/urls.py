from django.urls import path
from .views import (
    ProductListView, ProductCreateView,
    ProductUpdateView, ProductDeleteView,
    ProductDetailView
)
from .views import ProductModerationView

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
 path('<int:pk>/moderate/', ProductModerationView.as_view(), name='product_moderation'),
]