from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ContactsView,
    ProductCreateView,
    ProductUpdateView,
)

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', ProductCreateView.as_view(), name='add_product'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='edit_product'),
]