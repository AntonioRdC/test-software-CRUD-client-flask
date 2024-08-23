"""
Eneas Silva de Queiroz - pt-BR, UTF-8 - 22-08-2024
Manipulando o banco de dados sqlite3 
# test_template_client_controller.py
"""

import logging
from flask import url_for
from flask_testing import TestCase
from app import app, db
from models.client_model import Client

class TestClientController(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Ainda n\xc3\xa3o existem clientes cadastrados...", response.data)

    def test_create_client_get(self):
        response = self.client.get('/client/new')
        self.assertEqual(response.status_code, 200)

    def test_create_client_post(self):
        response = self.client.post('/client/new', data={
            'name': 'Cliente Teste',
            'cpf': '12345678909',
            'street': 'Rua Teste',
            'number': '100',
            'complement': 'Apto 101',
            'neighborhood': 'Bairro Teste',
            'zip_code': '12345-678',
            'city': 'Cidade Teste',
            'state': 'TS',
            'phone': '123456789',
            'email': 'clienteteste@example.com'
        })

        # Verifica se houve redirecionamento
        self.assertEqual(response.status_code, 302)  # Esperando redirecionamento após POST

        # Verifica se o cliente foi criado com sucesso
        client = Client.query.filter_by(cpf='12345678909').first()
        self.assertIsNotNone(client)
        self.assertEqual(client.name, 'Cliente Teste')

    def test_update_client_route(self):
        # Primeiro adicionamos um cliente para depois tentar atualizar
        client = Client(
            name='Cliente Teste',
            cpf='12345678909',
            street='Rua Teste',
            number='100',
            complement='Apto 101',
            neighborhood='Bairro Teste',
            zip_code='12345-678',
            city='Cidade Teste',
            state='TS',
            phone='123456789',
            email='clienteteste@example.com'
        )
        db.session.add(client)
        db.session.commit()

        # Atualiza o cliente
        response = self.client.post(f'/client/update/{client.id}', data={
            'name': 'Cliente Atualizado',
            'cpf': '12345678909',
            'street': 'Rua Nova',
            'number': '200',
            'complement': 'Casa',
            'neighborhood': 'Bairro Novo',
            'zip_code': '87654-321',
            'city': 'Cidade Nova',
            'state': 'NV',
            'phone': '987654321',
            'email': 'clienteatualizado@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Esperando redirecionamento após atualização

        # Verifica se o cliente foi atualizado
        updated_client = Client.query.get(client.id)
        self.assertIsNotNone(updated_client)
        self.assertEqual(updated_client.name, 'Cliente Atualizado')

    def test_delete_client_route(self):
        # Primeiro adicionamos um cliente para depois tentar deletar
        client = Client(
            name='Cliente Teste',
            cpf='12345678909',
            street='Rua Teste',
            number='100',
            complement='Apto 101',
            neighborhood='Bairro Teste',
            zip_code='12345-678',
            city='Cidade Teste',
            state='TS',
            phone='123456789',
            email='clienteteste@example.com'
        )
        db.session.add(client)
        db.session.commit()

        # Deleta o cliente
        response = self.client.get(f'/client/delete/{client.id}')
        self.assertEqual(response.status_code, 302)  # Esperando redirecionamento após deleção

        # Verifica se o cliente foi deletado
        deleted_client = Client.query.get(client.id)
        self.assertIsNone(deleted_client)

if __name__ == '__main__':
    import unittest
    unittest.main()
