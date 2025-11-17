# 🚀 Início Rápido - MVP Gestão de Obras

## ⚡ Instalação (5 minutos)

### 1️⃣ Clone o Repositório
```powershell
git clone https://github.com/omangatech-hub/mvp_obras.git
cd mvp_obras
```

### 2️⃣ Crie o Ambiente Virtual
```powershell
python -m venv .venv
```

### 3️⃣ Ative o Ambiente Virtual
**Windows PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
.\.venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4️⃣ Instale as Dependências
```powershell
pip install -r requirements.txt
```

### 5️⃣ Importe os Insumos SINAPI
```powershell
python importar_csv_sqlite.py
```
> ⏱️ Aguarde ~10 segundos (importa 4.984 registros)

### 6️⃣ Execute a Aplicação
```powershell
python app_flet.py
```

## 🎉 Pronto!

A aplicação abrirá em uma janela desktop. Navegue pelo menu lateral:

- 🏠 **Início**: Visão geral
- 🏗️ **Obras**: Gerenciar projetos
- 📦 **Insumos**: Catálogo com 4.984 itens do SINAPI
- 👷 **Funcionários**: RH e folha de pagamento
- 📊 **Dashboard**: Análises e gráficos

## 🔧 Comandos Úteis

### Popular Dados de Exemplo
```powershell
python popular_dados.py
```
Cria: 3 obras, 5 insumos, 4 funcionários

### Reimportar Insumos
```powershell
python importar_csv_sqlite.py
```
Recria o banco `insumos.db`

### Executar sem Ativar venv
```powershell
.\.venv\Scripts\python.exe app_flet.py
```

## 📚 Documentação

- **README.md**: Documentação completa
- **GUIA_RAPIDO.md**: Guia de uso rápido
- **SEGURANCA.md**: Informações sobre arquivos protegidos

## 🆘 Problemas?

### Erro: `ModuleNotFoundError: No module named 'flet'`
```powershell
# Certifique-se de estar no ambiente virtual
.\.venv\Scripts\Activate.ps1
pip install flet
```

### Erro: `file is not a database`
```powershell
# Reimporte os insumos
Remove-Item insumos.db -ErrorAction SilentlyContinue
python importar_csv_sqlite.py
```

### Aplicação não abre
```powershell
# Use o Python da venv explicitamente
.\.venv\Scripts\python.exe app_flet.py
```

## 🌟 Recursos Principais

✅ **4.984 insumos** do SINAPI importados  
✅ **Paginação** - 50 itens por página  
✅ **Busca rápida** - índices SQLite otimizados  
✅ **Interface moderna** - Material Design 3  
✅ **Performance** - carrega apenas dados necessários  

## 📞 Suporte

Consulte a documentação completa em `README.md` ou o guia rápido em `GUIA_RAPIDO.md`.

---

**Desenvolvido com ❤️ em Python + Flet**
