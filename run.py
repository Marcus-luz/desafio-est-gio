import subprocess
import os
import sys
import time
import webbrowser

print("🚀 Iniciando o ecossistema do Banco Agilize...")

is_windows = os.name == 'nt'
base_dir = os.path.abspath(os.path.dirname(__file__))
backend_dir = os.path.join(base_dir, "backend")
frontend_dir = os.path.join(base_dir, "frontend")

# Caminhos do ambiente virtual
venv_dir = os.path.join(backend_dir, "venv")

if is_windows:
    python_exec = os.path.join(venv_dir, "Scripts", "python.exe")
    pip_exec = os.path.join(venv_dir, "Scripts", "pip.exe")
else:
    python_exec = os.path.join(venv_dir, "bin", "python")
    pip_exec = os.path.join(venv_dir, "bin", "pip")

# ==========================================
# 1. SETUP AUTOMÁTICO (Máquina Limpa)
# ==========================================

# Instala o backend se o venv não existir
if not os.path.exists(venv_dir):
    print("📦 Ambiente virtual não encontrado. Criando 'venv' no backend...")
    subprocess.run([sys.executable, "-m", "venv", "venv"], cwd=backend_dir)
    
    print("📥 Instalando dependências do Python (FastAPI, Uvicorn, etc)...")
    subprocess.run([pip_exec, "install", "-r", "requirements.txt"], cwd=backend_dir)

# Instala o frontend se o node_modules não existir
node_modules_dir = os.path.join(frontend_dir, "node_modules")
if not os.path.exists(node_modules_dir):
    print("📦 Dependências do frontend não encontradas. Executando 'npm install'...")
    subprocess.run("npm install", shell=True, cwd=frontend_dir)

# ==========================================
# 2. INICIALIZAÇÃO DOS SERVIDORES
# ==========================================

backend_process = None
frontend_process = None

try:
    print("⏳ Subindo o Backend (FastAPI)...")
    backend_process = subprocess.Popen(
        [python_exec, "-m", "uvicorn", "main:app", "--reload", "--port", "8000"], 
        cwd=backend_dir
    )
    
    time.sleep(2) 
    
    print("⏳ Subindo o Frontend (React/Vite)...")
    frontend_process = subprocess.Popen(
        "npm run dev", 
        shell=True, 
        cwd=frontend_dir
    )
    
    time.sleep(3)
    print("🌐 Abrindo o navegador...")
    webbrowser.open("http://localhost:5173")
    
    print("\n✅ Servidores no ar! A aplicação está rodando perfeitamente.")
    print("👉 Pressione CTRL+C aqui neste terminal para desligar tudo de uma vez.\n")
    
    backend_process.wait()
    frontend_process.wait()

except KeyboardInterrupt:
    print("\n🛑 Recebido comando de parada (CTRL+C). Desligando servidores...")
    if backend_process:
        backend_process.terminate()
    if frontend_process:
        frontend_process.terminate()
    print("👋 Encerrado com sucesso. Até logo!")
    sys.exit(0)