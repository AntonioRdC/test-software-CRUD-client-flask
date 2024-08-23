"""
Eneas Silva de Queiroz - pt-BR, UTF-8 - 22-08-2024
Manipulando o banco de dados sqlite3 
# test_models.py
"""

from flask_testing import TestCase
from app import app, db  # Importa o app e o db diretamente
from models.client_model import Client  # Importa a classe Client

class TestClientModel(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        return app

    def setUp(self):
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_client(self):
        client = Client(
            name='Teste Cliente',
            cpf='12345678909',
            street='Rua Teste',
            number='100',
            complement='Apto 101',
            neighborhood='Bairro Teste',
            zip_code='12345-678',
            city='Cidade Teste',
            state='SP',
            phone='123456789',
            email='cliente@teste.com'
        )
        db.session.add(client)
        db.session.commit()
        self.assertEqual(Client.query.count(), 1)

    def test_get_client(self):
        client = Client(
            name='Teste Cliente',
            cpf='12345678909',
            street='Rua Teste',
            number='100',
            complement='Apto 101',
            neighborhood='Bairro Teste',
            zip_code='12345-678',
            city='Cidade Teste',
            state='SP',
            phone='123456789',
            email='cliente@teste.com'
        )
        db.session.add(client)
        db.session.commit()
        client_query = db.session.get(Client, client.id)
        self.assertEqual(client_query.id, client.id)

    def test_update_client(self):
        client = Client(
            name='Teste Cliente',
            cpf='12345678909',
            street='Rua Teste',
            number='100',
            complement='Apto 101',
            neighborhood='Bairro Teste',
            zip_code='12345-678',
            city='Cidade Teste',
            state='SP',
            phone='123456789',
            email='cliente@teste.com'
        )
        db.session.add(client)
        db.session.commit()

        client.name = 'Cliente Atualizado'
        client.email = 'clienteatualizado@teste.com'
        db.session.commit()

        client_atualizado = db.session.get(Client, client.id)
        self.assertEqual(client_atualizado.name, 'Cliente Atualizado')
        self.assertEqual(client_atualizado.email, 'clienteatualizado@teste.com')

    def test_delete_client(self):
        client = Client(
            name='Teste Cliente',
            cpf='12345678909',
            street='Rua Teste',
            number='100',
            complement='Apto 101',
            neighborhood='Bairro Teste',
            zip_code='12345-678',
            city='Cidade Teste',
            state='SP',
            phone='123456789',
            email='cliente@teste.com'
        )
        db.session.add(client)
        db.session.commit()

        db.session.delete(client)
        db.session.commit()

        client_deletado = db.session.get(Client, client.id)
        self.assertIsNone(client_deletado)

    def test_get_all_clients(self):
        client1 = Client(
            name='Teste Cliente 1',
            cpf='12345678909',
            street='Rua Teste',
            number='100',
            complement='Apto 101',
            neighborhood='Bairro Teste',
            zip_code='12345-678',
            city='Cidade Teste',
            state='SP',
            phone='123456789',
            email='cliente1@teste.com'
        )
        client2 = Client(
            name='Teste Cliente 2',
            cpf='10987654321',
            street='Rua Teste 2',
            number='200',
            complement='Casa 2',
            neighborhood='Bairro Teste 2',
            zip_code='87654-321',
            city='Cidade Teste 2',
            state='RJ',
            phone='987654321',
            email='cliente2@teste.com'
        )
        db.session.add(client1)
        db.session.add(client2)
        db.session.commit()

        todos_clients = Client.query.all()
        self.assertEqual(len(todos_clients), 2)

if __name__ == '__main__':
    import unittest
    unittest.main()
