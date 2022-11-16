from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles_api import views

router = DefaultRouter()
router.register('signup', views.UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('nickname/', views.NicknameAPIView.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('admin/delete/', views.DeleteUserAPIView.as_view()),
    path('admin/make_admin/', views.MakeAdminAPIView.as_view()),
    path('password/reset/', views.ForgetPassword.as_view()),
    path('password/reset/c/', views.ChangePassword.as_view())
]
