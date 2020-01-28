from flask import Blueprint, request, jsonify

beer = Blueprint("beer", __name__)


@beer.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    print(data)
    code = data["code"]
    if code == "0820":
        response = {"result": "success", "name": "Michael Kulinski", "initials": "MAK"}
    else:
        response = {"result": "failure"}

    return jsonify(response)


@beer.route("/upc", methods=["POST"])
def upc():
    data = request.get_json()
    print(data)

    upc = data["upc"]
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

    return jsonify({"result": "success"})


@beer.route("/charge", methods=["POST"])
def charge():
    data = request.get_json()
    print("Checking out a beer")
    print(data)

    upc = data["upc"]
    if upc == "01803127":
        response = {"result": "success", "name": "Natural Light"}
    else:
        response = {"result": "failure"}

    return jsonify(response)
