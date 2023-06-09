from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

from phonenumber_field.serializerfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber

from rest_framework import serializers

from config import settings

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    phone_number = PhoneNumberField()

    def create(self, validated_data):
        default_region = getattr(settings, 'PHONENUMBER_DEFAULT_REGION', None)

        if default_region:
            phone_number = validated_data['phone_number']
            updated_phone_number = PhoneNumber.from_string(str(phone_number), default_region)
            validated_data['phone_number'] = updated_phone_number
            print(validated_data['phone_number'])

        return super().create(validated_data)

    class Meta:
        model = User
        fields = (
            'id',
            'url',
            'username',
            'email',
            'phone_number',
            'created_at',
            'password',
        )


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = (
            'url',
            'name'
        )


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'password'
        )


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password'
        )
