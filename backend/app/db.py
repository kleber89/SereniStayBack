from pymongo import MongoClient

try:
    client = MongoClient("mongodb://localhost:27017/") #Client
    db = client["sereni_stay"] #DataBase

    #Collections
    users_collection = db["users"]
    admins_collection = db["admins"]
    spas_collection = db["spas"]
    services_collection = db["services"]

    print("MongoDB connected! Databases:", client.list_database_names())

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
