# Project 2: Commerce

¡Bienvenido a Commerce! A continuación, encontrarás una descripción general del proyecto, una lista de los archivos incluidos y las instrucciones para ejecutar la aplicación en tu entorno local.

## Descripción del proyecto

Bienvenido a Commerce, una plataforma de subastas que te permite crear, explorar y participar en subastas de diversos productos. La aplicación se implementa utilizando Django y cumple con una serie de características clave para ofrecer una experiencia completa a los usuarios:

## Modelos de la Aplicación

### 1. Usuario Personalizado (`CustomUser`)

- Este modelo representa a los usuarios de la aplicación y hereda de `AbstractUser`.
- Añade un campo personalizado `__str__` para mostrar el nombre de usuario en la representación de cadena.

### 2. Subasta (`Subasta`)

- Modelo que representa los listados de subastas.
- Campos:
  - `producto`: Nombre del producto (cadena, máximo 40 caracteres).
  - `descripcion`: Descripción detallada del producto (texto).
  - `categoria`: Categoría del producto seleccionada de opciones predefinidas.
  - `imagen`: URL de la imagen asociada al producto (cadena, máximo 256 caracteres).
  - `precio_inicial`: Precio inicial del producto en la subasta (decimal, mínimo 0.5).
  - `precio_venta`: Precio de venta del producto (decimal, predeterminado 0.00).
  - `vendedor`: Relación con el usuario vendedor (clave foránea a `CustomUser`).
  - `fecha`: Fecha y hora de creación del listado (automática).
  - `activo`: Indica si la subasta está activa (booleano, predeterminado True).

### 3. Comentario (`Comentario`)

- Modelo que representa los comentarios realizados en los listados de subastas.
- Campos:
  - `usuario`: Relación con el usuario que realiza el comentario (clave foránea a `CustomUser`).
  - `producto`: Relación con el producto al que se refiere el comentario (clave foránea a `Subasta`).
  - `comentario`: Contenido del comentario (texto).
  - `fecha`: Fecha y hora de creación del comentario (automática).

### 4. Oferta (`Oferta`)

- Modelo que registra las ofertas realizadas en los listados de subastas.
- Campos:
  - `usuario`: Relación con el usuario que realiza la oferta (clave foránea a `CustomUser`).
  - `producto`: Relación con el producto al que se refiere la oferta (clave foránea a `Subasta`).
  - `oferta`: Cantidad de la oferta realizada (decimal).

### 5. Lista de Seguimiento (`Watchlist`)

- Modelo que registra los productos agregados a la lista de seguimiento por parte de los usuarios.
- Campos:
  - `usuario`: Relación con el usuario que sigue el listado (clave foránea a `CustomUser`).
  - `producto`: Relación con el producto que se agrega a la lista de seguimiento (clave foránea a `Subasta`).

### Funcionalidades clave:

1. **Creación de Listados:** Los usuarios pueden crear nuevos listados de subastas, proporcionando detalles como título, descripción, precio inicial y categoría. También pueden agregar una imagen opcional.

2. **Página de Listados Activos:** Los usuarios pueden explorar todos los listados de subastas activos, viendo información esencial como título, descripción, precio actual y categoría.

3. **Página de Listado Individual:** Al hacer clic en un listado, los usuarios acceden a una página específica que muestra detalles completos sobre el listado. Pueden realizar ofertas, agregar a la lista de seguimiento y dejar comentarios.

4. **Lista de Seguimiento:** Los usuarios pueden mantener una lista de seguimiento de los listados que les interesan. Pueden agregar o eliminar listados de esta lista.

5. **Categorías:** Existe una página dedicada a mostrar todas las categorías disponibles. Al hacer clic en una categoría, los usuarios pueden ver los listados activos en esa categoría.

6. **Interfaz de Administración:** Los administradores pueden gestionar listados, ofertas, comentarios y categorías a través de la interfaz de administración de Django.

## Video tutorial

   **Youtube**: [https://youtu.be/j85BdENs898?si=KDA7LTmlctu6Kkey](https://youtu.be/kFv_-Uy0Kvg?si=Zvf12nVdOCFrYNgM)

## Estructura de Archivos de la Aplicación

- **commerce/:** Esta carpeta alberga el proyecto principal de Django, configurado como un módulo. La ejecución se realiza desde la ruta raíz a través del archivo `manage.py`.

- **commerce/:** Aquí se encuentra la aplicación principal llamada "commerce".

- **templates/:** Contiene las plantillas HTML que posibilitan la visualización del contenido de la aplicación.

- **static/:** Incluye el archivo CSS y un ícono para la aplicación, estos son utilizados en las plantillas HTML.

- **migrations/:** Registro de todas las migraciones realizadas hacia la base de datos.

## Archivos del Proyecto

- **manage.py:** Archivo principal para gestionar la aplicación Django.

- **db.sqlite3:** Base de datos precreada en SQLite 3 para gestionar toda la información.

## Ejecución de la aplicación

1. Asegúrate de tener Python 3.11 instalado en tu sistema.

2. Instala las dependencias de Python utilizando el siguiente comando:

   ```
   pip install -r requirements.txt
   ```

3. Desde la ruta raíz, ejecuta el siguiente comando para aplicar las migraciones:

   ```
   python manage.py migrate
   ```

4. Crea un superusuario para acceder a la interfaz de administración:

   ```
   python manage.py createsuperuser
   ```

5. Inicia el servidor web Django:

   ```
   python manage.py runserver
   ```

6. Abre tu navegador web y accede a `http://localhost:8000` para comenzar a usar la aplicación.

## Notas Adicionales

- Asegúrate de tener los archivos de la aplicación con la siguiente jerarquía:
   ```
    - commerce
        - migrations
        - static
            - css
            - icons
        - templates
            - layouts
            - registration

    - project2

    manage.py
    .gitignore
    requirements.txt
    db.sqlite3
   ```

¡Espero que disfrutes usando la aplicación de Commerce! Si tienes alguna pregunta o necesitas más información, no dudes en contactarme.

## Hecho por: Carlos Adrián Espinosa Luna
