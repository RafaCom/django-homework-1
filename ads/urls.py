from django.urls import path

from ads.views.category import CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView
from ads.views.ads import AdsListView, AdDetailView, AdUpdateView, AdDeleteView, AdCreateView, AdUploadImageView
from ads.views.users import UserListView, UserDetailView, UserCreateView, UserUpdateView, UserDeleteView
from ads.views import service

urlpatterns = [
    path('', service.IndexView.as_view()),

    path('cat/', CategoryListView.as_view()),
    path('cat/<int:pk>/', CategoryDetailView.as_view()),
    path('cat/create/', CategoryCreateView.as_view()),
    path('cat/<int:pk>/update/', CategoryUpdateView.as_view()),
    path('cat/<int:pk>/delete/', CategoryDeleteView.as_view()),

    path('ads/', AdsListView.as_view()),
    path('ad/create/', AdCreateView.as_view()),
    path('ad/<int:pk>/', AdDetailView.as_view()),
    path('ad/<int:pk>/update/', AdUpdateView.as_view()),
    path('ad/<int:pk>/delete/', AdDeleteView.as_view()),
    path('ad/<int:pk>/upload_image/', AdUploadImageView.as_view()),

    path('user/', UserListView.as_view()),
    path('user/<int:pk>/', UserDetailView.as_view()),
    path('user/create/', UserCreateView.as_view()),
    path('user/<int:pk>/update/', UserUpdateView.as_view()),
    path('user/<int:pk>/delete/', UserDeleteView.as_view()),
]

