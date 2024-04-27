from fastapi import HTTPException
import asyncpg
import os

class StoreService:
    @staticmethod
    async def isHadById(table: str,varia: int) -> bool:
        conn = await asyncpg.connect(
            user='admin',
            password='0000',
            database='magic-store',
            host='localhost',
            port='5432'
        )

        try:
            query = f"SELECT 1 FROM {table} WHERE id = $1;"
            result = await conn.fetch(query, varia)
            return len(result) > 0
        finally:
            await conn.close()

    @staticmethod
    async def isHadByName(
        table: str,
        varia: str
    ) -> bool:
        conn = await asyncpg.connect(
            user='admin',
            password='0000',
            database='magic-store',
            host='localhost',
            port='5432'
        )

        try:
            query = f"SELECT 1 FROM {table} WHERE name = $1;"
            result = await conn.fetch(query, varia)
            return len(result) > 0
        finally:
            await conn.close()
