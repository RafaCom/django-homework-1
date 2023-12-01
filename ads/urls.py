from django.urls import path

from ads.views import IndexView, CategoryView, AdsView, CategoryDetailView, AdDetailView

urlpatterns = [
    path('', IndexView.as_view()),
    path('cat/', CategoryView.as_view()),
    path('cat/<int:pk>/', CategoryDetailView.as_view()),
    path('ad/', AdsView.as_view()),
    path('ad/<int:pk>/', AdDetailView.as_view()),
]

