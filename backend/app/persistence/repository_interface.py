from app.db import db
from abc import ABC, abstractmethod
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

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
        obj["id"] = str(obj["id"]) #this save the id how string in MongoDB
        await self.collection.insert_one(obj)
        return obj["id"]

    async def update(self, obj_id: UUID, data):
        return await self.collection.update_one(
            {"id": str(obj_id)},
            {"$set": data}
        )

    async def delete(self, obj_id: UUID):
        try:
            result = await self.collection.delete_one({"id": str(obj_id)})
            if result.deleted_count == 0:
                raise ValueError("El objeto no fue encontrado o ya había sido eliminado.")
            return {"success": "El objeto fue eliminado correctamente"}
        except PyMongoError as e:
            raise RuntimeError(f"Error en la base de datos: {str(e)}")




class SpaRepository(Repository):
    def __init__(self):
        super().__init__('spas')

    async def get_by_attribute(self, attr_name, attr_value):
        return await self.collection.find_one({attr_name: attr_value})

    async def get_all(self):
        return [doc async for doc in self.collection.find()]

    async def add(self, obj):
        obj["id"] = str(obj["id"])
        await self.collection.insert_one(obj)
        return obj["id"]

    async def update(self, obj_id: UUID, data):
        return await self.collection.update_one(
            {"id": str(obj_id)},
            {"$set": data}
        )

    async def delete(self, obj_id: UUID):
        try:
            result = await self.collection.delete_one({"id": str(obj_id)})
            if result.deleted_count == 0:
                raise ValueError("The object was not found or had already been deleted.")
            return {"success": "The object was successfully removed"}
        except PyMongoError as e:
            raise RuntimeError(f"Error in the database: {str(e)}")


class ServiceRepository(Repository):
    def __init__(self):
        super().__init__('services')

    async def get_by_attribute(self, attr_name, attr_value):
        return [doc async for doc in self.collection.find({attr_name: attr_value})]

    

    async def get_all(self):
        return [doc async for doc in self.collection.find()]

    async def add(self, obj):
        obj["id"] = str(obj["id"])
        await self.collection.insert_one(obj)
        return obj["id"]

    async def update(self, obj_id: UUID, data):
        result = await self.collection.update_one(
            {"id": str(obj_id)},
            {"$set": data}
        )
        
        return result.modified_count > 0

    async def delete(self, obj_id: UUID):
        try:
            result = await self.collection.delete_one({"id": str(obj_id)})
            if result.deleted_count == 0:
                raise ValueError("The object was not found or had already been deleted.")
            return {"success": "The object was successfully removed"}
        except PyMongoError as e:
            raise RuntimeError(f"Error in the database: {str(e)}")


class BookingRepository(Repository):
    def __init__(self):
        super().__init__('bookings')


    async def add(self, booking_data):
        """Insert a new booking into the database."""
        booking_data["id"] = str(booking_data["id"])
        
        result = await self.collection.insert_one(booking_data)
        return str(result.inserted_id)
    

    async def get_by_attribute(self, attr_name, attr_value):
        return await self.collection.find_one({attr_name: attr_value})

    async def get_all(self):
        return [doc async for doc in self.collection.find()]



    async def update(self, obj_id: UUID, data):
        return await self.collection.update_one(
            {"id": str(obj_id)},
            {"$set": data}
        )

    async def delete(self, obj_id: UUID):
        try:
            result = await self.collection.delete_one({"id": str(obj_id)})
            if result.deleted_count == 0:
                raise ValueError("The object was not found or had already been deleted.")
            return {"success": "The object was successfully removed"}
        except PyMongoError as e:
            raise RuntimeError(f"Error in the database: {str(e)}")
        

    async def cancel_booking(self, booking_id: str):
        """Cancel a reservation by changing its status to 'cancelled'"""
        
        result = await self.collection.update_one(
            {"id": booking_id},
            {"$set": {"status": "cancelled"}}
        )
        return result.modified_count > 0
    


class ReviewRepository(Repository):
    def __init__(self):
        super().__init__('reviews')

    async def get_by_attribute(self, attr_name, attr_value):
        return await self.collection.find_one({attr_name: attr_value})

    async def get_all(self):
        return [doc async for doc in self.collection.find()]

    async def add(self, obj):
        obj["id"] = str(obj["id"]) #this save the id how string in MongoDB
        await self.collection.insert_one(obj)
        return obj["id"]

    async def update(self, obj_id: UUID, data):
        return await self.collection.update_one(
            {"id": str(obj_id)},
            {"$set": data}
        )

    async def delete(self, obj_id: UUID):
        try:
            result = await self.collection.delete_one({"id": str(obj_id)})
            if result.deleted_count == 0:
                raise ValueError("El objeto no fue encontrado o ya había sido eliminado.")
            return {"success": "El objeto fue eliminado correctamente"}
        except PyMongoError as e:
            raise RuntimeError(f"Error en la base de datos: {str(e)}")