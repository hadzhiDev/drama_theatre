from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model

from account.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_login',
        )


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[validate_password])

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'password'
        )
        extra_kwargs = {
            'first_name': {'required': True},
        }

    def validate(self, attrs):
        for item in attrs.items():
            if not item[1]:
                raise ValidationError({
                    item[0]: [
                        f'{item[0]} could not be empty'
                    ]
                })
        return attrs

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True,)
    new_password = serializers.CharField(required=True, validators=[validate_password])


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name',)

    def validate(self, attrs):
        for item in attrs.items():
            if not item[1]:
                raise ValidationError({
                    item[0]: [
                        f'{item[0]} could not be empty'
                    ]
                })
        return attrs

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class SendResetPasswordKeySerializer(serializers.Serializer):

    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):

    key = serializers.IntegerField()
    new_password = serializers.CharField(validators=[validate_password])
