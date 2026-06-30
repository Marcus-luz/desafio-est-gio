# Minha Solução — Banco

## Stack

* **Backend:** Python 3.13 (FastAPI/Uvicorn)
* **Frontend:** React 19 + Vite + JavaScript

## Pré-requisitos / dependências

* Python 3.10 ou superior
* Node.js 18 ou superior
* Backend: `pip install -r requirements.txt`
* Frontend: `npm install`

## Como executar

### Backend (API)

```bash
cd backend

# Ativar ambiente virtual

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

uvicorn main:app --reload --port 8000

# API disponível em http://localhost:8000
```

### Frontend

```bash
cd frontend

npm install
npm run dev

# Aplicação disponível em http://localhost:5173
```

## Exemplo de uso

```
1. Acesse a aplicação pelo navegador.
2. Selecione uma conta (Corrente ou Poupança).
3. Informe um valor para saque ou transferência.
4. Execute a operação.
5. A API aplica as regras de negócio da conta selecionada e retorna o saldo atualizado.
6. O histórico de transações é atualizado após cada operação.
```

## Observações (opcional)

* Implementada a funcionalidade de transferência entre contas (item bônus).
* Implementado histórico de transações.
* Testes unitários utilizando Pytest.
* Testes End-to-End utilizando Cypress.
* Script `run.py` para inicialização automática do Backend e Frontend.
* Conta Corrente: tarifa de R$ 1,00 por operação e cheque especial até R$ -500,00.
* Conta Poupança: sem tarifa e sem saldo negativo.
