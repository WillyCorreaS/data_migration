import pandas as pd
from conexion_db import get_engine

def load_csv_to_db():
    engine = get_engine()

    # Definir los nombres de las columnas
    employees_columns = ["id", "name", "datetime", "department_id", "job_id"]
    departments_columns = ["id", "department"]
    jobs_columns = ["id", "job"]

    # Cargar CSV asegurando que pandas no use la primera fila como nombres de columnas
    employees = pd.read_csv("data/hired_employees.csv", header=None, sep=",", names=employees_columns)
    departments = pd.read_csv("data/departments.csv", header=None, sep=",", names=departments_columns)
    jobs = pd.read_csv("data/jobs.csv", header=None, sep=",", names=jobs_columns)

    # Insertar primero departments y jobs para evitar problemas de FK
    departments.to_sql("departments", engine, if_exists="append", index=False)
    jobs.to_sql("jobs", engine, if_exists="append", index=False)

    # Filtrar filas donde haya valores nulos en employees
    employees = employees.dropna(subset=["id", "name", "datetime", "job_id", "department_id"])

    # Convertir department_id y job_id a enteros (en caso de que vengan como float por los nulos previos)
    employees["department_id"] = employees["department_id"].astype(int)
    employees["job_id"] = employees["job_id"].astype(int)

    # Leer los IDs válidos desde la base de datos
    valid_departments = pd.read_sql("SELECT id FROM departments", engine)
    valid_jobs = pd.read_sql("SELECT id FROM jobs", engine)

    # Filtrar empleados solo con department_id y job_id válidos
    employees = employees[
        employees["department_id"].isin(valid_departments["id"]) &
        employees["job_id"].isin(valid_jobs["id"])
    ]

    # Insertar los datos limpios en la base de datos
    employees.to_sql("hired_employees", engine, if_exists="append", index=False)

    print("¡Datos cargados correctamente!")

if __name__ == "__main__":
    load_csv_to_db()
