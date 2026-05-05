# 🏡 RefSur - Plataforma Web

## 📌 Descripción del sistema

RefSur es una aplicación web desarrollada con Django que permite la visualización y compra de productos de una empresa constructora.

El sistema incluye:

* 🪑 Venta de muebles (productos físicos)
* 🏡 Gestión de proyectos de viviendas (servicios)
* 🛒 Carrito de compras
* 💳 Integración de pagos (simulación con Transbank)

---

## 🌐 Acceso a la aplicación (Producción)

👉 https://refsur.onrender.com

---

## 📂 Repositorio del proyecto

👉 https://github.com/maurojasaros/refsur

---

## 🚀 Cómo usar el sistema

### 👤 1. Registro e inicio de sesión

* Ir a “Login”
* Crear una cuenta nueva
* Iniciar sesión

---

### 🛍️ 2. Navegación del catálogo

El sistema presenta dos tipos de productos:

#### 🪑 Muebles

* Tienen stock
* Permiten seleccionar cantidad
* Se pueden agregar directamente al carrito

#### 🏡 Casas (proyectos)

* Solo permiten una unidad en carrito
* Representan un proyecto, no una compra directa
* Incluyen:

  * Ubicación
  * Metros cuadrados
  * Visualización de planos

---

### 🛒 3. Carrito de compras

* Permite agregar productos
* Permite eliminar productos
* Permite modificar cantidades (solo muebles)
* Calcula automáticamente el total

---

### 💳 4. Proceso de compra

Flujo:
Carrito → Finalizar compra → Transbank → Confirmación

---

## 💳 Pago con Transbank (modo simulación)

El sistema utiliza Webpay en modo TEST.

👉 No se realizan cobros reales

### Tarjeta de prueba (aprobada)

VISA: 4051885600446623 (aprobado)
RUT: 11.111.111-1 / clave: 123

### Tarjeta de prueba (rechazada)

MASTERCARD: 5186059559590568 (rechazado)
RUT: 11.111.111-1 / clave: 123

https://www.transbankdevelopers.cl/documentacion/como_empezar#tarjetas-de-prueba


---

## ⚠️ Consideraciones importantes

### 🖼️ Manejo de imágenes

* Se utilizan imágenes estáticas
* No se cargan dinámicamente desde el panel de administración
* Esto se debe a limitaciones del hosting en Render (no persistencia de archivos)

---

### 🏡 Naturaleza de las casas

* No se venden directamente como producto
* Representan un proyecto de construcción
* El pago corresponde a un anticipo o solicitud de servicio

---

### 💳 Pagos

* El sistema utiliza simulación
* No existen transacciones reales

---

## 🧠 Decisiones técnicas relevantes

* Modelo unificado de productos (casas y muebles)
* Lógica diferenciada:

  * Muebles → stock y cantidad variable
  * Casas → sin stock y cantidad fija en carrito
* Validación de stock solo para productos físicos
* Uso de Transbank en entorno sandbox
* Deploy en Render

---

## ⚙️ Tecnologías utilizadas

* Backend: Django
* Frontend: HTML + Bootstrap
* Base de datos: PostgreSQL (producción)
* Deploy: Render
* API de pago: Transbank (modo TEST)

---

## 🔧 Ejecución en entorno local (opcional)

### 1. Clonar repositorio

git clone https://github.com/maurojasaros/refsur.git

### 2. Entrar al proyecto

cd refsur

### 3. Crear entorno virtual

python -m venv venv

### 4. Activar entorno

Windows:
venv\Scripts\activate

Linux/Mac:
source venv/bin/activate

### 5. Instalar dependencias

pip install -r requirements.txt

### 6. Aplicar migraciones

python manage.py migrate

### 7. Crear superusuario (opcional)

python manage.py createsuperuser

### 8. Ejecutar servidor

python manage.py runserver

---

## 📈 Mejoras futuras

* Integración con almacenamiento en la nube (AWS S3 / Cloudinary)
* Implementación de pagos reales
* Sistema de seguimiento de pedidos
* Personalización de proyectos de vivienda
* Optimización de rendimiento y escalabilidad

---






