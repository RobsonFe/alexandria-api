from django.urls import path
from .views import (
    CreateBookView,
    GetAllBooksView,
    UpdateBookView,
    DeleteBookView,
    GetBookView,
)

urlpatterns = [
    path('create/', CreateBookView.as_view(), name='create'),
    path('update/<str:pk>/', UpdateBookView.as_view(), name='update'),
    path('delete/<str:pk>/', DeleteBookView.as_view(), name='delete'),
    path('get/<str:pk>/', GetBookView.as_view(), name='get'),
    path('get-all/', GetAllBooksView.as_view(), name='get-all'),
]
