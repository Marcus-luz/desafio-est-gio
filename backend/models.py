from pydantic import BaseModel, Field


# NOTA ARQUITETURAL: 
# Para fins de simplificação deste desafio, os valores monetários estão tipados como 'float'.
# Em um ambiente de produção real, utilizaríamos o tipo 'Decimal' (da biblioteca built-in 'decimal') 
# ou armazenaríamos os valores em centavos (Integer) para evitar problemas de precisão de ponto flutuante.

# ==========================================
# Requisições (O que o Frontend envia)
# ==========================================

class SaqueRequest(BaseModel):
    conta_id: str = Field(
        ..., 
        description="ID da conta que realizará o saque"
    )
    # O parâmetro 'gt=0' garante que o valor deve ser Maior que Zero (Greater Than)
    valor: float = Field(
        ..., 
        gt=0, 
        description="O valor do saque deve ser estritamente maior que zero"
    )

class TransferenciaRequest(BaseModel):
    conta_origem: str = Field(
        ..., 
        description="ID da conta de origem do dinheiro"
    )
    conta_destino: str = Field(
        ..., 
        description="ID da conta que receberá o dinheiro"
    )
    valor: float = Field(
        ..., 
        gt=0, 
        description="O valor da transferência deve ser estritamente maior que zero"
    )

# ==========================================
# Respostas (O que o Backend devolve)
# ==========================================

class ContaResponse(BaseModel):
    id: str
    tipo: str
    saldo: float