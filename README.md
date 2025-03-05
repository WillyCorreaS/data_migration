# 🚀 **Coding Challenge**

Este proyecto implementa una solución para la migración, almacenamiento, análisis y consulta de datos utilizando **FastAPI**, **PostgreSQL** y **Python**.

Se presentan dos retos para el desarrollo:

## **Reto #1**

Eres un ingeniero de datos y vas a comenzar un proyecto importante: una migración de datos masivos a un nuevo sistema de base de datos. Debes crear una Prueba de Concepto (PoC) que cumpla con los siguientes requisitos:

Mover datos históricos desde archivos en formato CSV a la nueva base de datos.

✅ Crear un servicio API REST para recibir nuevos datos, asegurando que:

#### 🔹 Cada nueva transacción cumpla con las reglas del diccionario de datos.

#### 🔹 Se puedan insertar transacciones en lotes (de 1 a 1000 filas en una sola solicitud).

#### 🔹 Se pueda recibir la información para todas las tablas en el mismo servicio.

#### 🔹 Se respeten las reglas de datos para cada tabla.

✅ Implementar una funcionalidad para hacer copias de seguridad de cada tabla y almacenarlas en el sistema de archivos en formato AVRO.

✅ Implementar una funcionalidad para restaurar una tabla específica a partir de su copia de seguridad.

## **Reto #2**

Explorar los datos insertados en el primer reto y proporcionar métricas específicas a los stakeholders. Se debe crear un endpoint para cada requerimiento.

Requerimientos:

✅ Número de empleados contratados en 2021 por trimestre, desglosado por departamento y trabajo.

#### Ejemplo de salida:

| **departamento** | **trabajo**   | **Q1** | **Q2** | **Q3** | **Q4** |
|-----------------|--------------|-------|-------|-------|-------|
| Staff          | Reclutador   | 3     | 0     | 7     | 11    |
| Staff          | Gerente      | 2     | 1     | 0     | 2     |
| Supply Chain   | Gerente      | 0     | 1     | 3     | 0     |

✅ Lista de IDs, nombre y número de empleados contratados en los departamentos que contrataron más empleados que el promedio general de 2021. Ordenado por número de empleados contratados en orden descendente.

#### Ejemplo de salida:

| **id** | **departamento** | **contratados** |
|------|----------------|-------------|
| 1    | Staff         | 45          |
| 2    | Supply Chain  | 12          |



## 📌 **Descripción del Proyecto**
Se han desarrollado múltiples funcionalidades para la carga, respaldo, restauración y análisis de datos almacenados en una base de datos **PostgreSQL**.

### 🔹 **Características Principales**
✅ API REST con **FastAPI** para consultas y análisis de datos.
✅ Carga de datos desde archivos CSV a PostgreSQL.
✅ Backup y restauración de la base de datos en formato **AVRO**.
✅ Visualización de datos en formato gráfico para el número de empleados contratados en los departamentos que contrataron más empleados que el promedio general de 2021.
✅ Consultas optimizadas con **SQLAlchemy**.

---
## 🏗️ **Instalación y Configuración**

### 1️⃣ **Clonar el repositorio**
```sh
 git clone https://github.com/WillyCorreaS/data_migration.git
 cd data_migration
```

### 2️⃣ **Crear un entorno virtual y activarlo**
```sh
python -m venv venv
```
- En **Windows**:
```sh
venv\Scripts\activate
```
- En **Mac/Linux**:
```sh
source venv/bin/activate
```

### 3️⃣ **Instalar dependencias**
```sh
pip install -r requirements.txt
```

### 4️⃣ **Configurar PostgreSQL**
Asegúrate de tener **PostgreSQL** instalado y en ejecución.
```sql
CREATE DATABASE empresa;
```
Modifica `conexion_db.py` con las credenciales correctas:
```python
DB_URL = "postgresql://usuario:contraseña@localhost:5432/empresa"
```

### 5️⃣ **Ejecutar el Servidor de la API**
```sh
uvicorn main:app --reload
```
La API estará disponible en: **http://127.0.0.1:8000/docs**

---
## 📂 **Estructura del Proyecto**
```plaintext
📁 data_migration/
│── 📂 data/                # Archivos de datos CSV y backups en formato AVRO
│── 📜 main.py              # API REST con FastAPI
│── 📜 etl_data.py          # Script para cargar datos en PostgreSQL
│── 📜 backup.py            # Script para realizar backups en AVRO
│── 📜 restore.py           # Script para restaurar la base de datos desde AVRO
│── 📜 conexion_db.py       # Conexión a PostgreSQL con SQLAlchemy
│── 📜 test_db.py           # Script para test DB en PostgreSQL
│── 📜 truncate.py          # Script para truncar las tablas en PostgreSQL
│── 📜 requirements.txt     # Dependencias del proyecto
│── 📜 README.md            # Documentación del proyecto
```

---
## ⚙️ **Archivos y Funcionalidades**

### 🔹 `main.py` - API REST con FastAPI
- `/employees_per_department` → Devuelve empleados contratados por trimestre y departamento.
- `/departments_above_mean` → Devuelve los departamentos que contrataron más empleados que el promedio.

### 🔹 `etl_data.py` - Carga y limpia los Datos en PostgreSQL
- Lee los archivos CSV y los carga en la base de datos.
- Filtra datos inválidos y verifica claves foráneas.

### 🔹 `backup.py` - Copia de Seguridad en Formato AVRO
- Genera backups de las tablas en archivos `.avro` dentro de `data/`.

### 🔹 `restore.py` - Restauración de Datos desde AVRO
- Restaura los datos de los archivos `.avro` en PostgreSQL.

### 🔹 `conexion_db.py` - Conexión con PostgreSQL
- Gestiona la conexión a la base de datos mediante **SQLAlchemy**.

### 🔹 `test_db.py` - Test DB con PostgreSQL
- Valida la conexión a la base de datos mediante **SQLAlchemy** y devulve un mensaje de éxito o error.

### 🔹 `truncate.py` - Trunca los datos de las tablas
- Elimina los datos de las tablas y devuelve un mensaje: **Tablas truncadas correctamente.**.

---
## 🛠️ **Comandos Útiles**

### 🔄 **Eliminar Datos de las Tablas** (Truncar la BD)
```sql
TRUNCATE TABLE hired_employees RESTART IDENTITY CASCADE;
TRUNCATE TABLE departments RESTART IDENTITY CASCADE;
TRUNCATE TABLE jobs RESTART IDENTITY CASCADE;
```

### 🧐 **Verificar Datos en las Tablas**
```sql
SELECT * FROM hired_employees LIMIT 10;
SELECT * FROM departments;
SELECT * FROM jobs;
```

### 📦 **Respaldar Datos**
```sh
python backup.py
```

### 🔄 **Restaurar Datos desde Backup**
```sh
python restore.py
```

---
## 🚀 **Notas Finales**
Si encuentras algún problema, revisa que la base de datos **PostgreSQL** esté corriendo y que las dependencias estén correctamente instaladas! 💻🔥
