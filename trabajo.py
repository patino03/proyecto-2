import mysql.connector
from mysql.connector import Error

def create_connection():
    """Crea la conexión a la base de datos"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',            # El usuario por defecto de XAMPP es 'root'
            password='',            # Si no configuraste contraseña, déjalo vacío
            database='equipo_futbol'  # Nombre de la base de datos
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos equipo_futbol")
            return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def close_connection(connection):
    """Cierra la conexión a la base de datos"""
    if connection.is_connected():
        connection.close()
        print("Conexión cerrada correctamente")

def insert_team(connection, team_name, country):
    """Inserta un nuevo equipo en la tabla Teams"""
    try:
        cursor = connection.cursor()
        query = "INSERT INTO Teams (team_name, country) VALUES (%s, %s)"
        cursor.execute(query, (team_name, country))
        connection.commit()
        print("Equipo insertado correctamente")
    except Error as e:
        print(f"Error al insertar el equipo: {e}")

# Conectarse a la base de datos
connection = create_connection()

# Insertar datos en la tabla Teams
if connection:
    insert_team(connection, "Real Madrid", "España")
    insert_team(connection, "Manchester United", "Inglaterra")
    insert_team(connection, "Bayern Munich", "Alemania")
    
    # Cerrar la conexión
    close_connection(connection)
