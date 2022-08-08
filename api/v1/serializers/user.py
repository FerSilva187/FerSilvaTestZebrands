from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "email",
            "is_staff",
            "password"
        ]

        read_only_fields =  (
            "id",
        )
        
    
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    is_staff = serializers.BooleanField(write_only=True)
