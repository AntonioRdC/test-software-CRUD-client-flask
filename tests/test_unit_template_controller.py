import logging
from flask_testing import TestCase
from app import app, db
from models.client_model import Client


class TestClientController(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        return app

    def setUp(self):
        with app.app_context():
            db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_client_get(self):
        response = self.client.get('/client/new')
        self.assertEqual(response.status_code, 200)

    def test_create_client_post(self):
        response = self.client.post('/client/new', data={
            'name': 'Test Client',
            'cpf': '12345678909',
            'street': 'Test Street',
            'number': '100',
            'complement': 'Apt 101',
            'neighborhood': 'Test Neighborhood',
            'zip_code': '12345-678',
            'city': 'Test City',
            'state': 'TS',
            'phone': '123456789',
            'email': 'testclient@example.com'
        })
        self.assertEqual(response.status_code, 200)

        client = Client.query.filter_by(cpf='12345678909').first()
        self.assertIsNotNone(client)
        self.assertEqual(client.name, 'Test Client')

    def test_update_client_route(self):
        client = Client(
            name='Test Client',
            cpf='12345678909',
            street='Test Street',
            number='100',
            complement='Apt 101',
            neighborhood='Test Neighborhood',
            zip_code='12345-678',
            city='Test City',
            state='TS',
            phone='123456789',
            email='testclient@example.com'
        )
        db.session.add(client)
        db.session.commit()

        response = self.client.post(f'/client/update/{client.id}', data={
            'name': 'Updated Client',
            'cpf': '12345678909',
            'street': 'New Street',
            'number': '200',
            'complement': 'House',
            'neighborhood': 'New Neighborhood',
            'zip_code': '87654-321',
            'city': 'New City',
            'state': 'NV',
            'phone': '987654321',
            'email': 'updatedclient@example.com'
        })
        self.assertEqual(response.status_code, 302)

        updated_client = db.session.get(Client, client.id)
        self.assertIsNotNone(updated_client)
        self.assertEqual(updated_client.name, 'Updated Client')

    def test_delete_client_route(self):
        client = Client(
            name='Test Client',
            cpf='12345678909',
            street='Test Street',
            number='100',
            complement='Apt 101',
            neighborhood='Test Neighborhood',
            zip_code='12345-678',
            city='Test City',
            state='TS',
            phone='123456789',
            email='testclient@example.com'
        )
        db.session.add(client)
        db.session.commit()

        response = self.client.get(f'/client/delete/{client.id}')
        self.assertEqual(response.status_code, 302)

        deleted_client = db.session.get(Client, client.id)
        self.assertIsNone(deleted_client)


if __name__ == '__main__':
    import unittest
    unittest.main()
