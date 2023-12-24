from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import CustomUser, Client


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'group', 'first_name', 'last_name']

        extra_kwargs = {'password': {
            # Permet de cacher le password, si on possède la liste des utilisateurs avec une méthode GET
            'write_only': True,
            'required': True,
            # Permet de cacher le password dans le champ Password ( de base le mot de passe est en clair)
            "style": {'input_type': 'password'},
        }
        }

    @staticmethod
    def validate_password(value):
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

    def create(self, validated_data):

        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"