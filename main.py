import asyncio

from app.database.postgresql.base import SessionFactory
from app.modules.auction.services.base import AuctionServise


async def main():
    async with SessionFactory() as session:
        auction = AuctionServise(session, "https://nedradv.ru/nedradv/ru/auction")
        await auction.main()
        print("DONE")


asyncio.run(main())
