
## Instalación en Linux
### Instalar virtualenv
```
sudo apt-get install python3-pip
sudo pip3 install virtualenv
```
### Instalar sqllite
```
sudo apt-get install sqlite3
```
### AGREGAMOS EL ARCHIVO .env en la raiz con las siguientes variables
EMAIL_HOST=""
EMAIL_HOST_USER=""
EMAIL_HOST_PASSWORD=""
BASE_URL="http://localhost:8000"
TEST_API_KEY=""

### Instalación de dependencias
Activamos el virtualenv:
```
cd ~/Projects/testZebrands
source venv/bin/activate
```

```
pip install -r requirements.txt
```

Corremos el comando init.py para generar las migraciones, crear tablas, generar usuario 'admin' y crear productos de prueba
```
python manage.py init
```

Corremos el Projecto:
```
python manage.py runserver
```

## APIS
para ver la documentación de las apis podemos entrar a :```http://localhost:8000/api/v1/docs/ ``` es necesario hacer login con el usuario creado
en el comando init.

Para hacer un requests a endpoints como crear/editar/eliminar productos o crear/edtiar/eliminar usuarios  es necesario enviar el api_key generado en el comando
init como parámetro get(api_key)

/api/v1/products/ -- POST para crear un producto (es necesario enviar api_key)
/api/v1/products/consultedReport/ -- GET consultar reporte de mas veces visitado
/api/v1/products/get/ -- GET obtener listado de producto
/api/v1/products/{id}/deleteProduct/ -- DELETE eliminar un producto (es necesario enviar api_key)
/api/v1/products/{id}/edit/ -- POST editar un producto (es necesario enviar api_key)
/api/v1/products/{id}/view/ -- GET ver información de un producto
/api/v1/users/ --- POST para crear un usuario (es necesario enviar api_key)
/api/v1/users/get/ -- GET ver listado de usuarios (es necesario enviar api_key)
/api/v1/users/{id}/ -- GET ver un usuario(es necesario enviar api_key)
/api/v1/users/{id}/deleteUser/ -- DELETE eliminar un usuario (es necesario enviar api_key)
/api/v1/users/{id}/edit/ -- POST editar un usuario (es necesario enviar api_key)



## TEST 
python manage.py test

## CORREOS
PARA ENVIAR CORREOS ES NECESARIO AÑADIR LOS VALORES A LAS VARIABLES DEL .ENV
EMAIL_HOST
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD