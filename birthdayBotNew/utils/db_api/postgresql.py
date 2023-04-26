from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config

class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_birthday(self):
        sql = """
        CREATE TABLE IF NOT EXISTS birthday (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        Year INTEGER NOT NULL,
        Month INTEGER NOT NULL,
        Day INTEGER NOT NULL,
        telegram_id BIGINT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())


    async def add_birthday(self, full_name, Year, Month, Day, telegram_id):
        sql = "INSERT INTO Birthday (full_name, Year, Month, Day, telegram_id) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, full_name, Year, Month, Day, telegram_id, fetchrow=True)

    async def sent_date(self, Mont, Day):
        sql = "SELECT * FROM birthday WHERE EXTRACT(MONTH FROM Month) = %s AND EXTRACT(DAY FROM your_date_column) = %s"
        return await self.execute(sql, Mont, Day)

    async def select_all_birthday(self):
        sql = "SELECT * FROM birthday"
        return await self.execute(sql, fetch=True)

    async def select_birthday(self, **kwargs):
        sql = "SELECT * FROM birthday WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_birthday(self):
        sql = "SELECT COUNT(*) FROM birthday"
        return await self.execute(sql, fetchval=True)

    async def update_birthday_Year(self, Year, telegram_id):
        sql = "UPDATE birthday SET Year=$1 WHERE telegram_id=$2"
        return await self.execute(sql, Year, telegram_id, execute=True)

    async def delete_birthday(self):
        await self.execute("DELETE FROM birthday WHERE TRUE", execute=True)

    async def drop_birthday(self):
        await self.execute("DROP TABLE birthday", execute=True)

    async def my_birthday(self, tg_id):
        sql = "SELECT * FROM birthday WHERE telegram_id=$1 "
        return await self.execute(sql, tg_id, fetch=True)

    async def happy_Month_Day(self, Month, Day):
        sql = f"SELECT * FROM birthday WHERE Month = $1 AND Day = $2"
        return await self.execute(sql, Month, Day, fetch=True)

    async def delete_db_name(self, del_name):
        sql = "DELETE FROM birthday WHERE full_name=$1"
        return await self.execute(sql, del_name, execute=True)


    async def happy_day(self, t_month, t_day):
        sql = "SELECT * FROM birthday WHERE Month = $1 AND Day = $2"
        return await self.execute(sql, t_month, t_day, fetchval=True)


    ###first
    async def create_table_FIO_state(self):
        sql = """
        CREATE TABLE IF NOT EXISTS FIO_state (
        id SERIAL PRIMARY KEY,
        firstname VARCHAR(255) NOT NULL,
        surname varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_FIO_state(self, firstname, surname, telegram_id):
        sql = "INSERT INTO FIO_state (firstname, surname, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, firstname, surname, telegram_id, fetchrow=True)

    async def select_all_FIO_state(self):
        sql = "SELECT * FROM FIO_state"
        return await self.execute(sql, fetch=True)

    # async def id_check_FIO_state(self, tg_id):
    #     sql = "SELECT id FROM FIO_state"
    #     return await self.execute(sql, tg_id, fetch=True)

    async def select_FIO_state(self, **kwargs):
        sql = "SELECT * FROM FIO_state WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_FIO_state(self):
        sql = "SELECT COUNT(*) FROM FIO_state"
        return await self.execute(sql, fetchval=True)

    async def update_user_FIO_state_username(self, surname, telegram_id):
        sql = "UPDATE FIO_state SET surname=$1 WHERE telegram_id=$2"
        return await self.execute(sql, surname, telegram_id, execute=True)

    async def delete_FIO_state(self):
        await self.execute("DELETE FROM FIO_state WHERE TRUE", fetchrow=True)

    async def drop_FIO_state(self):
        await self.execute("DROP TABLE FIO_state", execute=True)

    async def my_bithday_see(self, tg_id):
        sql = "SELECT * FROM FIO_state WHERE telegram_id=$1"
        return await self.execute(sql, tg_id, fetch=True)
