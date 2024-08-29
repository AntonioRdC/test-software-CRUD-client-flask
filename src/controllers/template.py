from flask import Blueprint, request, render_template, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from models.client_model import Client
from validators.client_validator import validate_address, validate_cpf, validate_email, validate_name
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
        try:
            name = validate_name(request.form.get("name"))
            cpf = validate_cpf(request.form.get("cpf"))
            street, number, complement, neighborhood, zip_code, city, state = validate_address(
                request.form.get("street"),
                request.form.get("number"),
                request.form.get("complement"),
                request.form.get("neighborhood"),
                request.form.get("zip_code"),
                request.form.get("city"),
                request.form.get("state")
            )
            email = validate_email(request.form.get("email"))

            client = Client(
                name=name,
                cpf=cpf,
                street=street,
                number=number,
                complement=complement,
                neighborhood=neighborhood,
                zip_code=zip_code,
                city=city,
                state=state,
                phone=request.form.get("phone"),
                email=email,
            )
            db.session.add(client)
            db.session.commit()
            flash('Cliente criado com sucesso!', 'success')
        except ValueError as e:
            flash(str(e), 'error')
        except IntegrityError as e:
            db.session.rollback()
            flash('Erro de integridade. Cliente já existe.', 'error')
        except Exception as e:
            flash('Ocorreu um erro inesperado.', 'error')

    clients = db.session.execute(
        db.select(Client).order_by(Client.name)).scalars().all()
    return render_template('new.html', clients=clients)


@template.route('/client/update/<int:id>', methods=['GET', 'POST'])
def update_client(id):
    client = db.get_or_404(Client, id)
    if request.method == 'POST':
        try:
            client.name = validate_name(request.form.get("name"))
            client.cpf = validate_cpf(request.form.get("cpf"))
            client.street, client.number, client.complement, client.neighborhood, client.zip_code, client.city, client.state = validate_address(
                request.form.get("street"),
                request.form.get("number"),
                request.form.get("complement"),
                request.form.get("neighborhood"),
                request.form.get("zip_code"),
                request.form.get("city"),
                request.form.get("state")
            )
            client.email = validate_email(request.form.get("email"))
            client.phone = request.form.get("phone")

            db.session.add(client)
            db.session.commit()
            flash('Cliente atualizado com sucesso!', 'success')
            return redirect(url_for('template.index'))
        except ValueError as e:
            flash(str(e), 'error')
        except IntegrityError as e:
            db.session.rollback()
            flash('Erro de integridade. Atualização falhou.', 'error')
        except Exception as e:
            flash('Ocorreu um erro inesperado.', 'error')

    return render_template('update.html', client=client)


@template.route('/client/delete/<id>', methods=['GET'])
def delete_client(id):
    try:
        client = db.get_or_404(Client, id)
        db.session.delete(client)
        db.session.commit()
        flash('Cliente deletado com sucesso!', 'success')
    except Exception as e:
        flash('Ocorreu um erro ao deletar o cliente.', 'error')

    return redirect(url_for('template.index'))
