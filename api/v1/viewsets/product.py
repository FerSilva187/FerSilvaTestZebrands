from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from ..serializers.product import (
	ProductSerializer,
)
from core.models import Product
from api.permissions import isUserStaff
from api.utils import PREVENT_DELETE_MIXINS


class ProductViewSet(*PREVENT_DELETE_MIXINS):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [isUserStaff]
    
    @action(
        methods=["get"],
        detail=False,
        authentication_classes=[],
        permission_classes=[]
    )
    def get(self, request, pk=None):
        """
            RETURN A LIST OF PRODUCTS 
        """
        querysey = self.get_queryset()
        serializer = ProductSerializer(querysey , many=True)
        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=True,
        authentication_classes=[],
        permission_classes=[]
    )
    def view(self, request, pk=None):
        """
            RETURN INFORMATION OF ONE PRODUCT BY ID
        """
        instance = get_object_or_404(Product, id=pk)
        if not request.user.is_authenticated:
            instance.times_consulted += 1
            instance.save()

        serializer = ProductSerializer(instance=instance)
        return Response(serializer.data)



    def create(self, request):
        """
            CREATE AN INSTANCE OF A PRODUCT
        """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            data = dict(serializer.validated_data.items())
            if request.user.is_authenticated:
                data["user_created"] = request.user
            instance = Product.objects.create(**data)
            instance.save()
            serializer = ProductSerializer(instance)
            return self.ok(
                message="The product has been created correctly.",
                product=serializer.data
            )

        error = serializer.errors
        return self.error(status.HTTP_400_BAD_REQUEST, **error)

    def get_queryset(self):

        queryset = self.queryset
        name = self.request.GET.get("name")
        description = self.request.GET.get("description")
        sku = self.request.GET.get("sku")

        if name:
            queryset = queryset.filter(
                name__icontains=name
            )
        
        if description:
            queryset = queryset.filter(
                description__icontains=description
            )
        
        if sku:
            queryset = queryset.filter(
                sku=sku
            )

        return queryset


    @action(
        methods=["post"],
        detail=True,
        serializer_class=ProductSerializer,
    )
    def edit(self, request, pk):
        """
           Endpoint to edit a product. 
        """
        instance = get_object_or_404(Product, id=pk) #return http404 if does not exists
        serializer = ProductSerializer(instance=instance)
        data_before_load = serializer.data
        instance.user_modified = request.user
        serializer = ProductSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()    
            data_after_load = serializer.data

            changes = ""
            """
                WE ITERATE THE PYLOAD RECIVED AND COMAPARE
                WITH THE DATA BEFORE LOAD TO SEND THE CHANGES
                DONE 
            """
            for k, d in data_after_load.items():
                db = data_before_load.get(k)
                if db != d:
                    changes = f"{changes} {k}: {db} to {d} \n"
            
        
            warning_message = ""
            if not settings.EMAIL_HOST:
                warning_message = "Is necesary configure a email host in your .env"
            else:
                emails = User.objects.all().exclude(id=request.user.id).values_list("email", flat=True)
                send_mail(
                    'A product has been edited',
                    f'The product {instance.name} was edited by {request.user.username} \n  {changes}',
                    'admin@zebrands.com',
                    ["fernando@dmspitic.com", ],
                    fail_silently=False,
                )

            return self.ok(                
                message="the product has been edited correctly",
                warning_message=warning_message,
                changes=changes,
            )

        error = serializer.errors
        return self.error(status.HTTP_400_BAD_REQUEST, **error)


    @action(
        methods=["delete"],
        detail=True,
    )
    def deleteProduct(self, request, pk):
        """
           Endpoint to delete a product. 
        """
        instance = get_object_or_404(Product, id=pk) #return http404 if does not exists
        instance.delete()
        return self.ok(
            message="The product has been deleted correctly"
        )


    
    @action(
        methods=["get"],
        detail=False,
    )
    def consultedReport(self, request):
        """
           Endpoint to check products ordered by times consulted. 
        """
        objects = Product.objects.all().order_by("-times_consulted").values(
            "name",
            "sku",
            "times_consulted",
            "price",
        )
        

        return self.ok(
            data=objects
        )
