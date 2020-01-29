from flask import Blueprint, request, jsonify
from web.models.beer import Beer, BeerType
from web.models import db

beer = Blueprint("beer", __name__)


@beer.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    print(data)
    if "brother_code" in data:
        brother_code = data["brother_code"]
    else:
        return jsonify({"result": "failure"})

    # Lookup if brother code in database
    # If not, then return failure
    # Else, log that this brother opened the fridge
    #   return {"result": "success", "name": "Michael Kulinski", "initials": "MAK"}

    if brother_code == "0820":
        response = {"result": "success", "name": "Michael Kulinski", "initials": "MAK"}
    else:
        response = {"result": "failure"}

    return jsonify(response)


@beer.route("/upc", methods=["POST"])
def upc():
    data = request.get_json()
    print(data)

    if "upc" in data:
        upc = data["upc"]
    else:
        return jsonify({"result": "failure"})

    # Check if upc code exists in database
    # If not, return failure
    # Else,
    #   return {"result": "success","beer_id": beer.pk,"name": beer.name,"type": beer.get_beer_type_display(),"total_consumed": beer.checkout_total,}

    if upc == "01803127":
        response = {
            "result": "success",
            "beer_id": "1",
            "name": "Natural Light",
            "type": "Lager",
            "total_consumed": "420",
        }
    else:
        response = {"result": "failure"}

    return jsonify(response)


@beer.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    print("Beer added")
    print(data)

    if "beer_id" in data:
        beer_id = data["beer_id"]

        quantity = data["quantity"] if "quantity" in data else 0
        # Lookup beer_id in database and get its data
        beer = Beer.query.filter_by(id=beer_id).first()
        if beer is None:
            return jsonify({"result": "failure"})
        else:
            beer.current_stock += quantity
            beer.purchase_total += quantity

            db.session.add(beer)
            db.session.commit()
            return jsonify({"result": "success"})

    elif "name" in data:
        print("Got into correct branch")
        name = data["name"]
        quantity = data["quantity"] if "quantity" in data else 0
        upc = data["upc"]
        beer_type = data["upc"] if "beer_type" in data else BeerType.LAGER

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
