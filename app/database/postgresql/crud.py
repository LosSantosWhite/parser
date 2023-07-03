from typing import Generic, Type, TypeVar

from sqlalchemy import select, update, TextClause
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.postgresql.base import Base

Table = TypeVar("Table", bound=Base)


class CRUD(Generic[Table]):
    table: Type[Table]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id_: str) -> Table | None:
        return await self.session.get(self.table, id_)

    async def insert(self, data: dict, **kwargs) -> Table:
        instance = self.table(**data, **kwargs)

        self.session.add(instance=instance)
        await self.session.flush()
        await self.session.refresh(instance=instance)

        return instance

    async def select(self, *filters, order_by: TextClause = None) -> Table:
        stmt = select(self.table).where(*filters)

        if order_by:
            stmt = stmt.order_by(*order_by)
        result = await self.session.execute(stmt)
        return result

    async def update(self, data: dict, id_: str) -> Table:
        stmt = update(self.table).where(self.table.obj_id == id_).values(**data)
        result = await self.session.execute(stmt)
        return result
