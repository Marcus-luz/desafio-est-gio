import { useState, useEffect } from 'react';
import { getContas, realizarSaque, realizarTransferencia } from './api';

function App() {
  // ==========================================
  // Estados da Aplicação
  // ==========================================
  const [contas, setContas] = useState([]);
  const [mensagem, setMensagem] = useState({ texto: '', tipo: '' });

  // Estados do Formulário de Saque
  const [saqueConta, setSaqueConta] = useState('');
  const [saqueValor, setSaqueValor] = useState('');

  // Estados do Formulário de Transferência
  const [transfOrigem, setTransfOrigem] = useState('');
  const [transfDestino, setTransfDestino] = useState('');
  const [transfValor, setTransfValor] = useState('');

  // ==========================================
  // Lógica de Carregamento e Feedback
  // ==========================================
  const carregarContas = async () => {
    try {
      const dados = await getContas();
      setContas(dados);
    } catch (error) {
      mostrarMensagem('Erro ao carregar contas da API.', 'erro');
    }
  };

  // Executa assim que a tela abre pela primeira vez
  useEffect(() => {
    carregarContas();
  }, []);

  const mostrarMensagem = (texto, tipo) => {
    setMensagem({ texto, tipo });
    // Esconde a mensagem automaticamente após 5 segundos
    setTimeout(() => setMensagem({ texto: '', tipo: '' }), 5000);
  };

  // ==========================================
  // Handlers dos Formulários
  // ==========================================
  const handleSaque = async (e) => {
    e.preventDefault(); // Evita que a página recarregue
    try {
      const res = await realizarSaque(saqueConta, saqueValor);
      mostrarMensagem(res.mensagem, 'sucesso');
      setSaqueValor(''); 
      carregarContas(); // Atualiza os saldos imediatamente na tela
    } catch (error) {
      mostrarMensagem(error.message, 'erro');
    }
  };

  const handleTransferencia = async (e) => {
    e.preventDefault();
    if (transfOrigem === transfDestino) {
      mostrarMensagem('A conta de origem e destino não podem ser as mesmas.', 'erro');
      return;
    }

    try {
      const res = await realizarTransferencia(transfOrigem, transfDestino, transfValor);
      mostrarMensagem(res.mensagem, 'sucesso');
      setTransfValor('');
      carregarContas(); // Atualiza os saldos imediatamente na tela
    } catch (error) {
      mostrarMensagem(error.message, 'erro');
    }
  };

  // ==========================================
  // Interface do Usuário (Renderização)
  // ==========================================
  return (
    <div style={{ padding: '30px', fontFamily: 'sans-serif', maxWidth: '900px', margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center', color: '#333' }}>🏦 Banco Agilize</h1>

      {/* Caixa de Mensagens de Sucesso ou Erro */}
      {mensagem.texto && (
        <div style={{
          padding: '15px',
          marginBottom: '20px',
          backgroundColor: mensagem.tipo === 'erro' ? '#ffe6e6' : '#e6ffe6',
          color: mensagem.tipo === 'erro' ? '#cc0000' : '#006600',
          border: `1px solid ${mensagem.tipo === 'erro' ? '#ffcccc' : '#ccffcc'}`,
          borderRadius: '8px',
          textAlign: 'center',
          fontWeight: 'bold'
        }}>
          {mensagem.texto}
        </div>
      )}

      {/* Seção 1: Listagem de Contas */}
      <section style={{ marginBottom: '40px' }}>
        <h2>Saldos Disponíveis</h2>
        <div style={{ display: 'flex', gap: '15px', flexWrap: 'wrap' }}>
          {contas.map(conta => (
            <div key={conta.id} style={{ 
              border: '1px solid #ddd', 
              padding: '20px', 
              borderRadius: '10px', 
              flex: '1 1 250px',
              backgroundColor: '#f9f9f9',
              boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
            }}>
              <h3 style={{ margin: '0 0 10px 0', color: '#0056b3' }}>Conta {conta.id}</h3>
              <p style={{ margin: '5px 0' }}><strong>Tipo:</strong> {conta.tipo === 'corrente' ? 'Corrente' : 'Poupança'}</p>
              <p style={{ margin: '5px 0', fontSize: '1.2em' }}>
                <strong>Saldo:</strong> R$ {conta.saldo.toFixed(2)}
              </p>
            </div>
          ))}
        </div>
      </section>

      <hr style={{ border: 'none', borderTop: '2px solid #eee', margin: '30px 0' }} />

      {/* Seção 2: Formulários de Operação */}
      <section style={{ display: 'flex', gap: '40px', flexWrap: 'wrap' }}>
        
        {/* Formulário de Saque */}
        <div style={{ flex: '1 1 300px' }}>
          <h2 style={{ color: '#d9534f' }}>Realizar Saque</h2>
          <form onSubmit={handleSaque} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
            <select 
              value={saqueConta} 
              onChange={(e) => setSaqueConta(e.target.value)} 
              required
              style={{ padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
            >
              <option value="">Selecione a conta...</option>
              {contas.map(c => <option key={c.id} value={c.id}>Conta {c.id} ({c.tipo})</option>)}
            </select>
            
            <input 
              type="number" 
              step="0.01" 
              placeholder="Valor a sacar (R$)" 
              value={saqueValor} 
              onChange={(e) => setSaqueValor(e.target.value)} 
              required 
              style={{ padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
            />
            
            <button 
              type="submit" 
              style={{ padding: '10px', backgroundColor: '#d9534f', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold' }}
            >
              Confirmar Saque
            </button>
          </form>
        </div>

        {/* Formulário de Transferência */}
        <div style={{ flex: '1 1 300px' }}>
          <h2 style={{ color: '#5cb85c' }}>Transferência (Extra)</h2>
          <form onSubmit={handleTransferencia} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
            <select 
              value={transfOrigem} 
              onChange={(e) => setTransfOrigem(e.target.value)} 
              required
              style={{ padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
            >
              <option value="">Conta de Origem (Sai o dinheiro)...</option>
              {contas.map(c => <option key={c.id} value={c.id}>Conta {c.id} ({c.tipo})</option>)}
            </select>

            <select 
              value={transfDestino} 
              onChange={(e) => setTransfDestino(e.target.value)} 
              required
              style={{ padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
            >
              <option value="">Conta de Destino (Recebe o dinheiro)...</option>
              {contas.map(c => <option key={c.id} value={c.id}>Conta {c.id}</option>)}
            </select>

            <input 
              type="number" 
              step="0.01" 
              placeholder="Valor a transferir (R$)" 
              value={transfValor} 
              onChange={(e) => setTransfValor(e.target.value)} 
              required 
              style={{ padding: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
            />
            
            <button 
              type="submit" 
              style={{ padding: '10px', backgroundColor: '#5cb85c', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold' }}
            >
              Confirmar Transferência
            </button>
          </form>
        </div>

      </section>
    </div>
  );
}

export default App;