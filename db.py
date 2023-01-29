import asyncio
import aiosqlite as aiosqlite
from functools import lru_cache
alarm = False

#@lru_cache
async def get_info_from_db():
    async with aiosqlite.connect('sql_app.db') as db:
        data = await db.execute_fetchall("SELECT * FROM people")
        await db.commit()
        return print(data)


async def check_new_peoples_db():
    async with aiosqlite.connect('sql_app.db') as db:
        if await db.execute_fetchall("SELECT * FROM people") != await get_info_from_db():
            return alarm == True, print('alarm')
        #return print('нет изменений')



if __name__ == '__main__':l
    while alarm == False:
        #asyncio.run(get_info_from_db())
        asyncio.run(check_new_peoples_db())