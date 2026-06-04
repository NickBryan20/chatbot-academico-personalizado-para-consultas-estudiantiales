import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_db():
    try:
        # Conectar a la base de datos 'postgres' por defecto
        conn = psycopg2.connect(
            dbname='postgres',
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', ''),
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432')
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Verificar si existe
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'tesis_chatbot_db'")
        exists = cur.fetchone()
        
        if not exists:
            print("Creando base de datos 'tesis_chatbot_db'...")
            cur.execute('CREATE DATABASE tesis_chatbot_db')
            print("¡Base de datos creada exitosamente!")
        else:
            print("La base de datos 'tesis_chatbot_db' ya existe.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_db()
