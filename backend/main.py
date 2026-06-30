from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Importando nossos módulos separados (Arquitetura limpa)
from models import SaqueRequest, TransferenciaRequest
from database import contas_db

app = FastAPI(
    title="API Banco - Desafio Agilize",
    description="API para simulação de saques e transferências"
)

# ==========================================
# Configuração de CORS (Essencial para o Frontend)
# ==========================================
# Isso permite que o nosso frontend em React (rodando na porta 5173) 
# consiga fazer requisições para esta API (rodando na porta 8000) sem ser bloqueado.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção usaríamos o domínio exato, mas para o desafio "*" é perfeito
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constantes das regras de negócio
TARIFA_CORRENTE = 1.00
LIMITE_CHEQUE_ESPECIAL = -500.00

# ==========================================
# Rotas (Endpoints)
# ==========================================

@app.get("/contas")
def listar_contas():
    """Retorna todas as contas e seus saldos atuais para o frontend exibir."""
    return list(contas_db.values())


@app.post("/saque")
def realizar_saque(req: SaqueRequest):
    """Executa a operação obrigatória de saque aplicando as regras R1 e R2."""
    conta = contas_db.get(req.conta_id)
    
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada.")

    # Regra 1 (R1): Conta Corrente
    if conta["tipo"] == "corrente":
        custo_total = req.valor + TARIFA_CORRENTE
        novo_saldo = conta["saldo"] - custo_total
        
        if novo_saldo < LIMITE_CHEQUE_ESPECIAL:
            raise HTTPException(
                status_code=400, 
                detail=f"Operação negada. O limite do cheque especial é de R$ 500,00 negativos."
            )
            
        conta["saldo"] = novo_saldo
        return {"mensagem": "Saque realizado com sucesso", "tarifa": TARIFA_CORRENTE, "saldo_atual": conta["saldo"]}

    # Regra 2 (R2): Conta Poupança
    elif conta["tipo"] == "poupanca":
        if conta["saldo"] < req.valor:
            raise HTTPException(
                status_code=400, 
                detail="Operação negada. Conta poupança não possui limite de cheque especial."
            )
            
        conta["saldo"] -= req.valor
        return {"mensagem": "Saque realizado com sucesso", "tarifa": 0, "saldo_atual": conta["saldo"]}


@app.post("/transferencia")
def realizar_transferencia(req: TransferenciaRequest):
    """Executa a operação opcional de transferência rendendo pontos extras."""
    origem = contas_db.get(req.conta_origem)
    destino = contas_db.get(req.conta_destino)

    if not origem:
        raise HTTPException(status_code=404, detail="Conta de origem não encontrada.")
    if not destino:
        raise HTTPException(status_code=404, detail="Conta de destino não encontrada.")
    if origem["id"] == destino["id"]:
        raise HTTPException(status_code=400, detail="Não é possível transferir para a mesma conta.")

    # Validação de regras na conta de origem
    if origem["tipo"] == "corrente":
        custo_total = req.valor + TARIFA_CORRENTE
        novo_saldo = origem["saldo"] - custo_total
        
        if novo_saldo < LIMITE_CHEQUE_ESPECIAL:
            raise HTTPException(status_code=400, detail="Limite de cheque especial excedido na origem.")
            
        origem["saldo"] = novo_saldo

    elif origem["tipo"] == "poupanca":
        if origem["saldo"] < req.valor:
            raise HTTPException(status_code=400, detail="Saldo insuficiente na origem.")
            
        origem["saldo"] -= req.valor

    # Adiciona o valor na conta de destino (sem descontar tarifa de quem recebe)
    destino["saldo"] += req.valor

    return {
        "mensagem": "Transferência realizada com sucesso", 
        "saldo_origem_atual": origem["saldo"]
    }