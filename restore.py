import fastavro
import pandas as pd
from conexion_db import get_engine

def restore_table(table_name):
    """Restaura una tabla en la base de datos desde un archivo AVRO."""
    file_path = f"data/{table_name}.avro"

    try:
        with open(file_path, "rb") as f:
            reader = fastavro.reader(f)
            records = [record for record in reader]  # Leer los datos del archivo AVRO

        if not records:
            print(f"El archivo {file_path} está vacío. No se restauró la tabla {table_name}.")
            return

        df = pd.DataFrame(records)

        # Convertir columnas de fecha de string a datetime si es necesario
        for column in df.columns:
            if df[column].dtype == "object":  # Posibles fechas en formato string
                try:
                    df[column] = pd.to_datetime(df[column])
                except ValueError:
                    pass  # Si no se puede convertir, dejar como está

        # Restaurar los datos en la base de datos
        df.to_sql(table_name, get_engine(), if_exists="replace", index=False)
        print(f"Datos restaurados en la tabla {table_name} desde {file_path}")

    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no existe.")
    except Exception as e:
        print(f"Error restaurando {table_name}: {e}")

if __name__ == "__main__":
    tables = ["hired_employees", "departments", "jobs"]
    for table in tables:
        restore_table(table)
