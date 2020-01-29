from flask import Blueprint, request, jsonify
from web.models.beer import Beer, BeerType
from web.models.user import User
from web.models import db
from datetime import datetime

beer = Blueprint("beer", __name__)


@beer.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    print(data)
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


@beer.route("/upc", methods=["POST"])
def upc():
    data = request.get_json()
    print(data)

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


@beer.route("/add", methods=["POST"])
def add():
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

        beer_type = (
            BeerType(data["beer_type"]) if "beer_type" in data else BeerType.LAGER
        )

        # Create new kind of beer for database
        beer = Beer(
            name=name,
            upc=upc,
            beer_type=beer_type,
            current_stock=quantity,
            checkout_total=0,
            purchase_total=quantity,
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


@beer.route("/charge", methods=["POST"])
def charge():
    data = request.get_json()
    print("Checking out a beer")
    print(data)

    if "upc" in data and "beer_code" in data:
        upc = data["upc"]
        beer_code = data["beer_code"]
    else:
        return jsonify({"result": "failure"})

    # Lookup brother via beer_code
    # Lookup beer via upc code
    # if either of those fail
    #   return  failure
    # else
    #   create a new beer transaction
    #   current_stock -= 1
    #   return success and name of beer checked out

    if upc == "01803127":
        response = {"result": "success", "name": "Natural Light"}
    else:
        response = {"result": "failure"}

    return jsonify(response)
