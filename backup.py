import fastavro
import pandas as pd
from conexion_db import get_engine

def generate_avro_schema(df, table_name):
    #Generamos un esquema AVRO a partir de un DataFrame
    fields = []
    for column, dtype in df.dtypes.items():
        avro_type = "string"  # Por default
        if "int" in str(dtype):
            avro_type = "int"
        elif "float" in str(dtype):
            avro_type = "float"
        elif "bool" in str(dtype):
            avro_type = "boolean"
        elif "datetime" in str(dtype):  # Detecta campos tipo datetime
            avro_type = "string"

        fields.append({"name": column, "type": avro_type})

    return {
        "type": "record",
        "name": table_name,
        "fields": fields
    }

def backup_table(table_name):
    df = pd.read_sql(f"SELECT * FROM {table_name}", get_engine())

    if df.empty:
        print(f"La tabla {table_name} está vacía. No se generó el backup.") #Validación tabla vacía
        return

    # Convertir columnas datetime a string
    for column in df.select_dtypes(include=["datetime"]).columns:
        df[column] = df[column].astype(str)

    schema = generate_avro_schema(df, table_name)
    records = df.to_dict(orient="records")  # Convierte el DataFrame en lista de diccionarios

    with open(f"data/{table_name}.avro", "wb") as f:
        fastavro.writer(f, schema, records)

    print(f"Copia de seguridad creada: data/{table_name}.avro")

if __name__ == "__main__":
    tables = ["hired_employees", "departments", "jobs"]
    for table in tables:
        backup_table(table)
