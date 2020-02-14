from flask import Blueprint, request, jsonify
from web.models.beer import Beer, BeerType, BeerTransaction
from web.models.user import User
from web.models import db
from datetime import datetime

beer = Blueprint("beer", __name__)


@beer.route("/upc", methods=["POST"])
def upc():
    """
    Checks to see if the upc has already been added in the past
    If so, return information about that beer
    Otherwise, return an error
    """
    data = request.get_json()

    if "upc" in data:
        upc = data["upc"]
    else:
        return jsonify({"result": "failure"})

    # Check if upc code exists in database
    beer = Beer.query.filter_by(upc=upc).first()
    if beer is None:
        return jsonify({"result": "failure"})
    else:
        return jsonify(
            {
                "result": "success",
                "beer_id": beer.id,
                "name": beer.name,
                "beer_type": str(beer.beer_type),
            }
        )


@beer.route("/checkin", methods=["POST"])
def checkin():
    """
    Checks new beers into the beer fridge
    Creates a new beer row if upc doesn't exist in the database
    Otherwise, updates the quantities for beers that have already been checked in before
    """
    data = request.get_json()

    if "beer_id" in data:
        beer_id = data["beer_id"]

        quantity = data["quantity"] if "quantity" in data else 0
        # Lookup beer_id in database and get its data
        beer = Beer.query.filter_by(id=beer_id).first()
        if beer is None:
            return jsonify({"result": "failure", "fail": "Beer id does not exist"})
        else:
            beer.current_stock += quantity
            beer.purchase_total += quantity
            beer.last_added = datetime.now()

            db.session.add(beer)
            db.session.commit()
            print("Beer added")
            print(data)
            return jsonify({"result": "success"})

    elif "name" in data:
        name = data["name"]
        quantity = data["quantity"] if "quantity" in data else 0
        upc = data["upc"]

        if "beer_type" not in data or data["beer_type"] == "None":
            beer_type = BeerType.LAGER
        else:
            beer_type = BeerType(data["beer_type"])

        # Create new kind of beer for database
        beer = Beer(
            name=name,
            upc=upc,
            beer_type=beer_type,
            current_stock=quantity,
            checkout_total=0,
            purchase_total=quantity,
            last_added=datetime.now(),
        )

        try:
            db.session.add(beer)
            db.session.commit()
            print("Beer added")
            print(data)
            return jsonify({"result": "success"})
        except Exception:
            print("Tried to add a beer with a UPC that already exists")
            return jsonify({"result": "failure", "fail": "Upc collision"})

    return jsonify({"result": "failure", "fail": "end"})


@beer.route("/login", methods=["POST"])
def login():
    """
    Tries to find a brother with the given beer_code
    If found, returns their name and initials
    If not, fails since that person doesn't exist
    """
    data = request.get_json()

    if "beer_code" in data:
        beer_code = data["beer_code"]
    else:
        return jsonify({"result": "failure"})

    # Make sure that the person with this beer_code exists
    brother = User.query.filter_by(beer_code=beer_code).first()
    if brother is None:
        return jsonify({"result": "failure"})
    else:
        # TODO log that this person opened the fridge
        return jsonify(
            {
                "result": "success",
                "name": brother.full_name(),
                "initials": brother.initials(),
            }
        )


@beer.route("/checkout", methods=["POST"])
def checkout():
    data = request.get_json()
    print("Checking out a beer")
    print(data)

    if "upc" in data and "beer_code" in data:
        upc = data["upc"]
        beer_code = data["beer_code"]
    else:
        return jsonify({"result": "failure"})

    # Make sure that the person with this beer_code exists
    brother = User.query.filter_by(beer_code=beer_code).first()
    beer = Beer.query.filter_by(upc=upc).first()
    if brother is None or beer is None:
        return jsonify({"result": "failure"})
    else:
        try:
            beer.current_stock -= 1
            beer.checkout_total += 1
            db.session.add(beer)

            transaction = BeerTransaction(
                brother_id=brother.id, beer_id=beer.id, date=datetime.now()
            )
            db.session.add(transaction)

            db.session.commit()
            return jsonify({"result": "success", "name": beer.name})
        except Exception:
            return jsonify(
                {
                    "result": "failure",
                    "fail": "Tried to check out more beers than available",
                }
            )


# Super basic example of how to query foreign keys. Useful for charging brothers
@beer.route("/query", methods=["GET", "POST"])
def query():
    transactions_by_beer = Beer.query.get(2).beer_transactions
    transactions_by_brother = User.query.get(1).beer_transactions

    brother = BeerTransaction.query.get(3).brother
    beer = BeerTransaction.query.get(2).beer
    return jsonify(
        transactions_by_beer=[str(t) for t in transactions_by_beer],
        transactions_by_brother=[str(t) for t in transactions_by_brother],
        brother=str(brother),
        beer=str(beer),
    )
