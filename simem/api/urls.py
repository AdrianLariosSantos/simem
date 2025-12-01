from django.urls import path, include
from rest_framework.routers import DefaultRouter
from usuarios.viewsets import UsuariosViewSet
from usuarios.views import CustomAuthToken, Logout
from catalogos.viewsets import CatalogoHashTagViewSet
from movilizaciones.viewsets import ExpedientesViewSet, RegistroViewSet, HashTagRegistroViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuariosViewSet, basename='usuarios')
router.register(r'catalogos/hashtags', CatalogoHashTagViewSet, basename='catalogo-hashtag')
router.register(r'expedientes', ExpedientesViewSet, basename='expedientes')
router.register(r'registros', RegistroViewSet, basename='registros')
router.register(r'hashtag-registros', HashTagRegistroViewSet, basename='hashtag-registros')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', CustomAuthToken.as_view(), name='api-login'),
    path('auth/logout/', Logout.as_view(), name='api-logout'),
]
