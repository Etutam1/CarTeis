Botón Facturar:
Podemos crear una factura sin viajes para después agregárselos, o previamente agregar viajes a la tabla, y una vez crea-
dos completamos los campos de la factura y al darle a facturar creará una factura y los viajes asociados a la factura en
la base de datos.

Botones Tabla Viajes:
El botón de la papelera selecciona la fila del botón y elimina el viaje.
El botón del lápiz es para editar el viaje, para eso hay que previamente seleccionar el viaje, hacer las modificaciones
en el formulario de la izquierda y una vez hechas le damos click a dicho botón y saltará una ventana para confirmar

Botón Tabla facturas:
El botón de la papelera selecciona la fila del botón y elimina la factura.

Filtro Tabla facturas:
Al activar el checkbox se revelará un campo donde introducir el dni de cliente/conductor o el número de factura por el
que queremos flitrar. Además podemos irnos al panel de clientes o conductores y hacer click en un cliente/ conductor en
su tabla y se nos introducirá su DNI en este campo para filtrar Facturas, dependiendo el rbt seleccionado.

Botón Lupa Frame Información Factura:
Busca en el panel de clientes si existe dicho por su Dni, en caso contrario se nos notifica por una ventana emergente.

Campo Kms:
Al seleccionar QComboBox de Municipio de Origen/Destino, y comprobar que los dos tienen algo seleccionado, se calcula
la distancia através de geopy através de la comparación de dos puntos según su latitud y altitud. Previamente comprobará
si tenemos conexión a internet, en caso contrario se nos notificará y desbloqueará el campo y tendremos que introducir
el valor a mano.

para crear requisitos:

	pip freeze > requirements.txt


para instalar requisitos:

	pip install -r requirements.txt
