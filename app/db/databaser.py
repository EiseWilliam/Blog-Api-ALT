import logging

from motor.motor_asyncio import AsyncIOMotorClient


class DataBase:
    client: AsyncIOMotorClient


db = DataBase()

async def connect_to_mongo():
    logging.info("Connecting to database...")
    
                                   
    logging.info("Database connected!")


import logging

async def close_mongo_connection():
    logging.info("Closing database connection...")
    db.client.close()
    logging.info("Database connection closed!")
    
    
from motor.motor_asyncio import AsyncIOMotorClient

async def get_database() -> AsyncIOMotorClient:
    return db.client
