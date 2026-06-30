# 🏦 Banco Agilize

Aplicação Full Stack desenvolvida como solução para o desafio técnico da Agilize.

O sistema simula operações bancárias entre contas Corrente e Poupança, aplicando regras específicas para saques e transferências, além de disponibilizar histórico de transações e testes automatizados.

---

# 🚀 Tecnologias Utilizadas

## Backend

* Python 3.13
* FastAPI
* Uvicorn
* Pydantic

## Frontend

* React 19
* Vite
* JavaScript

## Testes

* Pytest
* Cypress

---

# 📋 Pré-requisitos

Antes de iniciar, certifique-se de possuir instalado:

* Python 3.10 ou superior
* Node.js 18 ou superior
* NPM

Para verificar as versões:

```bash
python --version
node --version
npm --version
```

---

# 📥 Clonando o Projeto

```bash
git clone <url-do-repositorio>

cd banco-agilize
```

---

# ▶️ Executando o Projeto

A aplicação é composta por:

* Backend (API FastAPI)
* Frontend (Interface React)

Ambos devem estar executando simultaneamente.

---

## 1️⃣ Iniciando o Backend

Abra um terminal na raiz do projeto.

Entre na pasta do backend:

```bash
cd backend
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual.

### Windows (PowerShell)

```bash
.\venv\Scripts\activate
```

### Linux / MacOS

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Inicie a API:

```bash
uvicorn main:app --reload --port 8000
```

Se tudo estiver correto, você verá uma mensagem semelhante a:

```text
Uvicorn running on http://127.0.0.1:8000
```

A API estará disponível em:

```text
http://localhost:8000
```

⚠️ Mantenha este terminal aberto durante toda a execução do projeto.

---

## 2️⃣ Iniciando o Frontend

Abra um NOVO terminal (sem fechar o terminal do backend).

Volte para a raiz do projeto:

```bash
cd frontend
```

Instale as dependências:

```bash
npm install
```

Inicie a aplicação:

```bash
npm run dev
```

Você verá uma saída semelhante a:

```text
Local: http://localhost:5173
```

A aplicação estará disponível em:

```text
http://localhost:5173
```

⚠️ Mantenha este terminal aberto durante toda a execução do projeto.

---

## 3️⃣ Validando a Aplicação

Com os dois terminais em execução:

### Backend

```text
http://localhost:8000
```

### Frontend

```text
http://localhost:5173
```

Acesse o endereço do Frontend no navegador para utilizar o sistema.

---

# ⚡ Inicialização Automática

Também é possível iniciar Backend e Frontend utilizando o script disponibilizado na raiz do projeto.

Execute:

```bash
python run.py
```

O script irá:

* Iniciar o Backend;
* Iniciar o Frontend;
* Abrir automaticamente o navegador.

Para encerrar tudo:

```bash
CTRL + C
```

---

# 📌 Regras de Negócio

## Conta Corrente

* Cobrança de R$ 1,00 por operação.
* Permite utilização de cheque especial.
* Limite mínimo de saldo: R$ -500,00.
* Operações que ultrapassem esse limite são recusadas.

## Conta Poupança

* Não possui tarifa.
* Não permite saldo negativo.

## Transferências

* Não é permitido transferir para a mesma conta.
* O valor deve ser maior que zero.

---

# 🧪 Testes Automatizados

Os testes estão organizados na pasta:

```text
/testes
```

---

## Testes Unitários (Backend)

Abra um novo terminal.

Entre na pasta:

```bash
cd testes
```

Ative o ambiente virtual utilizado pelo backend.

### Windows

```bash
..\backend\venv\Scripts\activate
```

### Linux / MacOS

```bash
source ../backend/venv/bin/activate
```

Execute:

```bash
pytest test_backend.py
```

---

## Testes E2E (Frontend)

Antes de executar, certifique-se de que Backend e Frontend estejam rodando.

Abra um novo terminal.

Entre na pasta:

```bash
cd testes
```

Executar em modo headless:

```bash
npx cypress run
```

Executar com interface gráfica:

```bash
npx cypress open
```

---

# 📂 Estrutura do Projeto

```text
Banco-Agilize/
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── services.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── testes/
│   ├── test_backend.py
│   └── cypress/
│
├── run.py
│
└── README.md
```

---

# ⭐ Diferenciais Implementados

* Transferência entre contas.
* Histórico de transações.
* Testes unitários com Pytest.
* Testes End-to-End com Cypress.
* Inicialização automatizada via script.
* Validações implementadas no Backend e Frontend.
