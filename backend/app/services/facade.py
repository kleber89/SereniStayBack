from app.persistence.repository_interface import (
    UserRepository, AdminRepository,
    ServiceRepository, SpaRepository,
    BookingRepository)
from app.models.user import User
from app.models.admin import Admin
from app.models.spa import Spa
from app.models.service import Service
from app.models.booking import Booking
from uuid import UUID, uuid4


class Facade:
    def __init__(self):
        self.user_db = UserRepository()
        self.admin_db = AdminRepository()
        self.spa_db = SpaRepository()
        self.service_db = ServiceRepository()
        self.booking_db = BookingRepository()



# ___________________________________User______________________________________________________
    
    async def create_user(self, user_data):
        user = User(**user_data)
        return await self.user_db.add(user.model_dump())
    
    async def update_user(self, user_id: UUID, user_data):
        return await self.user_db.update(str(user_id), user_data)
    
    async def get_user_by_attribute(self, attr_name, attr_value):
        return await self.user_db.get_by_attribute(attr_name, attr_value)
    
    async def get_all_users(self):
        return await self.user_db.get_all()
    
    async def delete_user(self, user_id: UUID):
        try:
            return await self.user_db.delete({"_id": str(user_id)})
        except Exception as e:
            raise ValueError(f"Error deleting user: {str(e)}")



# ___________________________________Admin______________________________________________________

    async def create_admin(self, admin_data):
        admin = Admin(**admin_data)
        return await self.admin_db.add(admin)
    
    async def update_admin(self, admin_id: UUID, admin_data):
        return await self.admin_db.update(admin_id, admin_data)
    
    async def delete_admin(self, admin_id: UUID):
        try:
            return await self.admin_db.delete({"_id": str(admin_id)})
        except Exception as e:
            raise ValueError(f"Error deleting admin: {str(e)}")



# ___________________________________Spa______________________________________________________

    async def create_spa(self, spa_data):
        spa = Spa(**spa_data)
        return await self.spa_db.add(spa)
    
    async def update_spa(self, spa_id: UUID, spa_data):
        return await self.spa_db.update(spa_id, spa_data)
    
    async def delete_spa(self, spa_id: UUID):
        return await self.spa_db.delete({"_id": str(spa_id)})



# ___________________________________Service______________________________________________________

    async def create_service(self, service_data):
        service = Service(**service_data)
        return await self.service_db.add(service)
    
    async def update_service(self, service_id: UUID, service_data):
        return await self.service_db.update(service_id, service_data)
    
    async def delete_service(self, service_id: UUID):
        return await self.service_db.delete({"_id": str(service_id)})



# ___________________________________Booking______________________________________________________
    
    async def create_booking(self, booking_data):
        booking = Booking(**booking_data)
        return await self.booking_db.add(booking)
    
    async def get_booking_by_id(self, booking_id: UUID):
        return await self.booking_db.get_by_id(str(booking_id))
    
    async def get_all_bookings(self):
        return await self.booking_db.get_all()
    
    async def update_booking(self, booking_id: UUID, booking_data):
        return await self.booking_db.update(booking_id, booking_data)
    
    async def delete_booking(self, booking_id: UUID):
        return await self.booking_db.delete({"_id": str(booking_id)})



import asyncio
from uuid import uuid4
from app.services.facade import Facade

async def test_facade():
    facade = Facade()

    print("\n🔹 Test 1: Crear un usuario")
    user_data = {
        "id": uuid4(),
        "name": {"first_name": "John", "last_name": "Doe"},  # ✅ Corrección aquí
        "email": "john.doe@gmail.com",  # ✅ Email válido
        "hashed_password": "securepassword123"  # ✅ Clave correcta
    }
    user = await facade.create_user(user_data)
    print(f"✅ Usuario creado: {user}")

    print("\n🔹 Test 2: Obtener usuario por email")
    fetched_user = await facade.get_user_by_attribute("email", user_data["email"])
    print(f"✅ Usuario encontrado: {fetched_user}")

    print("\n🔹 Test 3: Obtener todos los usuarios")
    all_users = await facade.get_all_users()
    print(f"✅ Lista de usuarios: {all_users}")

    print("\n🔹 Test 4: Actualizar usuario")
    updated_data = {"name": {"first_name": "Johnny", "last_name": "Doe"}}  # ✅ Corrección aquí también
    updated_user = await facade.update_user(user_data["id"], updated_data)
    print(f"✅ Usuario actualizado: {updated_user}")

    print("\n🔹 Test 5: Eliminar usuario")
    result = await facade.delete_user(user_data["id"])
    print(f"✅ Usuario eliminado: {result}")

if __name__ == "__main__":
    asyncio.run(test_facade())
