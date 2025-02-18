from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
import pendulum
from datetime import datetime, timezone

class BaseEntity(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


    def update_timestamp(self):
        "Updates the updated_at field with the current date in UTC"
        
        self.updated_at = pendulum.now("UTC").to_iso8601_string()

    def to_timezone(self, timezone: str):
        "Convert timestamps to a specific time zone"

        return {
            "id": self.id,
            "created_at": pendulum.parse(self.created_at).in_timezone(timezone).to_iso8601_string(),
            "updated_at": pendulum.parse(self.updated_at).in_timezone(timezone).to_iso8601_string(),
        }
    
    async def save(self, collection: AsyncIOMotorCollection):
        """Save or update the document in MongoDB"""

        self.updated_at = pendulum.now("UTC").to_iso8601_string()
        data = self.model_dump()
        await collection.update_one({"id": self.id}, {"$set": data}, upsert=True)


    async def update(self, collection: AsyncIOMotorCollection, data: dict):
        """Update specific fields and save"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        await self.save(collection)