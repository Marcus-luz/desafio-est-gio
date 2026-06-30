import sys
import os

caminho_backend = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, caminho_backend)

import pytest
from fastapi.testclient import TestClient

from main import app
from database import contas_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    """Reseta o estado do banco em memória antes de cada teste, garantindo isolamento."""
    contas_db.clear()
    contas_db.update({
        "1001": {"id": "1001", "tipo": "corrente", "saldo": 1000.00},
        "1002": {"id": "1002", "tipo": "poupanca", "saldo": 1000.00},
        "1003": {"id": "1003", "tipo": "corrente", "saldo": 100.00}
    })


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