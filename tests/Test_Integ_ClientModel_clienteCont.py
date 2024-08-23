"""
Eneas Silva de Queiroz - pt-BR, UTF-8 - 22-08-2024
Manipulando o banco de dados sqlite3 
Test_Integ_ClientModel_clienteCont.py
"""

import unittest
from app import app
from database.database import db
from models.client_model import Client

class TestIntegrationClientModel(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_integration_novo_to_index(self):
        # Usando valores válidos para todos os campos
        self.client.post('/client/new', data={
            'name': 'Cliente Integrado',
            'cpf': '12345678909',  # CPF válido
            'street': 'Rua Teste',
            'number': '100',
            'complement': 'Apto 101',
            'neighborhood': 'Bairro Teste',
            'zip_code': '12345-678',
            'city': 'Cidade Teste',
            'state': 'SP',  # UF válido (duas letras maiúsculas)
            'phone': '123456789',
            'email': 'clienteteste@example.com'
        })
        response = self.client.get('/')
        self.assertIn(b'Cliente Integrado', response.data)

    def test_integration_deleta_to_index(self):
        cliente = Client(
            name='Cliente para Deletar',
            cpf='10987654321',
            street='Rua Teste',
            number='200',
            complement='Casa 2',
            neighborhood='Bairro Teste',
            zip_code='87654-321',
            city='Cidade Teste',
            state='RJ',  # UF válido
            phone='987654321',
            email='clientedeletar@example.com'
        )
        with app.app_context():
            db.session.add(cliente)
            db.session.commit()
            
            # Certifique-se de que o cliente foi realmente salvo
            cliente_id = cliente.id
            self.assertIsNotNone(cliente_id, "O cliente não foi salvo corretamente.")
        
        self.client.get(f'/client/delete/{cliente_id}')
        response = self.client.get('/')
        self.assertNotIn(b'Cliente para Deletar', response.data)

if __name__ == '__main__':
    unittest.main()
