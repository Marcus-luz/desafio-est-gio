from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from models import SaqueRequest, TransferenciaRequest
from database import contas_db, historico_db

app = FastAPI(title="API Banco - Desafio Agilize")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TARIFA_CORRENTE = 1.00
LIMITE_CHEQUE_ESPECIAL = -500.00

# ==========================================
# Funções Auxiliares
# ==========================================
def registrar_transacao(tipo: str, detalhes: str):
    """Grava a operação no banco de dados com data e hora."""
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    historico_db.append({
        "id": len(historico_db) + 1,
        "data": data_atual,
        "tipo": tipo,
        "detalhes": detalhes
    })

# ==========================================
# Rotas (Endpoints)
# ==========================================

@app.get("/contas")
def listar_contas():
    return list(contas_db.values())

@app.get("/historico")
def listar_historico():
    # Retorna o histórico invertido (mais recentes primeiro)
    return list(reversed(historico_db))

@app.post("/saque")
def realizar_saque(req: SaqueRequest):
    conta = contas_db.get(req.conta_id)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada.")

    if conta["tipo"] == "corrente":
        custo_total = req.valor + TARIFA_CORRENTE
        novo_saldo = conta["saldo"] - custo_total
        
        if novo_saldo < LIMITE_CHEQUE_ESPECIAL:
            raise HTTPException(status_code=400, detail="Operação negada: Limite do cheque especial excedido (-R$ 500,00).")
            
        conta["saldo"] = novo_saldo
        registrar_transacao("Saque", f"Conta {conta['id']} sacou R$ {req.valor:.2f} (Tarifa: R$ 1.00)")
        return {"mensagem": "Saque realizado com sucesso", "saldo_atual": conta["saldo"]}

    elif conta["tipo"] == "poupanca":
        if conta["saldo"] < req.valor:
            raise HTTPException(status_code=400, detail="Operação negada: Conta poupança não possui limite de cheque especial.")
            
        conta["saldo"] -= req.valor
        registrar_transacao("Saque", f"Conta {conta['id']} sacou R$ {req.valor:.2f} (Isento de tarifa)")
        return {"mensagem": "Saque realizado com sucesso", "saldo_atual": conta["saldo"]}

@app.post("/transferencia")
def realizar_transferencia(req: TransferenciaRequest):
    origem = contas_db.get(req.conta_origem)
    destino = contas_db.get(req.conta_destino)

    # Edge Cases (Casos Extremos)
    if not origem or not destino:
        raise HTTPException(status_code=404, detail="Conta de origem ou destino não encontrada.")
    if origem["id"] == destino["id"]:
        raise HTTPException(status_code=400, detail="Operação negada: Não é possível transferir para a mesma conta.")

    if origem["tipo"] == "corrente":
        custo_total = req.valor + TARIFA_CORRENTE
        novo_saldo = origem["saldo"] - custo_total
        if novo_saldo < LIMITE_CHEQUE_ESPECIAL:
            raise HTTPException(status_code=400, detail="Operação negada: Limite de cheque especial excedido na origem.")
        origem["saldo"] = novo_saldo

    elif origem["tipo"] == "poupanca":
        if origem["saldo"] < req.valor:
            raise HTTPException(status_code=400, detail="Operação negada: Saldo insuficiente na conta origem.")
        origem["saldo"] -= req.valor

    destino["saldo"] += req.valor
    
    registrar_transacao(
        "Transferência", 
        f"Conta {origem['id']} enviou R$ {req.valor:.2f} para Conta {destino['id']}"
    )

    return {"mensagem": "Transferência realizada com sucesso", "saldo_origem_atual": origem["saldo"]}