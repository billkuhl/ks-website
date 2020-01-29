from web.models import db
from datetime import datetime
import enum


class BeerType(enum.Enum):
    IPA = "IPA"
    STOUT = "Stout"
    PORTER = "Porter"
    PALE_ALE = "Pale Ale"
    ALE = "Ale"
    WHEAT = "Wheat"
    AMBER = "Amber"
    LAGER = "Lager"
    BARLEY_WINE = "Barley Wine"
    SOUR = "Sour"
    BOCK = "Bock"
    PILSNER = "Pilsner"
    CIDER = "Cider"

    def __str__(self):
        return str(self.value)


class Beer(db.Model):
    __tablename__ = "beer"

    # Identification information
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    upc = db.Column(db.String(64), unique=True)
    beer_type = db.Column(db.Enum(BeerType))

    # Quantity information
    current_stock = db.Column(db.Integer, default=0)
    checkout_total = db.Column(db.Integer, default=0)
    purchase_total = db.Column(db.Integer, default=0)
    last_added = db.Column(db.DateTime, default=datetime.now())

    __table_args__ = (
        db.CheckConstraint(current_stock >= 0, name="check_stock_positive"),
        {},
    )

