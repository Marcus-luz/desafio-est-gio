import sys
import os

# Aponta o caminho absoluto para a pasta 'backend' para importar o código fonte
caminho_backend = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, caminho_backend)

from fastapi.testclient import TestClient

# Como o sys.path já está dentro da pasta backend, importamos o app e o banco diretamente
from main import app
from database import contas_db

client = TestClient(app)

def test_saque_conta_corrente_cobra_tarifa():
    # Saque de 100 + 1 de tarifa = 899 restantes na conta 1001
    response = client.post("/saque", json={"conta_id": "1001", "valor": 100.00})
    assert response.status_code == 200
    assert contas_db["1001"]["saldo"] == 899.00

def test_saque_rejeitado_limite_cheque_especial():
    # Tentar sacar mais do que os 100 de saldo e o limite de -500 da conta 1003
    response = client.post("/saque", json={"conta_id": "1003", "valor": 600.00})
    assert response.status_code == 400
    assert "Limite do cheque especial" in response.json()["detail"]

def test_transferencia_mesma_conta_rejeitada():
    response = client.post(
        "/transferencia", 
        json={"conta_origem": "1002", "conta_destino": "1002", "valor": 50.00}
    )
    assert response.status_code == 400