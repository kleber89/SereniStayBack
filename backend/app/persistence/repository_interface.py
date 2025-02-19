from app.db import db
from abc import ABC, abstractmethod
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient

class Repository(ABC):
    "Abstract methods, the subclasses will inherit them and each one must implement these methods"

    def __init__(self, collection_name):
        self.collection = db[collection_name]

    @abstractmethod
    async def add(self, obj):
        pass
    
    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def update(self, obj_id, data):
        pass

    @abstractmethod
    async def delete(self, obj_id):
        pass

    @abstractmethod
    async def get_by_attribute(self, attr_name, attr_value):
        pass


class UserRepository(Repository):
    def __init__(self):
        super().__init__('users')

    async def get_by_attribute(self, attr_name, attr_value):
        return await self.collection.find_one({attr_name: attr_value})

    async def get_all(self):
        return [doc async for doc in self.collection.find()]

    async def add(self, obj):
        obj["_id"] = str(obj["id"]) #this save the id how string in MongoDB
        result = await self.collection.insert_one(obj)
        return result.inserted_id

    async def update(self, obj_id: UUID, data):
        return await self.collection.update_one(
            {"_id": str(obj_id)},
            {"$set": data}
        )

    async def delete(self, obj_id: UUID):
        return await self.collection.delete_one({"_id": str(obj_id)})



class AdminRepository(Repository):
    def __init__(self):
        super().__init__('admins')

    async def get_by_attribute(self, attr_name, attr_value):
        return await self.collection.find_one({attr_name: attr_value})

    async def get_all(self):
        return [doc async for doc in self.collection.find()]

    async def add(self, obj):
        obj["_id"] = str(obj["id"])
        result = await self.collection.insert_one(obj)
        return result.inserted_id

    async def update(self, obj_id: UUID, data):
        return await self.collection.update_one(
            {"_id": str(obj_id)},
            {"$set": data}
        )

    async def delete(self, obj_id: UUID):
        return await self.collection.delete_one({"_id": str(obj_id)})

class SpaRepository(Repository):
    def __init__(self):
        super().__init__('spas')

    async def get_by_attribute(self, attr_name, attr_value):
        return await self.collection.find_one({attr_name: attr_value})

    async def get_all(self):
        return [doc async for doc in self.collection.find()]

    async def add(self, obj):
        obj["_id"] = str(obj["id"])
        result = await self.collection.insert_one(obj)
        return result.inserted_id

    async def update(self, obj_id: UUID, data):
        return await self.collection.update_one(
            {"_id": str(obj_id)},
            {"$set": data}
        )

    async def delete(self, obj_id: UUID):
        return await self.collection.delete_one({"_id": str(obj_id)})


class ServiceRepository(Repository):
    def __init__(self):
        super().__init__('services')

    async def get_by_attribute(self, attr_name, attr_value):
        return await self.collection.find_one({attr_name: attr_value})

    async def get_all(self):
        return [doc async for doc in self.collection.find()]

    async def add(self, obj):
        obj["_id"] = str(obj["id"])
        result = await self.collection.insert_one(obj)
        return result.inserted_id

    async def update(self, obj_id: UUID, data):
        return await self.collection.update_one(
            {"_id": str(obj_id)},
            {"$set": data}
        )

    async def delete(self, obj_id: UUID):
        return await self.collection.delete_one({"_id": str(obj_id)})


class BookingRepository(Repository):
    def __init__(self):
        super().__init__('bookings')

    async def get_by_attribute(self, attr_name, attr_value):
        return await self.collection.find_one({attr_name: attr_value})

    async def get_all(self):
        return [doc async for doc in self.collection.find()]

    async def add(self, obj):
        obj["_id"] = str(obj["id"])
        result = await self.collection.insert_one(obj)
        return result.inserted_id

    async def update(self, obj_id: UUID, data):
        return await self.collection.update_one(
            {"_id": str(obj_id)},
            {"$set": data}
        )

    async def delete(self, obj_id: UUID):
        return await self.collection.delete_one({"_id": str(obj_id)})
