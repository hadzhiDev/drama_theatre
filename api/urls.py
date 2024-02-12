from django.urls import path, include
# import api.views
# from . import views
# from .yasg import urlpatterns as url_doc


urlpatterns = [
    path('auth/', include('api.auth.urls')),

    # path('', include(router.urls))
]