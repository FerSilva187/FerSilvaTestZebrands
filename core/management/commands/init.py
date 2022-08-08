from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from core.models import Product, Profile
from testZebrands.utils import random_password

class Command(BaseCommand):
    help = (
        "Crea los modelos necesarios"
    )

    def print_divider(self):
        self.stdout.write("*" * 45)

    def create_product(self, name):
        instance = Product()
        instance.sku = f"SKU{name}Test" 
        instance.name = f"{name}" 
        instance.description = f"Test {name}" 
        instance.price = 5
        instance.brand = f"BrandTest-{name}"
        try: 
            instance.save()
        except:
            pass

    def create_user(self):

        if not User.objects.filter(username="admin_test").exists():
            user = User()
            user.username = "admin_test"
            user.set_password("1234")
            user.is_staff = True
            user.save()
        

        profile = Profile()
        profile.user = user
        profile.api_key = random_password(30)
        profile.save()
        self.stdout.write(
            "Se ha creado el usuario 'admin_test' con password: '1234' "
        )
        self.stdout.write(
            f"Api Key = {profile.api_key} "
        )

    def handle(self, *args, **options):

        call_command("migrate")
        self.stdout.write("Migraciones generadas")
        self.print_divider()

        self.stdout.write("Creando productos de prueba")
        self.create_product("Product 1")
        self.create_product("Product 2")
        self.create_product("Product 3")
        self.stdout.write("Se han creado 3 productos de pureba")
        self.print_divider()
        self.create_user()
        self.print_divider()

        self.stdout.write(
            "Proceso finalizado."
        )
