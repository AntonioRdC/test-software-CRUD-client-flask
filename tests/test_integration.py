from flask_testing import TestCase
from flask import url_for
from src.app import app, db
from src.models.client_model import Client


class TestIntegration(TestCase):

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

    def test_index_page_with_clients(self):
        client1 = Client(
            name='Cliente A', cpf='12345678901', street='Rua A', number=100,
            complement='Apto 101', neighborhood='Bairro A', zip_code='12345-678',
            city='Cidade A', state='Estado A', phone='123456789', email='clientea@example.com'
        )
        client2 = Client(
            name='Cliente B', cpf='10987654321', street='Rua B', number=200,
            complement='Casa 2', neighborhood='Bairro B', zip_code='87654-321',
            city='Cidade B', state='Estado B', phone='987654321', email='clienteb@example.com'
        )

        db.session.add(client1)
        db.session.add(client2)
        db.session.commit()

        response = self.client.get(url_for('template.index'))

        self.assert200(response)
        self.assertIn(b'Cliente A', response.data)
        self.assertIn(b'Cliente B', response.data)
        self.assertIn(b'12345678901', response.data)
        self.assertIn(b'10987654321', response.data)

    def test_index_page_without_clients(self):
        response = self.client.get(url_for('template.index'))

        self.assert200(response)


if __name__ == '__main__':
    import unittest
    unittest.main()
