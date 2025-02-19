from motor.motor_asyncio import AsyncIOMotorClient
from bson.binary import UuidRepresentation

client = AsyncIOMotorClient("mongodb://localhost:27017/", UuidRepresentation="standard") #Client

db = client["sereni_stay"] #DataBase

#Collections
users_collection = db["users"]
admins_collection = db["admins"]
spas_collection = db["spas"]
services_collection = db["services"]
bookings_collection = db["bookings"]
