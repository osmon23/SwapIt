from django.urls import path
from rest_framework import routers

from .views import UserViewSet, GroupViewSet, UserLoginView, UserRegistrationView, RatingViewSet, UserPasswordChangeView

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('login/', UserLoginView.as_view()),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('<int:pk>/change-password/', UserPasswordChangeView.as_view(), name='change-password'),
]

urlpatterns += router.urls
