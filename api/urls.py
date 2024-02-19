from django.urls import path, include
from api import views
from .yasg import urlpatterns as url_doc

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('news', views.NewsViewSet)
router.register('gallery', views.PhotoViewSet)
router.register('photo-category', views.PhotoCategoryViewSet)

urlpatterns = [
    path('auth/', include('api.auth.urls')),

    path('', include(router.urls))
]

urlpatterns += url_doc