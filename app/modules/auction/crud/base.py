from app.database.postgresql.crud import CRUD
from app.modules.auction.crud.models import Auction


class AuctionCRUD(CRUD[Auction]):
    table = Auction
