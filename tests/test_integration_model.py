import unittest
from flask_testing import TestCase
from src.app import app, db
from src.models.client_model import Client


class TestIntegrationClientModel(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        return app

    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_integration_new_to_index(self):
        self.client.post('/client/new', data={
            'name': 'Cliente A',
            'cpf': '12345678909',
            'street': 'Rua A',
            'number': '100',
            'complement': 'Apto 101',
            'neighborhood': 'Bairro A',
            'zip_code': '12345-678',
            'city': 'Cidade A',
            'state': 'RO',
            'phone': '123456789',
            'email': 'clientea@example.com'
        })

        response = self.client.get('/')

        self.assertIn(b'Cliente A', response.data)

    def test_integration_delete_to_index(self):
        client = Client(
            name='Cliente B', cpf='10987654321', street='Rua B', number=200,
            complement='Casa 2', neighborhood='Bairro B', zip_code='87654-321',
            city='Cidade B', state='Estado B', phone='987654321', email='clienteb@example.com'
        )

        with self.app.app_context():
            db.session.add(client)
            db.session.commit()

            cliente_id = client.id

            self.client.get(f'/client/delete/{cliente_id}')
            response = self.client.get('/')
            self.assertNotIn(b'Cliente B', response.data)


if __name__ == '__main__':
    unittest.main()
