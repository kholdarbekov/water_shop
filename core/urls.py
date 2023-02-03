from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePage.as_view(), name="home_page"),
    path("product/?<int:pk>", views.ProductDetailView.as_view(), name="product_detail"),
]
