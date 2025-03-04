# 🚀 Proyecto de Migración y Análisis de Datos con FastAPI y PostgreSQL

Este proyecto implementa una solución completa para la migración, almacenamiento, análisis y consulta de datos utilizando **FastAPI**, **PostgreSQL** y **Python**.

## 📌 **Descripción del Proyecto**
Se han desarrollado múltiples funcionalidades para la carga, respaldo, restauración y análisis de datos almacenados en una base de datos **PostgreSQL**.

### 🔹 **Características Principales**
✅ API REST con **FastAPI** para consultas y análisis de datos.
✅ Carga de datos desde archivos CSV a PostgreSQL.
✅ Backup y restauración de la base de datos en formato **AVRO**.
✅ Visualización de datos en formato gráfico.
✅ Consultas optimizadas con **SQLAlchemy**.

---
## 🏗️ **Instalación y Configuración**

### 1️⃣ **Clonar el repositorio**
```sh
 git clone https://github.com/tu_usuario/tu_repositorio.git
 cd tu_repositorio
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
│── 📜 load_data.py         # Script para cargar datos en PostgreSQL
│── 📜 backup.py            # Script para realizar backups en AVRO
│── 📜 restore.py           # Script para restaurar la base de datos desde AVRO
│── 📜 conexion_db.py       # Conexión a PostgreSQL con SQLAlchemy
│── 📜 requirements.txt     # Dependencias del proyecto
│── 📜 README.md            # Documentación del proyecto
```

---
## ⚙️ **Archivos y Funcionalidades**

### 🔹 `main.py` - API REST con FastAPI
- `/employees_per_department` → Devuelve empleados contratados por trimestre y departamento.
- `/departments_above_mean` → Devuelve los departamentos que contrataron más empleados que el promedio.

### 🔹 `load_data.py` - Carga de Datos en PostgreSQL
- Lee los archivos CSV y los carga en la base de datos.
- Filtra datos inválidos y verifica claves foráneas.

### 🔹 `backup.py` - Copia de Seguridad en Formato AVRO
- Genera backups de las tablas en archivos `.avro` dentro de `data/`.

### 🔹 `restore.py` - Restauración de Datos desde AVRO
- Restaura los datos de los archivos `.avro` en PostgreSQL.

### 🔹 `conexion_db.py` - Conexión con PostgreSQL
- Gestiona la conexión a la base de datos mediante **SQLAlchemy**.

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
SELECT * FROM departments LIMIT 10;
SELECT * FROM jobs LIMIT 10;
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
Si encuentras algún problema, revisa que la base de datos **PostgreSQL** esté corriendo y que las dependencias estén correctamente instaladas. ¡Disfruta programando! 💻🔥

