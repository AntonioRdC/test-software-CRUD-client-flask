from flask import Blueprint, request, jsonify, abort
from sqlalchemy.exc import IntegrityError
from models.client_model import Client
from database.database import db
from services.via_cep import get_address

api = Blueprint('api', __name__)


@api.route("/api/clients", methods=["GET"])
def get_clients():
    clients = db.session.execute(
        db.select(Client).order_by(Client.name)).scalars().all()
    return jsonify([{
        "id": client.id, "name": client.name, "cpf": client.cpf, "street": client.street,
        "number": client.number, "complement": client.complement, "neighborhood": client.neighborhood,
        "zip_code": client.zip_code, "city": client.city, "state": client.state, "phone": client.phone,
        "email": client.email
    } for client in clients])


@api.route("/api/clients", methods=["POST"])
def create_client():
    if not request.json or not all(k in request.json for k in ("name", "cpf", "street", "number", "neighborhood", "zip_code", "city", "state", "phone", "email")):
        abort(400)
    try:
        client = Client(
            name=request.json["name"],
            cpf=request.json["cpf"],
            street=request.json["street"],
            number=request.json["number"],
            complement=request.json.get("complement", ""),
            neighborhood=request.json["neighborhood"],
            zip_code=request.json["zip_code"],
            city=request.json["city"],
            state=request.json["state"],
            phone=request.json["phone"],
            email=request.json["email"],
        )
        print(client.name, client.cpf, client.street, client.number, client.complement,
              client.neighborhood, client.zip_code, client.city, client.state, client.phone, client.email)
        db.session.add(client)
        db.session.commit()
        return jsonify({
            "id": client.id, "name": client.name, "cpf": client.cpf, "street": client.street,
            "number": client.number, "complement": client.complement, "neighborhood": client.neighborhood,
            "zip_code": client.zip_code, "city": client.city, "state": client.state, "phone": client.phone,
            "email": client.email
        }), 201
    except IntegrityError as e:
        return jsonify({"message": "Cpf cadastrado, já existe"}), 409
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Ocorreu um erro inesperado."}), 500


@api.route("/api/clients/<int:id>", methods=["GET"])
def get_client(id):
    client = db.get_or_404(Client, id)
    return jsonify({
        "id": client.id, "name": client.name, "cpf": client.cpf, "street": client.street,
        "number": client.number, "complement": client.complement, "neighborhood": client.neighborhood,
        "zip_code": client.zip_code, "city": client.city, "state": client.state, "phone": client.phone,
        "email": client.email
    })


@api.route("/api/clients/<int:id>", methods=["PUT"])
def update_client(id):
    client = db.get_or_404(Client, id)
    if not request.json:
        abort(400)

    try:
        client.name = request.json.get("name", client.name)
        client.cpf = request.json.get("cpf", client.cpf)
        client.street = request.json.get("street", client.street)
        client.number = request.json.get("number", client.number)
        client.complement = request.json.get("complement", client.complement)
        client.neighborhood = request.json.get(
            "neighborhood", client.neighborhood)
        client.zip_code = request.json.get("zip_code", client.zip_code)
        client.city = request.json.get("city", client.city)
        client.state = request.json.get("state", client.state)
        client.phone = request.json.get("phone", client.phone)
        client.email = request.json.get("email", client.email)

        db.session.commit()
        return jsonify({
            "id": client.id, "name": client.name, "cpf": client.cpf, "street": client.street,
            "number": client.number, "complement": client.complement, "neighborhood": client.neighborhood,
            "zip_code": client.zip_code, "city": client.city, "state": client.state, "phone": client.phone,
            "email": client.email
        })
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@api.route("/api/clients/<int:id>", methods=["DELETE"])
def delete_client(id):
    client = db.get_or_404(Client, id)
    db.session.delete(client)
    db.session.commit()
    return jsonify({}), 204


@api.route('/api/fetch_address/<cep>', methods=['GET'])
def fetch_address(cep):
    address = get_address(cep)
    if address:
        return jsonify(address)
    return jsonify({'error': 'CEP not found'}), 404
