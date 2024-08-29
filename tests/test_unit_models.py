from flask_testing import TestCase
from src.app import app, db
from src.models.client_model import Client


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
            name='Test Client',
            cpf='12345678909',
            street='Test Street',
            number='100',
            complement='Apt 101',
            neighborhood='Test Neighborhood',
            zip_code='12345-678',
            city='Test City',
            state='SP',
            phone='123456789',
            email='client@test.com'
        )
        db.session.add(client)
        db.session.commit()
        self.assertEqual(Client.query.count(), 1)

    def test_get_client(self):
        client = Client(
            name='Test Client',
            cpf='12345678909',
            street='Test Street',
            number='100',
            complement='Apt 101',
            neighborhood='Test Neighborhood',
            zip_code='12345-678',
            city='Test City',
            state='SP',
            phone='123456789',
            email='client@test.com'
        )
        db.session.add(client)
        db.session.commit()
        client_query = db.session.get(Client, client.id)
        self.assertEqual(client_query.id, client.id)

    def test_update_client(self):
        client = Client(
            name='Test Client',
            cpf='12345678909',
            street='Test Street',
            number='100',
            complement='Apt 101',
            neighborhood='Test Neighborhood',
            zip_code='12345-678',
            city='Test City',
            state='SP',
            phone='123456789',
            email='client@test.com'
        )
        db.session.add(client)
        db.session.commit()

        client.name = 'Updated Client'
        client.email = 'updatedclient@test.com'
        db.session.commit()

        updated_client = db.session.get(Client, client.id)
        self.assertEqual(updated_client.name, 'Updated Client')
        self.assertEqual(updated_client.email, 'updatedclient@test.com')

    def test_delete_client(self):
        client = Client(
            name='Test Client',
            cpf='12345678909',
            street='Test Street',
            number='100',
            complement='Apt 101',
            neighborhood='Test Neighborhood',
            zip_code='12345-678',
            city='Test City',
            state='SP',
            phone='123456789',
            email='client@test.com'
        )
        db.session.add(client)
        db.session.commit()

        db.session.delete(client)
        db.session.commit()

        deleted_client = db.session.get(Client, client.id)
        self.assertIsNone(deleted_client)

    def test_get_all_clients(self):
        client1 = Client(
            name='Test Client 1',
            cpf='12345678909',
            street='Test Street',
            number='100',
            complement='Apt 101',
            neighborhood='Test Neighborhood',
            zip_code='12345-678',
            city='Test City',
            state='SP',
            phone='123456789',
            email='client1@test.com'
        )
        client2 = Client(
            name='Test Client 2',
            cpf='10987654321',
            street='Test Street 2',
            number='200',
            complement='House 2',
            neighborhood='Test Neighborhood 2',
            zip_code='87654-321',
            city='Test City 2',
            state='RJ',
            phone='987654321',
            email='client2@test.com'
        )
        db.session.add(client1)
        db.session.add(client2)
        db.session.commit()

        all_clients = Client.query.all()
        self.assertEqual(len(all_clients), 2)


if __name__ == '__main__':
    import unittest
    unittest.main()
