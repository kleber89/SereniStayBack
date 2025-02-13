from app import db
from abc import ABC, abstractmethod
from bson import ObjectId #For queries with _id

class Repository(ABC):
    "Abstract methods, the subclasses will inherit them and each one must implement these methods"

    def __init__(self, collection_name):
        self.collection = db[collection_name]

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class UserRepository(Repository):
    def __init__(self):
        super().__init__('users')

    def get(self, obj_id):
        return self.collection.find_one({"_id": ObjectId(obj_id)})

    def get_all(self):
        return list(self.collection.find())

    def add(self, obj):
        return self.collection.insert_one(obj).inserted_id

    def update(self, obj_id, data):
        return self.collection.update_one(
            {"_id": ObjectId(obj_id)},
            {"$set": data}
        )

    def delete(self, obj_id):
        return self.collection.delete_one({"_id": ObjectId(obj_id)})

    def get_by_attribute(self, attr_name, attr_value):
        pass


class AdminRepository(UserRepository):
    def __init__(self):
        super().__init__('admins')


class SpaRepository(UserRepository):
    def __init__(self):
        super().__init__('spas')


class ServiceRepository(UserRepository):
    def __init__(self):
        super().__init__('services')
