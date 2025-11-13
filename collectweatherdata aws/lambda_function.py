import pymysql
import json
import os  # Para leer variables de entorno

# RDS (datos sensibles como usuario, contraseña y host se leen desde variables de entorno)
host = os.environ['DB_HOST']
user = os.environ['DB_USER']
password = os.environ['DB_PASS']
db_name = "gans"

def lambda_handler(event, context):
    # Conectar a RDS
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    cursor = conn.cursor()

    # Insertar prueba (puedes hacer que los datos vengan del evento)
    cursor.execute(
        "INSERT INTO weather_data (city, temperature, description) VALUES (%s, %s, %s)",
        ("LambdaTest", 22.3, "Cloudy")
    )

    conn.commit()

    # Leer el último registro insertado
    cursor.execute("SELECT * FROM weather_data ORDER BY id DESC LIMIT 1")
    last_entry = cursor.fetchone()

    cursor.close()
    conn.close()

    # Convertir datetime a string para JSON
    last_entry_serializable = list(last_entry)
    last_entry_serializable[4] = str(last_entry_serializable[4])  # columna created_at

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Insert OK desde Lambda",
            "last_entry": last_entry_serializable
        })
    }
