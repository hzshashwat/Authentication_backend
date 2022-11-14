from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles_api import views

router = DefaultRouter()
router.register('signup', views.UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('nickname/', views.NicknameAPIView.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('password/reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('admin/delete/', views.DeleteUserAPIView.as_view())
]
