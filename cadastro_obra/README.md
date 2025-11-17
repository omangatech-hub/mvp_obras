# Cadastro de Obras

Sistema completo para cadastro e gerenciamento de obras.

## Campos da Obra

- **Nome da Obra**: Identificação da obra
- **Início**: Data de início da obra
- **Término Previsto**: Data estimada para conclusão
- **Término Real**: Data real de conclusão (preenchido ao finalizar)
- **Custo Estimado**: Valor estimado do projeto
- **Custo Real**: Valor real gasto (preenchido ao finalizar)

## Estrutura

- `obra.py`: Classe de dados da obra com validações
- `cadastro.py`: Gerenciador de cadastro (CRUD completo)
- `main_obra.py`: Interface de linha de comando
- `obras.json`: Arquivo de persistência (criado automaticamente)

## Como usar

```powershell
cd cadastro_obra
python main_obra.py
```

## Funcionalidades

1. ✅ Cadastrar nova obra
2. ✅ Listar todas as obras
3. ✅ Buscar obra por ID
4. ✅ Buscar obra por nome (busca parcial)
5. ✅ Atualizar dados da obra
6. ✅ Finalizar obra (registrar término real e custo real)
7. ✅ Remover obra
8. ✅ Validações completas
9. ✅ Persistência em JSON
10. ✅ Formatação de valores monetários

## Exemplo de uso programático

```python
from cadastro import CadastroObra
from obra import Obra
from datetime import datetime

# Criar cadastro
cadastro = CadastroObra()

# Adicionar obra
obra = Obra(
    nome="Edifício Residencial São Paulo",
    inicio=datetime(2025, 1, 15),
    termino_previsto=datetime(2026, 6, 30),
    custo_estimado=2500000.00
)

sucesso, mensagem = cadastro.adicionar(obra)
print(mensagem)

# Listar obras
for obra in cadastro.listar():
    print(obra)

# Finalizar obra
cadastro.finalizar_obra(
    id=1,
    termino_real=datetime(2026, 7, 15),
    custo_real=2650000.00
)
```

## Validações

- Nome não pode ser vazio
- Término previsto deve ser posterior ao início
- Custo estimado deve ser maior que zero
- Término real não pode ser anterior ao início
- Custo real não pode ser negativo
