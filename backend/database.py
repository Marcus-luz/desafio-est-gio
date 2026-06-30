
# Banco de Dados em Memória

# Utilizamos um dicionário onde a chave é o ID da conta.
# Isso simula o comportamento de uma chave primária (Primary Key) em um banco real,
# permitindo buscas incrivelmente rápidas com complexidade O(1).

contas_db = {
    "1001": {
        "id": "1001",
        "tipo": "corrente",
        "saldo": 1000.00
    },
    "1002": {
        "id": "1002",
        "tipo": "poupanca",
        "saldo": 1000.00
    },
    # Uma conta com saldo baixo propositalmente para testarmos 
    # a Regra 1 (limite do cheque especial) mais facilmente depois.
    "1003": {
        "id": "1003",
        "tipo": "corrente",
        "saldo": 100.00 
    }
}