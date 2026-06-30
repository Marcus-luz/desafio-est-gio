// A URL base onde o nosso FastAPI está rodando
const API_URL = 'http://127.0.0.1:8000';

export const getContas = async () => {
    const response = await fetch(`${API_URL}/contas`);
    return response.json();
};

export const realizarSaque = async (conta_id, valor) => {
    const response = await fetch(`${API_URL}/saque`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        // O body precisa bater exatamente com o SaqueRequest do Pydantic
        body: JSON.stringify({ conta_id, valor: parseFloat(valor) })
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        // Dispara o erro com a mensagem exata que definimos no backend (ex: "Saldo insuficiente")
        throw new Error(errorData.detail || 'Erro desconhecido ao realizar saque');
    }
    
    return response.json();
};

export const realizarTransferencia = async (conta_origem, conta_destino, valor) => {
    const response = await fetch(`${API_URL}/transferencia`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            conta_origem, 
            conta_destino, 
            valor: parseFloat(valor) 
        })
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Erro desconhecido ao realizar transferência');
    }

    return response.json();
};