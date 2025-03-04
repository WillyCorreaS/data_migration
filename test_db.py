from sqlalchemy import create_engine

DB_URL = "postgresql://postgres:admin@localhost:5432/empresa"

try:
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        result = conn.execute("SELECT version();")
        for row in result:
            print(row)
    print("Conexión exitosa a PostgreSQL.")
except Exception as e:
    print("Error de conexión:", e)
