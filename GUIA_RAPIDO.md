# 🚀 Guia Rápido - Sistema de Gestão de Obras

## Início Rápido (60 segundos)

### 1️⃣ Ativar Ambiente Virtual
```powershell
# PowerShell
.\.venv\Scripts\Activate.ps1

# CMD
.\.venv\Scripts\activate.bat
```

### 2️⃣ Executar Aplicativo
```powershell
python app_flet.py
```

### 3️⃣ Popular com Dados (Opcional)
```powershell
python popular_dados.py
```

---

## 🎯 Atalhos do Sistema

### Menu Lateral (NavigationRail)
- **🏠 Início**: Tela inicial com logo e estatísticas
- **🏗️ Obras**: Cadastro e gestão de obras
- **📦 Insumos**: Controle de estoque de materiais
- **👷 Funcionários**: Gestão de RH e folha de pagamento
- **📊 Dashboard**: Análises e relatórios visuais

---

## 📋 Operações Comuns

### Cadastrar Nova Obra
1. Clique em **🏗️ Obras** no menu lateral
2. Clique no botão **➕ Novo Cadastro**
3. Preencha:
   - Nome da obra
   - Data de início (DD/MM/AAAA)
   - Término previsto (DD/MM/AAAA)
   - Custo estimado (R$)
4. Clique em **Salvar**

### Finalizar Obra
1. Na página **🏗️ Obras**, encontre a obra
2. Clique no botão **✅ Finalizar** (verde)
3. Informe:
   - Data de término real (DD/MM/AAAA)
   - Custo real (R$)
4. Clique em **Salvar Finalização**

### Adicionar Estoque
1. Clique em **📦 Insumos** no menu lateral
2. Encontre o insumo na tabela
3. Clique no botão **➕** (verde)
4. Informe a quantidade a adicionar
5. Clique em **Confirmar Entrada**

### Remover Estoque
1. Na página **📦 Insumos**, encontre o insumo
2. Clique no botão **➖** (laranja)
3. Informe a quantidade a remover
4. Clique em **Confirmar Saída**

### Cadastrar Funcionário
1. Clique em **👷 Funcionários** no menu lateral
2. Clique em **➕ Novo Funcionário**
3. Preencha:
   - Nome completo
   - CPF (apenas números, 11 dígitos)
   - Cargo
   - Salário (R$)
   - Data de admissão (DD/MM/AAAA)
4. Clique em **Salvar**

### Demitir Funcionário
1. Na página **👷 Funcionários**, encontre o funcionário
2. Clique no botão **👤 Demitir** (laranja)
3. Informe a data de demissão (DD/MM/AAAA)
4. Clique em **Confirmar Demissão**

---

## ⚠️ Alertas Visuais

| Cor | Significado | Onde Aparece |
|-----|-------------|--------------|
| 🟢 **Verde** | Sucesso / Ativo | SnackBars, Status, Botões |
| 🔴 **Vermelho** | Erro / Crítico | SnackBars, Estoque Baixo, Demitido |
| 🟠 **Laranja** | Aviso / Atenção | SnackBars, Botões de Demitir/Saída |
| 🔵 **Azul** | Informação / Edição | Botões de Editar |

---

## 🎨 Ícones e Ações

### Obras
- **✏️ Editar**: Atualizar dados da obra
- **✅ Finalizar**: Marcar obra como concluída (só obras em andamento)
- **🗑️ Excluir**: Remover obra do sistema

### Insumos
- **➕ Entrada**: Adicionar quantidade ao estoque
- **➖ Saída**: Remover quantidade do estoque
- **✏️ Editar**: Atualizar dados do insumo
- **🗑️ Excluir**: Remover insumo do sistema

### Funcionários
- **✏️ Editar**: Atualizar dados do funcionário
- **👤 Demitir**: Registrar demissão (só funcionários ativos)
- **🗑️ Excluir**: Remover funcionário do sistema

---

## 📊 Interpretando o Dashboard

### Cards de Métricas (Topo)
- **Obras Ativas**: Quantidade de obras em andamento
- **Funcionários Ativos**: Funcionários não demitidos
- **Insumos Cadastrados**: Total de materiais no sistema
- **Estoque Baixo**: Insumos com quantidade < 10

### Painéis de Análise

#### 🏗️ Análise de Obras
- **Total**: Todas as obras cadastradas
- **Em andamento**: Obras sem término real
- **Finalizadas**: Obras com término real
- **Obras atrasadas**: Término previsto já passou
- **Média de atraso**: Dias de atraso médio

#### 💰 Análise de Custos
- **Custo estimado total**: Soma de todos os custos estimados
- **Custo real total**: Soma de todos os custos reais (obras finalizadas)
- **Economia total**: Quando gastou menos que o estimado
- **Estouro total**: Quando gastou mais que o estimado
- **Taxa de precisão**: % de assertividade nas estimativas

#### 👥 Análise de RH
- **Funcionários ativos**: Não demitidos
- **Funcionários demitidos**: Com data de demissão
- **Folha de pagamento**: Soma dos salários (só ativos)
- **Salário médio**: Folha ÷ quantidade de ativos
- **Top 5 cargos**: Cargos mais comuns

#### 📦 Análise de Estoque
- **Total de insumos**: Quantidade de materiais cadastrados
- **Valor em estoque**: Soma de (quantidade × preço unitário)
- **Estoque baixo**: Insumos com quantidade < 10
- **Sem estoque**: Insumos zerados
- **Top 5 mais valiosos**: Insumos com maior valor em estoque

---

## 🔧 Solução Rápida de Problemas

### Aplicativo não abre
```powershell
# Use o caminho completo do Python da venv
D:\04_gestao_obra\.venv\Scripts\python.exe app_flet.py
```

### Erro "ModuleNotFoundError: No module named 'flet'"
```powershell
# Ative a venv e instale o Flet
.\.venv\Scripts\Activate.ps1
pip install flet
```

### CPF sempre retorna inválido
- ✅ Use apenas números (sem pontos ou traços)
- ✅ Deve ter 11 dígitos
- ✅ Não pode ser sequência repetida (111.111.111-11)
- ✅ Teste com CPF válido: `12345678909`

### Data não aceita
- ✅ Use formato **DD/MM/AAAA** (exemplo: `15/01/2024`)
- ✅ Para obras: término deve ser depois do início
- ✅ Para demissão: deve ser depois da admissão

### Estoque negativo
- ❌ Sistema **não permite** estoque negativo
- ✅ Verifique a quantidade disponível antes de remover
- ℹ️ Quantidade atual aparece no dialog de saída

---

## 📁 Arquivos de Dados

### Localização
```
D:\04_gestao_obra\
├── obras.json          # Todas as obras
├── insumos.json        # Todos os insumos
└── funcionarios.json   # Todos os funcionários
```

### Backup Manual
```powershell
# Copiar arquivos JSON para backup
Copy-Item *.json -Destination "backup_$(Get-Date -Format 'yyyyMMdd')\"
```

### Resetar Sistema
```powershell
# CUIDADO: Apaga todos os dados!
Remove-Item obras.json, insumos.json, funcionarios.json

# Recriar com dados de exemplo
python popular_dados.py
```

---

## 🎓 Dicas Pro

### 1. Validação de CPF
O sistema usa o **algoritmo oficial brasileiro**:
- Calcula dígitos verificadores
- Rejeita CPFs inválidos automaticamente
- Formata automaticamente (000.000.000-00)

### 2. Controle de Estoque
- **Entrada**: Sempre verde (adiciona)
- **Saída**: Sempre laranja (remove)
- **Alerta**: Texto vermelho para < 10 unidades
- **Banner**: Aparece no topo se houver itens críticos

### 3. Finalização de Obras
- Botão **Finalizar** desabilita após uso
- Não pode "desfinalizar" uma obra (edição protegida)
- Custos e datas reais ficam fixos após finalização

### 4. Demissão de Funcionários
- Botão **Demitir** desabilita após uso
- Funcionário não é excluído, apenas marcado como demitido
- Não conta na folha de pagamento após demissão
- Histórico preservado para auditoria

### 5. Dashboard em Tempo Real
- Atualiza automaticamente ao mudar de página
- Todas as métricas são calculadas na hora
- Não precisa "atualizar" manualmente

---

## ⌨️ Atalhos do Teclado (Flet)

| Tecla | Ação |
|-------|------|
| **Tab** | Navegar entre campos |
| **Enter** | Confirmar dialog (botão padrão) |
| **Esc** | Fechar dialog |
| **Ctrl+C** | Copiar texto selecionado |

---

## 📞 Suporte

### Logs de Erro
Se encontrar erros, procure por:
```
D:\04_gestao_obra\*.log
```

### Reportar Problema
1. Descreva o que tentou fazer
2. Copie a mensagem de erro (se houver)
3. Informe qual página estava usando
4. Mencione se consegue reproduzir

---

## 📖 Documentação Completa

Para informações detalhadas, consulte:
- **README.md**: Documentação completa do sistema
- **cadastro_obra/README.md**: Detalhes do módulo de obras
- Arquivos `.py`: Código-fonte com docstrings

---

**Última atualização:** Janeiro/2025  
**Versão:** 2.0 (Interface Flet)  
**Desenvolvido para:** Tiago Rizzetto
