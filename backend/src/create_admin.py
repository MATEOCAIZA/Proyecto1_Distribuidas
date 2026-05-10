import bcrypt
from pymongo import MongoClient

# Conexión a tu Mongo de Docker
client = MongoClient('mongodb://localhost:27017/')
db = client['chatapp'] 
# Importante: Asegúrate de que esta colección sea la que consulta tu Backend
users_collection = db['admin'] 

def create_admin():
    # Cambiado de email a username
    username = "ana@gmail.com"
    password = "ana45@"
    
    # Encriptar la contraseña para que coincida con la lógica de tu App
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    admin_user = {
        "username": username, # Clave cambiada
        "password": hashed_password.decode('utf-8'),
        "role": "admin", 
        "name": "Administrador"
    }
    
    # Limpia entradas previas si quieres evitar duplicados (opcional)
    # users_collection.delete_one({"username": username})
    
    users_collection.insert_one(admin_user)
    print(f"Usuario admin creado: {username} / {password}")

if __name__ == "__main__":
    create_admin()