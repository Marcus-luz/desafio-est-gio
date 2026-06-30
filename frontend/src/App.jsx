import { useState, useEffect } from 'react';
import { getContas, realizarSaque, realizarTransferencia, getHistorico } from './Api';
import './App.css';
import logoBanco from './assets/logo-banco.png';

function App() {
  const [nomeRecrutador, setNomeRecrutador] = useState('');
  const [telaLogada, setTelaLogada] = useState(false);
  const [inputNome, setInputNome] = useState('');

  const [contas, setContas] = useState([]);
  const [historico, setHistorico] = useState([]);
  const [mensagem, setMensagem] = useState({ texto: '', tipo: '' });

  const [saqueConta, setSaqueConta] = useState('');
  const [saqueValor, setSaqueValor] = useState('');

  const [transfOrigem, setTransfOrigem] = useState('');
  const [transfDestino, setTransfDestino] = useState('');
  const [transfValor, setTransfValor] = useState('');

  const carregarDados = async () => {
    try {
      const dadosContas = await getContas();
      const dadosHistorico = await getHistorico();
      setContas(dadosContas);
      setHistorico(dadosHistorico);
    } catch (error) {
      mostrarMensagem('Erro ao conectar com o servidor.', 'erro');
    }
  };

  useEffect(() => { carregarDados(); }, []);

  const mostrarMensagem = (texto, tipo) => {
    setMensagem({ texto, tipo });
    setTimeout(() => setMensagem({ texto: '', tipo: '' }), 5000);
  };

  const handleEntrar = (e) => {
    e.preventDefault();
    if (inputNome.trim() !== '') {
      setNomeRecrutador(inputNome);
      setTelaLogada(true);
    }
  };

  const handleSaque = async (e) => {
    e.preventDefault();
    try {
      const res = await realizarSaque(saqueConta, saqueValor);
      mostrarMensagem(res.mensagem, 'sucesso');
      setSaqueValor(''); 
      carregarDados();
    } catch (error) {
      mostrarMensagem(error.message, 'erro');
      setSaqueValor(''); // Limpa o campo mesmo com erro
    }
  };

  const handleTransferencia = async (e) => {
    e.preventDefault();
    if (transfOrigem === transfDestino) {
      mostrarMensagem('A conta de origem e destino não podem ser iguais.', 'erro');
      setTransfValor(''); // Limpa o campo
      return;
    }
    try {
      const res = await realizarTransferencia(transfOrigem, transfDestino, transfValor);
      mostrarMensagem(res.mensagem, 'sucesso');
      setTransfValor('');
      carregarDados();
    } catch (error) {
      mostrarMensagem(error.message, 'erro');
      setTransfValor(''); // Limpa o campo mesmo com erro
    }
  };

  if (!telaLogada) {
    return (
      <div className="login-container">
        <div className="login-card">
          {/* Substituímos o H2 simples pela logo do banco */}
          <img src={logoBanco} alt="Logotipo Banco Agilize" className="login-logo" />
          
          <form onSubmit={handleEntrar}>
            <input 
              type="text" 
              placeholder="Digite seu nome" 
              value={inputNome}
              onChange={(e) => setInputNome(e.target.value)}
              required
            />
            <button type="submit" className="btn-primary" style={{ backgroundColor: '#FF7E5F' }}>
              ACESSAR
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <header className="header-bg">
        <h1>Olá, {nomeRecrutador}</h1>
        <p>Bem-vindo ao Banco Agilize</p>
      </header>

      {mensagem.texto && (
        <div className={`alert ${mensagem.tipo}`}>
          {mensagem.texto}
        </div>
      )}

      <section className="cards-container">
        {contas.map(conta => (
          <div className="bank-card" key={conta.id}>
            <h3>Conta {conta.id}</h3>
            <div className="balance">
              R$ {conta.saldo.toFixed(2)}
            </div>
            <div className="type">
              {conta.tipo === 'corrente' ? 'Corrente' : 'Poupança'}
            </div>
          </div>
        ))}
      </section>

      <section className="actions-section">
        <div className="action-card">
          <h2>Fazer Saque</h2>
          <form onSubmit={handleSaque}>
            <div className="input-group">
              <select value={saqueConta} onChange={(e) => setSaqueConta(e.target.value)} required>
                <option value="">Selecione a conta...</option>
                {contas.map(c => <option key={c.id} value={c.id}>Conta {c.id} - R$ {c.saldo}</option>)}
              </select>
            </div>
            <div className="input-group">
              {/* Bloqueio de valores negativos via HTML (min="0.01") */}
              <input type="number" step="0.01" min="0.01" placeholder="Valor (R$)" value={saqueValor} onChange={(e) => setSaqueValor(e.target.value)} required />
            </div>
            <button type="submit" className="btn-primary">Confirmar Saque</button>
          </form>
        </div>

        <div className="action-card">
          <h2>Transferência</h2>
          <form onSubmit={handleTransferencia}>
            <div className="input-group">
              <select value={transfOrigem} onChange={(e) => setTransfOrigem(e.target.value)} required>
                <option value="">De (Origem)...</option>
                {contas.map(c => <option key={c.id} value={c.id}>Conta {c.id} - R$ {c.saldo}</option>)}
              </select>
            </div>
            <div className="input-group">
              <select value={transfDestino} onChange={(e) => setTransfDestino(e.target.value)} required>
                <option value="">Para (Destino)...</option>
                {contas.map(c => <option key={c.id} value={c.id}>Conta {c.id}</option>)}
              </select>
            </div>
            <div className="input-group">
               {/* Bloqueio de valores negativos via HTML (min="0.01") */}
              <input type="number" step="0.01" min="0.01" placeholder="Valor (R$)" value={transfValor} onChange={(e) => setTransfValor(e.target.value)} required />
            </div>
            <button type="submit" className="btn-primary btn-secondary">Transferir Agora</button>
          </form>
        </div>
      </section>

      {/* Nova Seção: Histórico de Transações */}
      <section className="historico-section">
        <h2>Histórico de Atividades</h2>
        <div className="historico-list">
          {historico.length === 0 ? (
            <p style={{ textAlign: 'center', color: '#888', padding: '10px' }}>Nenhuma transação realizada ainda.</p>
          ) : (
            historico.map(item => (
              <div className="historico-item" key={item.id}>
                <span className="hist-data">{item.data}</span>
                <span className="hist-tipo">{item.tipo}</span>
                <span className="hist-detalhes">{item.detalhes}</span>
              </div>
            ))
          )}
        </div>
      </section>

    </div>
  );
}

export default App;