import subprocess
import os
import sys
import time
import webbrowser  # <-- NOVO IMPORT: Biblioteca nativa para abrir o navegador

print("Iniciando o Banco Agilize (Fullstack)...")

is_windows = os.name == 'nt'

# Pega o caminho absoluto (completo) da pasta onde este script está rodando
base_dir = os.path.abspath(os.path.dirname(__file__))
backend_dir = os.path.join(base_dir, "backend")

# Constrói o caminho completo até o python.exe (ex: C:\...\backend\venv\Scripts\python.exe)
if is_windows:
    python_exec = os.path.join(backend_dir, "venv", "Scripts", "python.exe")
else:
    python_exec = os.path.join(backend_dir, "venv", "bin", "python")

backend_process = None
frontend_process = None

try:
    print("Subindo o Backend (FastAPI)...")
    # Passamos o caminho absoluto do python para não ter erro de pasta
    backend_process = subprocess.Popen(
        [python_exec, "-m", "uvicorn", "main:app", "--reload", "--port", "8000"], 
        cwd=backend_dir
    )
    
    time.sleep(2) 
    
    print("Subindo o Frontend (React/Vite)...")
    frontend_process = subprocess.Popen(
        "npm run dev", 
        shell=True, 
        cwd=os.path.join(base_dir, "frontend")
    )
    
    # ==========================================
    # MÁGICA: ABRIR O NAVEGADOR AUTOMATICAMENTE
    # ==========================================
    time.sleep(2.5) # Dá 2 segundos e meio para o Vite estar 100% no ar
    print("Abrindo o navegador...")
    webbrowser.open("http://localhost:5173")
    
    print("\nServidores no ar! A aplicação deve estar aberta no seu navegador.")
    print("Pressione CTRL+C aqui neste terminal para desligar tudo de uma vez.\n")
    
    backend_process.wait()
    frontend_process.wait()

except KeyboardInterrupt:
    print("\nRecebido comando de parada (CTRL+C). Desligando servidores...")
    if backend_process:
        backend_process.terminate()
    if frontend_process:
        frontend_process.terminate()
    print("Encerrado com sucesso. Até logo!")
    sys.exit(0)