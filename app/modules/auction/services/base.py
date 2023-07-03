from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.database.postgresql.decorators import transaction, duplicate
from app.modules.auction.crud.base import AuctionCRUD
from app.modules.auction.crud.models import Auction
from app.modules.auction.parser.base import ParserBase


class AuctionServise:
    def __init__(self, session: AsyncSession, url: str):
        self.session = session
        self.auction: AuctionCRUD = AuctionCRUD(session=session)
        self.parser: ParserBase = ParserBase(url)

    @transaction
    @duplicate("This auction already exists")
    async def create(self, schema: dict[str], _commit: bool = True) -> Auction:
        return await self.auction.insert(data=schema)

    async def update(
        self, id_: str, schema: dict[str], _commit: bool = True
    ) -> Auction:
        return await self.auction.update(data=schema, id_=id_)

    async def parse_info(self) -> list[dict]:
        return await self.parser.parse_info()

    async def main(self):
        objects = await self.parse_info()
        for obj in objects:
            try:
                await self.create(schema=obj, _commit=False)
            except IntegrityError:
                id_ = obj["obj_id"]
                await self.update(id_=id_, schema=obj)

        await self.session.commit()
