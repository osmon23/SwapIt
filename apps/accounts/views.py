from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.db.models import Avg

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Rating
from .serializers import UserSerializer, GroupSerializer, UserLoginSerializer, UserRegistrationSerializer, \
    RatingSerializer, UserPasswordChangeSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        ratings_received = Rating.objects.filter(to_user=instance)
        rating_serializer = RatingSerializer(ratings_received, many=True)
        data = serializer.data
        data['received_ratings'] = rating_serializer.data
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserLoginView(APIView):
    queryset = User.objects.all()
    permission_classes = []
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
            else:
                return Response({'error': 'Неверное имя пользователя или пароль'}, status=400)

        return Response(serializer.errors, status=400)


class UserRegistrationView(APIView):
    permission_classes = []
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({'message': 'Пользователь успешно зарегистрирован', 'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        from_user = request.user
        to_user_id = request.data.get('to_user')
        rating_value = request.data.get('rating')

        if to_user_id is None or rating_value is None:
            return Response({'error': 'Необходимо указать идентификатор пользователя и значение рейтинга'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            to_user = User.objects.get(pk=to_user_id)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь с указанным идентификатором не существует'},
                            status=status.HTTP_400_BAD_REQUEST)

        if from_user == to_user:
            return Response({'error': 'Нельзя оценить самого себя'}, status=status.HTTP_400_BAD_REQUEST)

        existing_rating = Rating.objects.filter(from_user=from_user, to_user=to_user).exists()
        if existing_rating:
            return Response({'error': 'Вы уже оценили этого пользователя'}, status=status.HTTP_400_BAD_REQUEST)

        rating = Rating(from_user=from_user, to_user=to_user, rating=rating_value)
        rating.save()

        # Обновление рейтинга у пользователя, к которому была оставлена оценка
        updated_rating = Rating.objects.filter(to_user=to_user).aggregate(Avg('rating'))
        to_user.rating = updated_rating['rating__avg']
        to_user.save()

        return Response({'message': 'Оценка успешно добавлена'}, status=status.HTTP_201_CREATED)


class UserPasswordChangeView(generics.UpdateAPIView):
    serializer_class = UserPasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.object = self.get_object()
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']

            if not self.object.check_password(current_password):
                return Response({'error': 'Неверный текущий пароль'}, status=status.HTTP_400_BAD_REQUEST)

            validate_password(new_password)
            self.object.set_password(new_password)
            self.object.save()
            return Response({'message': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
