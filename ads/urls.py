from django.urls import path

from ads.views import IndexView, CategoryListView, AdsListView, CategoryDetailView, AdDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, AdUpdateView, AdDeleteView

urlpatterns = [
    path('', IndexView.as_view()),
    path('cat/', CategoryListView.as_view()),
    path('cat/<int:pk>/', CategoryDetailView.as_view()),
    path('cat/create/', CategoryCreateView.as_view()),
    path('cat/<int:pk>/update/', CategoryUpdateView.as_view()),
    path('cat/<int:pk>/delete/', CategoryDeleteView.as_view()),
    path('ads/', AdsListView.as_view()),
    path('ad/<int:pk>/', AdDetailView.as_view()),
    path('ad/<int:pk>/update/', AdUpdateView.as_view()),
    path('ad/<int:pk>/delete/', AdDeleteView.as_view()),
]

