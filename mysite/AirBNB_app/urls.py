from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    UserProfileViewSet, CityViewSet, RulesViewSet,
    PropertyListAPIView, PropertyDetailAPIView,
    BookingViewSet, ReviewEditAPIView,ReviewCreateAPIView,RegisterView, LoginView, LogoutView
)


router = SimpleRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'cities', CityViewSet)
router.register(r'rules', RulesViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Подключаем роутер
    path('property/', PropertyListAPIView.as_view(), name='property-list'),
    path('property/<int:pk>/', PropertyDetailAPIView.as_view(), name='property-detail'),
    path('review/', ReviewCreateAPIView.as_view(), name='review-create'),
    path('review/<int:pk>/', ReviewEditAPIView.as_view(), name='review-edit'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
