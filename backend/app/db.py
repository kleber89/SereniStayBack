from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017/", UuidRepresentation="standard") #Client

db = client["sereni_stay"] #DataBase

#Collections
users_collection = db["users"]
spas_collection = db["spas"]
services_collection = db["services"]
bookings_collection = db["bookings"]
reviews_collection = db["reviews"]
