from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles_api import views

router = DefaultRouter()
router.register('signup', views.UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.UserLoginApiView.as_view()),
    path('password/reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
