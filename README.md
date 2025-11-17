# 🏗️ Sistema de Gestão de Obras - Tiago Rizzetto

Sistema completo de gerenciamento de obras de construção com **interface moderna em Flet** (Material Design).

![Status](https://img.shields.io/badge/status-completo-brightgreen) ![Python](https://img.shields.io/badge/python-3.13.5-blue) ![Flet](https://img.shields.io/badge/flet-0.28.3-orange)

---

## 📋 Índice

- [Características](#-características)
- [Capturas de Tela](#-capturas-de-tela)
- [Tecnologias](#️-tecnologias)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Módulos](#-módulos)
- [Interface Gráfica](#-interface-gráfica)
- [Desenvolvimento](#-desenvolvimento)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Características

### 🏗️ Gerenciamento de Obras
- ✅ Cadastro completo (nome, datas, custos estimados e reais)
- ✅ Controle de obras em andamento e finalizadas
- ✅ Acompanhamento de custos estimados vs reais
- ✅ Finalização de obras com registro de término efetivo
- ✅ Validação automática de datas e valores
- ✅ DataTable interativa com edição inline

### 📦 Controle de Insumos (SQLITE + PAGINAÇÃO)
- ✅ **Banco de dados SQLite** para performance com grandes volumes
- ✅ **Paginação inteligente** - exibe 50 insumos por página
- ✅ **4.984 insumos importados** do SINAPI (materiais e serviços de construção)
- ✅ **Busca rápida** por código, classificação ou descrição
- ✅ Cadastro com: Código, Classificação, Descrição, Unidade
- ✅ Campos opcionais: Preço, Fornecedor, Estoque
- ✅ **Índices otimizados** para buscas instantâneas
- ✅ Navegação por páginas com indicador visual

### 👷 Gestão de Funcionários
- ✅ Cadastro com **validação de CPF** (algoritmo oficial)
- ✅ Controle de admissão e demissão
- ✅ Cálculo automático de tempo de empresa
- ✅ Folha de pagamento automatizada
- ✅ Status visual (Ativo/Demitido)
- ✅ Relatórios por cargo

### 📊 Dashboard Analítico
- ✅ Visão geral de todas as operações
- ✅ Análise de obras (atrasos, taxa de conclusão)
- ✅ Análise financeira (economias, estouros de orçamento)
- ✅ Análise de RH (folha de pagamento, distribuição por cargo)
- ✅ Análise de estoque (valor, itens críticos, top 5)
- ✅ Métricas em tempo real com cards visuais

---

## 🖼️ Capturas de Tela

### Tela Inicial
- Logo da empresa centralizado
- Cards com estatísticas gerais (Obras, Insumos, Funcionários)
- Menu lateral com NavigationRail (Material Design 3)

### Páginas de Gerenciamento
- **DataTables** com ordenação e paginação
- **Dialogs modais** para CRUD (Create, Read, Update, Delete)
- **SnackBars** para notificações (verde=sucesso, vermelho=erro, laranja=aviso)
- **Cards de resumo** com ícones e cores temáticas

---

## 🛠️ Tecnologias

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.13.5 | Linguagem principal |
| **Flet** | 0.28.3 | Framework GUI (Desktop/Web/Mobile) |
| **SQLite** | 3.x | Banco de dados embutido para Insumos |
| **Material Design 3** | - | Sistema de design |
| **JSON** | - | Persistência de Obras e Funcionários |
| **Dataclasses** | - | Modelagem de dados |

### Por que Flet?
- 🌐 **Multiplataforma**: Desktop (Windows/Linux/Mac), Web, Mobile
- 🎨 **Material Design nativo**: Interface moderna sem CSS
- 🚀 **Rápido desenvolvimento**: Python puro, sem JavaScript
- 📦 **Deploy simplificado**: Executável standalone possível

---

## 📁 Estrutura do Projeto

```
04_gestao_obra/
│
├── .venv/                          # Ambiente virtual Python
│
├── cadastro_obra/                  # 🏗️ Módulo de Obras
│   ├── __init__.py
│   ├── obra.py                     # Modelo Obra (dataclass)
│   ├── cadastro.py                 # CRUD Obras
│   ├── main_obra.py                # CLI standalone
│   └── README.md
│
├── cadastro_insumo/                # 📦 Módulo de Insumos
│   ├── __init__.py
│   ├── insumo.py                   # Modelo Insumo
│   ├── cadastro.py                 # CRUD Insumos (interface SQLite)
│   ├── database.py                 # 🆕 DatabaseInsumos (SQLite + paginação)
│   ├── main_insumo.py              # CLI standalone
│   └── __init__.py
│
├── cadastro_funcionario/           # 👷 Módulo de Funcionários
│   ├── __init__.py
│   ├── funcionario.py              # Modelo Funcionario + CPF
│   ├── cadastro.py                 # CRUD Funcionários + RH
│   ├── main_funcionario.py         # CLI standalone
│   └── __init__.py
│
├── pages/                          # 🎨 Páginas Flet
│   ├── __init__.py
│   ├── pagina_obras.py             # UI Obras (DataTable + Dialogs)
│   ├── pagina_insumos.py           # UI Insumos (Estoque)
│   ├── pagina_funcionarios.py      # UI Funcionários (RH)
│   └── pagina_dashboard.py         # Dashboard Analítico
│
├── components/                     # 🧩 Componentes Reutilizáveis
│   └── __init__.py
│
├── app_flet.py                     # 🚀 APLICATIVO PRINCIPAL (GUI)
├── main.py                         # Sistema CLI integrado
├── popular_dados.py                # Script para popular banco
├── importar_csv_sqlite.py          # 🆕 Importa CSV para SQLite
├── importar_insumos.py             # Importa CSV para JSON (legacy)
│
├── logojpg.PNG                     # Logo da empresa
│
├── insumos.csv                     # 📄 4.984 insumos SINAPI
├── insumos.db                      # 🆕 💾 Banco SQLite de insumos
├── obras.json                      # 💾 Dados de obras
├── funcionarios.json               # 💾 Dados de funcionários
│
├── run.ps1                         # Script PowerShell
├── run.bat                         # Script Batch
│
└── README.md                       # 📖 Este arquivo
```

---

## 🚀 Instalação

### Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### Passo 1: Clone/Baixe o Projeto

```powershell
cd D:\04_gestao_obra
```

### Passo 2: Crie o Ambiente Virtual

```powershell
python -m venv .venv
```

### Passo 3: Ative o Ambiente Virtual

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

### Passo 4: Instale as Dependências

```powershell
pip install --upgrade pip
pip install flet
```

---

## 💻 Uso

### 🎨 Interface Gráfica (RECOMENDADO)

Execute o aplicativo Flet com interface moderna:

```powershell
# Método 1: Dentro do ambiente virtual ativado
python app_flet.py

# Método 2: Caminho completo (sem ativar venv)
D:\04_gestao_obra\.venv\Scripts\python.exe app_flet.py
```

**Recursos da Interface:**
- 🏠 **Tela Inicial**: Logo, estatísticas gerais
- 🏗️ **Obras**: CRUD completo, finalização, estatísticas
- 📦 **Insumos**: Controle de estoque, entrada/saída, alertas
- 👷 **Funcionários**: Cadastro, CPF, demissão, folha de pagamento
- 📊 **Dashboard**: Análises financeiras, RH, estoque, obras

### 📟 Interface CLI (Texto)

Para usar a versão terminal:

```powershell
python main.py
```

**Recursos CLI:**
- Menu hierárquico navegável
- Todas as funcionalidades de CRUD
- Relatórios em texto formatado

### 🗂️ Popular com Dados de Exemplo

```powershell
python popular_dados.py
```

**Cria automaticamente:**
- ✅ 3 obras (1 finalizada, 2 em andamento)
- ✅ 5 insumos com estoque variado
- ✅ 4 funcionários ativos em cargos diferentes

### 📥 Importar Insumos SINAPI (4.984 itens)

O sistema já vem com um banco SQLite populado, mas você pode reimportar:

```powershell
# Reimporta do CSV para SQLite (sobrescreve banco existente)
python importar_csv_sqlite.py
```

**O que é importado:**
- 📄 Arquivo: `insumos.csv` (4.984 linhas)
- 🏗️ Classificações: MATERIAL, SERVIÇOS, EQUIPAMENTOS, MÃO DE OBRA
- 📊 Campos: Código do Insumo, Classificação, Descrição, Unidade
- 💾 Destino: `insumos.db` (SQLite com índices otimizados)

**Tempo de importação:** ~10 segundos para 4.984 registros

---

## 📦 Módulos

### 1. 🏗️ Módulo Obra

**Arquivo:** `cadastro_obra/obra.py`

**Classe Obra:**
```python
@dataclass
class Obra:
    nome: str
    inicio: date                       # Data de início
    termino_previsto: date             # Data prevista
    custo_estimado: float              # Custo estimado
    termino_real: Optional[date]       # Data real (quando finalizada)
    custo_real: Optional[float]        # Custo real (quando finalizada)
    id: Optional[int] = None
```

**Validações:**
- `termino_previsto` deve ser posterior a `inicio`
- Custos devem ser positivos
- Datas em formato ISO (YYYY-MM-DD)

**Gerenciador:** `CadastroObra`
- `adicionar(obra)` → Adiciona nova obra
- `listar()` → Lista todas as obras
- `buscar_por_id(id)` → Busca por ID
- `buscar_por_nome(nome)` → Busca por nome (case-insensitive)
- `atualizar(id, obra)` → Atualiza obra existente
- `remover(id)` → Remove obra
- `finalizar_obra(id, termino_real, custo_real)` → Finaliza obra

---

### 2. 📦 Módulo Insumo

**Arquivo:** `cadastro_insumo/insumo.py`

**Classe Insumo:**
```python
@dataclass
class Insumo:
    nome: str
    unidade: str                   # kg, m, unidade, litro, etc
    quantidade_estoque: float
    preco_unitario: float
    fornecedor: str
    id: Optional[int] = None
```

**Métodos:**
- `calcular_valor_estoque()` → Retorna quantidade × preço
- `adicionar_estoque(qtd)` → Entrada de estoque
- `remover_estoque(qtd)` → Saída de estoque (valida disponibilidade)

**Gerenciador:** `CadastroInsumo`
- `adicionar(insumo)` → Cadastra novo insumo
- `listar()` → Lista todos os insumos
- `adicionar_estoque(id, qtd)` → Entrada no estoque
- `remover_estoque(id, qtd)` → Saída do estoque
- `relatorio_estoque_baixo()` → Lista insumos com qtd < 10
- `valor_total_estoque()` → Soma valor de todos os insumos

---

### 3. 👷 Módulo Funcionário

**Arquivo:** `cadastro_funcionario/funcionario.py`

**Classe Funcionario:**
```python
@dataclass
class Funcionario:
    nome: str
    cpf: str                       # 11 dígitos numéricos
    cargo: str
    salario: float
    data_admissao: date
    data_demissao: Optional[date] = None
    id: Optional[int] = None
```

**Métodos:**
- `validar_cpf(cpf)` → **Validação oficial brasileira** (dígitos verificadores)
- `formatar_cpf()` → Retorna CPF formatado: `000.000.000-00`
- `esta_ativo()` → Retorna `True` se não foi demitido
- `tempo_empresa()` → Calcula dias trabalhados (ou até demissão)

**Gerenciador:** `CadastroFuncionario`
- `adicionar(funcionario)` → Cadastra novo funcionário
- `listar(apenas_ativos=False)` → Lista funcionários
- `demitir(id, data_demissao)` → Demite funcionário
- `folha_pagamento(apenas_ativos=True)` → Calcula folha total

---

## 🎨 Interface Gráfica

### Arquitetura Flet

**Componentes principais:**
- **NavigationRail**: Menu lateral fixo (Material Design 3)
- **DataTable**: Tabelas com ordenação e paginação
- **AlertDialog**: Modais para CRUD
- **SnackBar**: Notificações toast
- **Card**: Containers para métricas

### Padrão de Design

**Separação de Responsabilidades:**
```
app_flet.py (Main)
    ├── Inicializa cadastros
    ├── Configura NavigationRail
    └── Gerencia navegação

pages/pagina_*.py (Views)
    ├── Cria interface específica
    ├── Gerencia dialogs e formulários
    └── Atualiza tabelas
```

### Páginas Implementadas

#### 🏠 Página Inicial
- Logo centralizado (logojpg.PNG)
- 3 cards de estatísticas
- Mensagem de boas-vindas

#### 🏗️ PaginaObras
**Recursos:**
- DataTable com 7 colunas (ID, Nome, Início, Término Previsto, Custo Estimado, Status, Ações)
- **Botões de ação**:
  - ✏️ **Editar**: Abre dialog com dados preenchidos
  - ✅ **Finalizar**: Dialog para término real + custo real (desabilita após finalizar)
  - 🗑️ **Excluir**: Confirmação antes de deletar
- **Cards de resumo**: Total | Em Andamento | Finalizadas
- **Validações**: Datas (formato DD/MM/AAAA), custos > 0

#### 📦 PaginaInsumos
**Recursos:**
- **Banco SQLite** com 4.984 insumos do SINAPI
- **Paginação**: Exibe 50 itens por vez (100 páginas no total)
- **Barra de busca**: Filtra por código, classificação ou descrição
- **Indicador de página**: "Página X de Y (total insumos)"
- **Navegação**: Botões anterior/próxima
- DataTable com 6 colunas (ID, Código, Classificação, Descrição, Unidade, Ações)
- **Botões de ação**:
  - ✏️ **Editar**: Atualizar dados do insumo
  - 🗑️ **Excluir**: Confirmação
- **Performance otimizada**: Carrega apenas 50 registros por vez
- **Cards de resumo**: Total de Insumos cadastrados

#### 👷 PaginaFuncionarios
**Recursos:**
- DataTable com 8 colunas (ID, Nome, CPF, Cargo, Salário, Admissão, Status, Ações)
- **CPF formatado**: `000.000.000-00`
- **Status visual**: Badge verde (Ativo) ou vermelho (Demitido)
- **Botões de ação**:
  - ✏️ **Editar**: Atualizar dados (mantém CPF para validação)
  - 👤 **Demitir**: Dialog com data de demissão (desabilita após demitir)
  - 🗑️ **Excluir**: Confirmação
- **Cards de resumo**: Ativos | Folha de Pagamento | Salário Médio

#### 📊 PaginaDashboard
**4 Cards de Métricas:**
1. Obras Ativas (azul)
2. Funcionários Ativos (laranja)
3. Insumos Cadastrados (roxo)
4. Estoque Baixo (vermelho)

**4 Painéis de Análise:**

1. **🏗️ Análise de Obras**
   - Total de obras
   - Em andamento
   - Finalizadas
   - Obras atrasadas
   - Média de atraso (em dias)

2. **💰 Análise de Custos**
   - Custo estimado total
   - Custo real total
   - Economia total (quando gastou menos)
   - Estouro total (quando gastou mais)
   - Taxa de precisão (%)

3. **👥 Análise de RH**
   - Funcionários ativos
   - Funcionários demitidos
   - Folha de pagamento mensal
   - Salário médio
   - Top 5 cargos mais comuns

4. **📦 Análise de Estoque**
   - Total de insumos
   - Valor total em estoque
   - Itens com estoque baixo
   - Itens sem estoque (zerados)
   - Top 5 insumos mais valiosos

---

## 🔧 Desenvolvimento

### Adicionar Nova Página

**1. Criar arquivo em `pages/`:**

```python
# pages/pagina_relatorios.py
import flet as ft

class PaginaRelatorios:
    def __init__(self, page: ft.Page, cadastro_obra):
        self.page = page
        self.cadastro = cadastro_obra
    
    def criar_pagina(self):
        return ft.Column([
            ft.Text("📋 Relatórios", size=32, weight=ft.FontWeight.BOLD),
            # ... seu conteúdo
        ])
```

**2. Importar em `app_flet.py`:**

```python
from pages.pagina_relatorios import PaginaRelatorios
```

**3. Inicializar no `__init__`:**

```python
self.pg_relatorios = PaginaRelatorios(page, self.cadastro_obra)
```

**4. Adicionar destino no `NavigationRail`:**

```python
ft.NavigationRailDestination(
    icon=ft.Icons.DESCRIPTION_OUTLINED,
    selected_icon=ft.Icons.DESCRIPTION,
    label="Relatórios"
),
```

**5. Adicionar case em `mudar_pagina()`:**

```python
elif indice == 5:
    self.conteudo.content = self.pg_relatorios.criar_pagina()
```

### Padrões de Código

**Dialog com validação:**
```python
def abrir_dialog_cadastro(self, e):
    dialog = ft.AlertDialog(
        title=ft.Text("Novo Item"),
        content=ft.Column([
            ft.TextField(label="Campo 1"),
            ft.TextField(label="Campo 2"),
        ]),
        actions=[
            ft.TextButton("Cancelar", on_click=self.fechar_dialog),
            ft.ElevatedButton("Salvar", on_click=self.salvar_item),
        ],
    )
    self.page.overlay.append(dialog)
    dialog.open = True
    self.page.update()
```

**SnackBar de feedback:**
```python
def mostrar_snackbar(self, mensagem, cor):
    self.page.snack_bar = ft.SnackBar(
        content=ft.Text(mensagem, color=ft.Colors.WHITE),
        bgcolor=cor,
    )
    self.page.snack_bar.open = True
    self.page.update()

# Uso:
self.mostrar_snackbar("Salvo com sucesso!", ft.Colors.GREEN_700)
self.mostrar_snackbar("Erro ao salvar", ft.Colors.RED_700)
```

---

## 🐛 Troubleshooting

### ❌ Erro: `ModuleNotFoundError: No module named 'flet'`

**Solução:**
```powershell
# Certifique-se de estar no ambiente virtual
.\.venv\Scripts\Activate.ps1

# Instale o Flet
pip install flet
```

---

### ❌ Erro: `AttributeError: module 'flet' has no attribute 'icons'`

**Causa:** Flet é **case-sensitive**

**Solução:** Use maiúsculas
```python
# ❌ ERRADO
ft.icons.HOME
ft.colors.BLUE

# ✅ CORRETO
ft.Icons.HOME
ft.Colors.BLUE
```

---

### ❌ Janela não abre / Nenhum erro exibido

**Solução:** Use o Python da venv explicitamente
```powershell
D:\04_gestao_obra\.venv\Scripts\python.exe app_flet.py
```

---

### ❌ Arquivos JSON corrompidos

**Solução:**
```powershell
# Delete os arquivos JSON
Remove-Item obras.json, insumos.json, funcionarios.json

# Recrie com dados de exemplo
python popular_dados.py
```

---

### ❌ CPF inválido sempre retorna erro

**Verifique:**
1. CPF tem 11 dígitos numéricos? (sem pontos/traços)
2. Não é sequência repetida? (111.111.111-11 é inválido)
3. Dígitos verificadores corretos?

**Teste com CPF válido:**
```
12345678909  # CPF válido para testes
```

---

## 📊 Formato dos Arquivos JSON

### obras.json
```json
[
  {
    "id": 1,
    "nome": "Residencial Jardim das Flores",
    "inicio": "2024-01-15",
    "termino_previsto": "2024-12-31",
    "custo_estimado": 250000.0,
    "termino_real": null,
    "custo_real": null
  }
]
```

### insumos.json
```json
[
  {
    "id": 1,
    "nome": "Cimento CP-II 50kg",
    "unidade": "saco",
    "quantidade_estoque": 50.0,
    "preco_unitario": 32.5,
    "fornecedor": "Cimentos Fortes"
  }
]
```

### funcionarios.json
```json
[
  {
    "id": 1,
    "nome": "João Silva",
    "cpf": "12345678909",
    "cargo": "Engenheiro Civil",
    "salario": 8500.0,
    "data_admissao": "2023-01-15",
    "data_demissao": null
  }
]
```

---

## 📝 Changelog

### v2.0.0 (Atual) - Interface Flet
✨ **Novidades:**
- Interface gráfica completa em Flet
- NavigationRail com 5 páginas
- DataTables interativos
- Dashboard analítico
- Cards de estatísticas
- Dialogs para CRUD
- SnackBars de feedback
- Validações visuais

### v1.0.0 - Sistema CLI
- Sistema CLI integrado
- Três módulos independentes (obras, insumos, funcionários)
- Persistência em JSON
- Validação de CPF

---

## 📜 Licença

Projeto desenvolvido para **Tiago Rizzetto**.  
Todos os direitos reservados © 2025.

---

## 👨‍💻 Autor

**Tiago Rizzetto**  
Sistema de Gestão de Obras  
Versão 2.0 - Interface Flet  
Data: Janeiro/2025

---

## 🎯 Status do Projeto

**✅ COMPLETO** - Sistema totalmente funcional com interface gráfica moderna!

**Funcionalidades implementadas:**
- [x] CRUD de Obras
- [x] CRUD de Insumos com controle de estoque
- [x] CRUD de Funcionários com validação de CPF
- [x] Dashboard analítico
- [x] Interface gráfica Flet
- [x] Persistência em JSON
- [x] Validações de dados
- [x] Notificações visuais
- [x] Sistema CLI (legacy)

**Possíveis Expansões Futuras:**
- [ ] Geração de PDFs com relatórios
- [ ] Gráficos com matplotlib/plotly
- [ ] Export para Excel
- [ ] Sistema de backup automático
- [ ] Multi-usuário com login
- [ ] Deploy Web (Flet suporta!)
- [ ] App mobile (Flet suporta!)

---

**Desenvolvido com ❤️ em Python e Flet**
