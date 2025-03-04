from conexion_db import get_engine

def truncate_tables():
    engine = get_engine()
    with engine.connect() as connection:
        connection.execute("TRUNCATE TABLE hired_employees RESTART IDENTITY CASCADE;")
        connection.execute("TRUNCATE TABLE departments RESTART IDENTITY CASCADE;")
        connection.execute("TRUNCATE TABLE jobs RESTART IDENTITY CASCADE;")
        print("Tablas truncadas correctamente.")

if __name__ == "__main__":
    truncate_tables()
