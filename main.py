from fastapi import FastAPI, HTTPException, Body
from sqlalchemy import text
from conexion_db import get_engine
import pandas as pd
import matplotlib.pyplot as plt
import io
from fastapi.responses import StreamingResponse
import traceback

app = FastAPI()

# Definir límites de inserción
MAX_BATCH_SIZE = 1000
MIN_BATCH_SIZE = 1
# Definir estructura esperada de cada tabla
TABLE_SCHEMAS = {
    "departments": ["id", "department"],
    "jobs": ["id", "job"],
    "hired_employees": ["id", "name", "datetime", "department_id", "job_id"]
}

# Endpoint para insertar nuevos datos
@app.post("/insert")
async def insert(data: dict = Body(...)):
    try:
        engine = get_engine()

        # Validación de estructura de datos
        for table, expected_columns in TABLE_SCHEMAS.items():
            if table in data:
                df = pd.DataFrame(data[table])

                # Validar si los datos contienen todas las columnas requeridas
                missing_cols = [col for col in expected_columns if col not in df.columns]
                if missing_cols:
                    raise HTTPException(status_code=400, detail=f"Faltan columnas {missing_cols} en la tabla {table}")

                # Validar límite de registros
                if not (MIN_BATCH_SIZE <= len(df) <= MAX_BATCH_SIZE):
                    raise HTTPException(status_code=400, detail=f"La tabla {table} debe contener entre {MIN_BATCH_SIZE} y {MAX_BATCH_SIZE} registros.")

                # Validar que no haya valores nulos
                if df.isnull().values.any():
                    raise HTTPException(status_code=400, detail=f"La tabla {table} contiene valores nulos.")
                
                # Inicializar variables para evitar error de referencia
                invalid_departments = []
                invalid_jobs = []

                # Validar FK en hired_employees
                if table == "hired_employees":
                    valid_departments = pd.read_sql("SELECT id FROM departments", engine)["id"].tolist()
                    valid_jobs = pd.read_sql("SELECT id FROM jobs", engine)["id"].tolist()

                    invalid_departments = df[~df["department_id"].isin(valid_departments)]["department_id"].unique().tolist()
                    invalid_jobs = df[~df["job_id"].isin(valid_jobs)]["job_id"].unique().tolist()

                if invalid_departments or invalid_jobs:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Los siguientes IDs no existen en la BD -> departamentos: {invalid_departments}, trabajos: {invalid_jobs}"
                    )

                # Insertar datos en la base de datos
                df.to_sql(table, engine, if_exists="append", index=False)

        return {"message": "Datos insertados correctamente"}
    
    except Exception as e:
        error_detail = traceback.format_exc()
        print(error_detail)
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# Endpoint para obtener empleados contratados por trimestre, departamento y trabajo
@app.get("/employees_per_department")
async def employees_per_department():
    try:
        engine = get_engine()
        query = """
            SELECT 
                d.department AS department, 
                j.job AS job,
                COUNT(*) FILTER (WHERE EXTRACT(QUARTER FROM he.datetime) = 1) AS Q1,
                COUNT(*) FILTER (WHERE EXTRACT(QUARTER FROM he.datetime) = 2) AS Q2,
                COUNT(*) FILTER (WHERE EXTRACT(QUARTER FROM he.datetime) = 3) AS Q3,
                COUNT(*) FILTER (WHERE EXTRACT(QUARTER FROM he.datetime) = 4) AS Q4
            FROM hired_employees he
            JOIN departments d ON he.department_id = d.id
            JOIN jobs j ON he.job_id = j.id
            WHERE EXTRACT(YEAR FROM he.datetime) = 2021
            GROUP BY d.department, j.job
            ORDER BY d.department, j.job;
        """
        with engine.connect() as connection:
            result = connection.execute(text(query))
            data = [dict(row) for row in result]
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener departamentos que contrataron más empleados que el promedio
@app.get("/departments_above_mean")
async def departments_above_mean():
    try:
        engine = get_engine()
        query = """
            WITH department_hired AS (
                SELECT he.department_id, d.department, COUNT(*) AS hired
                FROM hired_employees he
                JOIN departments d ON he.department_id = d.id
                WHERE EXTRACT(YEAR FROM he.datetime) = 2021
                GROUP BY he.department_id, d.department
            )
            SELECT d.department_id AS id, d.department, d.hired
            FROM department_hired d
            WHERE d.hired > (SELECT AVG(hired) FROM department_hired)
            ORDER BY d.hired DESC;
        """
        with engine.connect() as connection:
            result = connection.execute(text(query))
            data = [dict(row) for row in result]

        # Crear reporte visual
        df = pd.DataFrame(data)
        plt.figure(figsize=(10, 6))

        # Crear el gráfico de barras
        bars = plt.bar(df['department'], df['hired'], color='skyblue')

        # Etiquetas en las barras
        for bar in bars:
            yval = bar.get_height()  # Obtener la altura de cada barra
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5,  # Posición (x, y) de la etiqueta
                    str(int(yval)),  # El valor a mostrar (convertido a entero)
                    ha='center', va='bottom', fontsize=10)

        # Agregar etiquetas y título
        plt.xlabel("Departamento")
        plt.ylabel("Número de empleados contratados")
        plt.title("Departamentos que contrataron más empleados que el promedio en 2021")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        # Guardar el gráfico en un objeto de bytes y enviarlo como respuesta
        img_stream = io.BytesIO()
        plt.savefig(img_stream, format="png")
        img_stream.seek(0)
        plt.close()

        return StreamingResponse(img_stream, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
