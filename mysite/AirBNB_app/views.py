from django.shortcuts import render
from rest_framework import viewsets, generics,status
from .models import (UserProfile, City, Rules,
    Property, Booking, Review
)
from .models import UserProfile, City, Rules
from .pagination import PropertyPagination
from .serializers import (
UserProfileListSerializer,UserProfileDetailSerializer,CitySerializer,
RulesSerializer,PropertyListSerializer,PropertyDetailSerializer,
BookingSerializer,ReviewSerializer,ReviewCreateSerializer,UserProfileRegisterSerializer,LoginSerializer
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import GuestPermissions,HostPermissions,IsHost
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .filters import PropertyFilter
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response



class RegisterView(generics.CreateAPIView):
    serializer_class = UserProfileRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class RulesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer

class PropertyListAPIView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,]
    filterset_class = PropertyFilter
    pagination_class = PropertyPagination
    ordering_fields = [
        'price',
        'rating',
        'created_date', ]
    search_fields = ['title', 'description','city_name']

class PropertyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializer
    permission_classes = [HostPermissions]

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [GuestPermissions]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [GuestPermissions]

class ReviewEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [GuestPermissions]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

