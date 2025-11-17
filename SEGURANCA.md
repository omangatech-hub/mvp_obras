# 🔒 Arquivos Protegidos (Não Versionados)

Este repositório usa `.gitignore` para proteger dados sensíveis e arquivos desnecessários.

## Arquivos Excluídos do Git

### 📁 Ambiente Virtual
```
.venv/          # Ambiente Python (recrie localmente)
```

### 💾 Dados Sensíveis
```
*.db            # Bancos SQLite (dados reais dos usuários)
*.json          # Arquivos JSON (obras, funcionários)
```
**Exceção:** O arquivo `insumos.csv` é versionado pois contém dados públicos do SINAPI.

### 🗑️ Arquivos Temporários
```
__pycache__/    # Cache Python
*.pyc           # Bytecode compilado
.flet/          # Cache do Flet
*.log           # Logs
```

### 💻 IDE/Editor
```
.vscode/        # Configurações VS Code
.idea/          # Configurações PyCharm
```

## 🔐 Por que Proteger?

### Dados Sensíveis
- **insumos.db**: Pode conter preços reais negociados
- **obras.json**: Informações confidenciais de projetos
- **funcionarios.json**: Dados pessoais (CPF, salários)

### Performance
- **.venv/**: ~200MB de dependências (recrie localmente em 2 minutos)
- **__pycache__/**: Cache específico da máquina

## ✅ Primeira Execução

Após clonar o repositório:

### 1. Criar Ambiente Virtual
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Importar Dados SINAPI
```powershell
# Cria insumos.db com 4.984 registros
python importar_csv_sqlite.py
```

### 3. Executar Aplicação
```powershell
python app_flet.py
```

## 📋 O que É Versionado

✅ **Código-fonte** (.py)  
✅ **Documentação** (README.md, GUIA_RAPIDO.md)  
✅ **Dados públicos** (insumos.csv - SINAPI)  
✅ **Configuração** (requirements.txt, .gitignore)  
✅ **Assets** (logojpg.PNG)  
✅ **Scripts** (run.bat, run.ps1)

## 🔄 Backup de Dados

Se você quiser fazer backup dos seus dados:

```powershell
# Criar pasta de backup
New-Item -ItemType Directory -Force -Path backup

# Copiar dados
Copy-Item insumos.db, obras.json, funcionarios.json backup/
```

**⚠️ NUNCA faça commit do backup para o Git!**

## 🛡️ Segurança

- ✅ Dados pessoais protegidos (CPF, salários)
- ✅ Informações comerciais protegidas (preços, contratos)
- ✅ Credenciais nunca versionadas
- ✅ Arquivos temporários ignorados

## 📞 Suporte

Dúvidas sobre arquivos versionados? Consulte `.gitignore` na raiz do projeto.
