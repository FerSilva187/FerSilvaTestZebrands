from logging import warning
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..serializers.user import (
    UserSerializer,
)
from core.models import Product
from api.permissions import isUserStaff
from api.utils import PREVENT_DELETE_MIXINS


class UserViewSet(*PREVENT_DELETE_MIXINS):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [isUserStaff]


    def create(self, request):
        """
            CREATE AN INSTANCE OF A USER
        """
        serializer = all(data=request.data)
        if serializer.is_valid():
            data = dict(serializer.validated_data.items())
            instance = User.objects.create(**data)
            instance.save()
            serializer = UserSerializer(instance)
            return self.ok(
                message="The user has been created correctly.",
                user=serializer.data
            )

        error = serializer.errors
        return self.error(status.HTTP_400_BAD_REQUEST, **error)

    def get_queryset(self):

        queryset = self.queryset
        first_name = self.request.GET.get("first_name")
        username = self.request.GET.get("username")

        if first_name:
            queryset = queryset.filter(
                first_name__icontains=first_name
            )
        
        if username:
            queryset = queryset.filter(
                username=username
            )

        return queryset

    @action(
        methods=["get"],
        detail=False,
    )
    def get(self, request, pk=None):
        querysey = self.get_queryset()
        serializer = UserSerializer(querysey , many=True)
        return Response(serializer.data)


    @action(
        methods=["post"],
        detail=True,
        serializer_class=UserSerializer,
    )
    def edit(self, request, pk):
        """
           endpoint to edit a user. 
        """
        instance = get_object_or_404(User, id=pk) #return http404 if does not exists
        serializer = UserSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()    
            return self.ok(                
                message="the user has been edited correctly"
            )

        error = serializer.errors
        return self.error(status.HTTP_400_BAD_REQUEST, **error)


    @action(
        methods=["delete"],
        detail=True,
    )
    def deleteUser(self, request, pk):
        """
           endpoint to delete a user. 
        """
        instance = get_object_or_404(User, id=pk) #return http404 if does not exists
        instance.delete()
        return self.ok(
            message="The user has been deleted correctly"
        )

