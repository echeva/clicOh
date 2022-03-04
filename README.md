# clicOh
### Prueba de conocimiento con Django Rest Framework
#### [Objetivo]
Analizar el nivel de conocimiento de los postulantes a desarrollador de backend Clicoh.

#### [Prueba lógica]
Crear una API REST utilizando DJANGO REST FRAMEWORK, que brinde la funcionalidad básica y acotada de un Ecommerce.

#### Instalación 
`Python 3.8.12`
<pre> pip install -r requirements.txt </pre>
<pre> python manage.py createsuperuser </pre>

### API endpoints

#### Obtener token
`POST /api/token/`

``` sh
Body: 
    {
        "username": <string>,
        "password": <string>
    }

Response: 
    {
        "refresh": <refresh>,
        "access": <access>
    } 
```

#### Authorization header

``` sh
Header: { Authorization Bearer:  Token <access> }
```

#### Listar todos los productos
`GET /api/products/`

#### Consultar un producto
`GET /api/products/{id}/`

#### Registrar un producto
`POST /api/products/`

 ``` sh
 Body: 
    {
        "name": <string>,
        "price": <decimal>,
        "stock": <integer>
    }
```

#### Editar un producto
`PATCH /api/products/{id}/`

``` sh
 Body: 
   {
        "name": <string><optional>,
        "price": <decimal><optional>,
        "stock": <integer><optional>
   }
``` 

#### Eliminar un producto
`DELETE /api/products/{id}/`


#### Listar todas las ordenes
`GET /api/orders/`

#### Consultar una orden y sus detalles
`GET /api/orders/{id}`

#### Registrar una orden (inclusive sus detalles). Debe actualizar el stock del producto
`POST /api/orders/`

``` sh 
Body: 
    {
        "date_time": "2022-02-17 01:23:00",
        "details": [
            {
                "product": <product_id>,
                "quantity": <quantity>
            },
            {
                "product": <product_id>,
                "quantity": <quantity>
            }
        ]
    }
```

#### Editar una orden (inclusive sus detalles). Debe actualizar el stock del producto
`PATCH /api/orders/{id}/`

``` sh
Body: 
    {
        "date_time": "2022-02-17 01:23:00",
        "details": [
            {
                "id": <id><optional>,
                "product": <product_id>,
                "quantity": <quantity>
            },
            {
                "id": <id><optional>,
                "product": <product_id>,
                "quantity": <quantity>
            }
        ]
    }
```

#### Eliminar una orden. Restaura stock del producto
`DELETE /api/orders/{id}/`
