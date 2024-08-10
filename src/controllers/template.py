from flask import Blueprint, request, render_template, redirect, url_for
from sqlalchemy.exc import IntegrityError
from models.client_model import Client
from database.database import db

template = Blueprint('template', __name__)


@template.route('/')
def index():
    clients = db.session.execute(
        db.select(Client).order_by(Client.name)).scalars().all()
    return render_template('new.html', clients=clients)


@template.route('/client/new', methods=['GET', 'POST'])
def create_client():
    if request.method == 'POST':
        client = Client(
            name=request.form.get("name"),
            cpf=request.form.get("cpf"),
            street=request.form.get("street"),
            number=request.form.get("number"),
            complement=request.form.get("complement"),
            neighborhood=request.form.get("neighborhood"),
            zip_code=request.form.get("zip_code"),
            city=request.form.get("city"),
            state=request.form.get("state"),
            phone=request.form.get("phone"),
            email=request.form.get("email"),
        )

        db.session.add(client)
        db.session.commit()

    clients = db.session.execute(
        db.select(Client).order_by(Client.name)).scalars().all()
    return render_template('new.html', clients=clients)


@template.route('/client/update/<int:id>', methods=['GET', 'POST'])
def update_client(id):
    client = db.get_or_404(Client, id)
    if request.method == 'POST':
        client = Client(
            name=request.form.get("name"),
            cpf=request.form.get("cpf"),
            street=request.form.get("street"),
            number=request.form.get("number"),
            complement=request.form.get("complement"),
            neighborhood=request.form.get("neighborhood"),
            zip_code=request.form.get("zip_code"),
            city=request.form.get("city"),
            state=request.form.get("state"),
            phone=request.form.get("phone"),
            email=request.form.get("email"),
        )

        db.session.commit()
        return redirect(url_for('template.index'))
    return render_template('update.html', client=client)


@template.route('/client/delete/<id>', methods=['GET'])
def delete_client(id):
    client = db.get_or_404(Client, id)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('template.index'))
