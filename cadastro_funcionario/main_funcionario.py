"""
Sistema de Cadastro de Funcionários
"""
from datetime import datetime
from .cadastro import CadastroFuncionario
from .funcionario import Funcionario


def menu():
    """Exibe o menu principal"""
    print("\n" + "="*50)
    print("SISTEMA DE CADASTRO DE FUNCIONÁRIOS")
    print("="*50)
    print("1. Cadastrar novo funcionário")
    print("2. Listar todos os funcionários")
    print("3. Listar funcionários ativos")
    print("4. Buscar funcionário por ID")
    print("5. Buscar funcionário por CPF")
    print("6. Buscar funcionário por nome")
    print("7. Buscar por cargo")
    print("8. Atualizar funcionário")
    print("9. Demitir funcionário")
    print("10. Folha de pagamento")
    print("11. Relatório por cargo")
    print("12. Remover funcionário")
    print("0. Sair")
    print("="*50)


def ler_data(mensagem: str) -> datetime:
    """Lê uma data do usuário"""
    while True:
        try:
            data_str = input(mensagem)
            return datetime.strptime(data_str, '%d/%m/%Y')
        except ValueError:
            print("Data inválida! Use o formato DD/MM/AAAA")


def ler_float(mensagem: str) -> float:
    """Lê um valor float do usuário"""
    while True:
        try:
            return float(input(mensagem).replace(',', '.'))
        except ValueError:
            print("Valor inválido! Digite um número")


def cadastrar_funcionario(cadastro: CadastroFuncionario):
    """Cadastra um novo funcionário"""
    print("\n--- CADASTRAR NOVO FUNCIONÁRIO ---")
    
    nome = input("Nome completo: ").strip()
    cpf = input("CPF (apenas números ou com formatação): ").strip()
    cargo = input("Cargo: ").strip()
    salario = ler_float("Salário (R$): ")
    data_admissao = ler_data("Data de admissão (DD/MM/AAAA): ")
    
    funcionario = Funcionario(
        nome=nome,
        cpf=cpf,
        cargo=cargo,
        salario=salario,
        data_admissao=data_admissao
    )
    
    sucesso, mensagem = cadastro.adicionar(funcionario)
    print(f"\n{'✓' if sucesso else '✗'} {mensagem}")


def listar_funcionarios(cadastro: CadastroFuncionario, apenas_ativos: bool = False):
    """Lista funcionários"""
    funcionarios = cadastro.listar(apenas_ativos)
    
    if not funcionarios:
        tipo = "ativos" if apenas_ativos else "cadastrados"
        print(f"\nNenhum funcionário {tipo}.")
        return
    
    titulo = "ATIVOS" if apenas_ativos else "CADASTRADOS"
    print(f"\n--- FUNCIONÁRIOS {titulo} ({len(funcionarios)}) ---")
    for func in funcionarios:
        print(f"\n[ID: {func.id}]")
        print(func)
    
    if apenas_ativos:
        folha = cadastro.folha_pagamento(True)
        print(f"\n{'='*50}")
        print(f"FOLHA DE PAGAMENTO: R$ {folha:,.2f}")
        print(f"{'='*50}")


def buscar_por_id(cadastro: CadastroFuncionario):
    """Busca funcionário por ID"""
    try:
        id = int(input("\nDigite o ID do funcionário: "))
        func = cadastro.buscar_por_id(id)
        
        if func:
            print(f"\n[ID: {func.id}]")
            print(func)
        else:
            print(f"\n✗ Funcionário com ID {id} não encontrado")
    except ValueError:
        print("\n✗ ID inválido!")


def buscar_por_cpf(cadastro: CadastroFuncionario):
    """Busca funcionário por CPF"""
    cpf = input("\nDigite o CPF: ").strip()
    func = cadastro.buscar_por_cpf(cpf)
    
    if func:
        print(f"\n[ID: {func.id}]")
        print(func)
    else:
        print(f"\n✗ Funcionário com CPF {cpf} não encontrado")


def buscar_por_nome(cadastro: CadastroFuncionario):
    """Busca funcionários por nome"""
    nome = input("\nDigite o nome (ou parte do nome): ").strip()
    funcionarios = cadastro.buscar_por_nome(nome)
    
    if not funcionarios:
        print(f"\n✗ Nenhum funcionário encontrado com '{nome}'")
        return
    
    print(f"\n--- RESULTADOS ({len(funcionarios)}) ---")
    for func in funcionarios:
        print(f"\n[ID: {func.id}]")
        print(func)


def buscar_por_cargo(cadastro: CadastroFuncionario):
    """Busca funcionários por cargo"""
    cargo = input("\nDigite o cargo: ").strip()
    funcionarios = cadastro.buscar_por_cargo(cargo)
    
    if not funcionarios:
        print(f"\n✗ Nenhum funcionário encontrado com cargo '{cargo}'")
        return
    
    print(f"\n--- RESULTADOS ({len(funcionarios)}) ---")
    for func in funcionarios:
        print(f"\n[ID: {func.id}]")
        print(f"  {func.nome} - {func.cargo} - R$ {func.salario:,.2f}")
        print(f"  Status: {'Ativo' if func.esta_ativo() else 'Demitido'}")


def atualizar_funcionario(cadastro: CadastroFuncionario):
    """Atualiza um funcionário existente"""
    try:
        id = int(input("\nDigite o ID do funcionário a atualizar: "))
        func = cadastro.buscar_por_id(id)
        
        if not func:
            print(f"\n✗ Funcionário com ID {id} não encontrado")
            return
        
        print(f"\nFuncionário atual:")
        print(func)
        print("\n--- NOVOS DADOS (Enter para manter o atual) ---")
        
        nome = input(f"Nome [{func.nome}]: ").strip() or func.nome
        cpf = input(f"CPF [{func.formatar_cpf()}]: ").strip() or func.cpf
        cargo = input(f"Cargo [{func.cargo}]: ").strip() or func.cargo
        
        salario_str = input(f"Salário [{func.salario:.2f}]: ").strip()
        salario = float(salario_str.replace(',', '.')) if salario_str else func.salario
        
        admissao_str = input(f"Data de admissão [{func.data_admissao.strftime('%d/%m/%Y')}]: ").strip()
        data_admissao = datetime.strptime(admissao_str, '%d/%m/%Y') if admissao_str else func.data_admissao
        
        func_atualizado = Funcionario(
            nome=nome,
            cpf=cpf,
            cargo=cargo,
            salario=salario,
            data_admissao=data_admissao,
            data_demissao=func.data_demissao
        )
        
        sucesso, mensagem = cadastro.atualizar(id, func_atualizado)
        print(f"\n{'✓' if sucesso else '✗'} {mensagem}")
        
    except ValueError as e:
        print(f"\n✗ Erro: {e}")


def demitir_funcionario(cadastro: CadastroFuncionario):
    """Demite um funcionário"""
    try:
        id = int(input("\nDigite o ID do funcionário a demitir: "))
        func = cadastro.buscar_por_id(id)
        
        if not func:
            print(f"\n✗ Funcionário com ID {id} não encontrado")
            return
        
        if not func.esta_ativo():
            print(f"\n✗ Funcionário '{func.nome}' já foi demitido")
            return
        
        print(f"\nFuncionário: {func.nome}")
        print(f"Cargo: {func.cargo}")
        print(f"Tempo de empresa: {func.tempo_empresa()} dias")
        
        data_demissao = ler_data("Data de demissão (DD/MM/AAAA): ")
        
        confirmacao = input("\nConfirmar demissão? (S/N): ").strip().upper()
        if confirmacao == 'S':
            sucesso, mensagem = cadastro.demitir(id, data_demissao)
            print(f"\n{'✓' if sucesso else '✗'} {mensagem}")
        else:
            print("\n✗ Demissão cancelada")
        
    except ValueError:
        print("\n✗ ID inválido!")


def folha_pagamento(cadastro: CadastroFuncionario):
    """Exibe folha de pagamento"""
    total = cadastro.folha_pagamento(True)
    ativos = cadastro.listar(True)
    
    print(f"\n{'='*50}")
    print(f"FOLHA DE PAGAMENTO")
    print(f"{'='*50}")
    print(f"Funcionários ativos: {len(ativos)}")
    print(f"Total: R$ {total:,.2f}")
    print(f"Média salarial: R$ {(total / len(ativos) if ativos else 0):,.2f}")
    print(f"{'='*50}")


def relatorio_por_cargo(cadastro: CadastroFuncionario):
    """Exibe relatório por cargo"""
    relatorio = cadastro.relatorio_por_cargo()
    
    if not relatorio:
        print("\nNenhum funcionário cadastrado.")
        return
    
    print(f"\n{'='*50}")
    print(f"RELATÓRIO POR CARGO")
    print(f"{'='*50}")
    
    for cargo, dados in relatorio.items():
        print(f"\n{cargo}:")
        print(f"  Total: {dados['quantidade']} funcionário(s)")
        print(f"  Ativos: {dados['ativos']}")
        print(f"  Inativos: {dados['quantidade'] - dados['ativos']}")
        print(f"  Total em salários: R$ {dados['total_salarios']:,.2f}")
        if dados['ativos'] > 0:
            media = dados['total_salarios'] / dados['quantidade']
            print(f"  Média salarial: R$ {media:,.2f}")


def remover_funcionario(cadastro: CadastroFuncionario):
    """Remove um funcionário"""
    try:
        id = int(input("\nDigite o ID do funcionário a remover: "))
        func = cadastro.buscar_por_id(id)
        
        if not func:
            print(f"\n✗ Funcionário com ID {id} não encontrado")
            return
        
        print(f"\nFuncionário: {func.nome}")
        confirmacao = input("Tem certeza que deseja remover? (S/N): ").strip().upper()
        
        if confirmacao == 'S':
            sucesso, mensagem = cadastro.remover(id)
            print(f"\n{'✓' if sucesso else '✗'} {mensagem}")
        else:
            print("\n✗ Remoção cancelada")
            
    except ValueError:
        print("\n✗ ID inválido!")


def main():
    """Função principal"""
    cadastro = CadastroFuncionario()
    
    while True:
        menu()
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            cadastrar_funcionario(cadastro)
        elif opcao == '2':
            listar_funcionarios(cadastro, False)
        elif opcao == '3':
            listar_funcionarios(cadastro, True)
        elif opcao == '4':
            buscar_por_id(cadastro)
        elif opcao == '5':
            buscar_por_cpf(cadastro)
        elif opcao == '6':
            buscar_por_nome(cadastro)
        elif opcao == '7':
            buscar_por_cargo(cadastro)
        elif opcao == '8':
            atualizar_funcionario(cadastro)
        elif opcao == '9':
            demitir_funcionario(cadastro)
        elif opcao == '10':
            folha_pagamento(cadastro)
        elif opcao == '11':
            relatorio_por_cargo(cadastro)
        elif opcao == '12':
            remover_funcionario(cadastro)
        elif opcao == '0':
            print("\nEncerrando sistema...")
            break
        else:
            print("\n✗ Opção inválida!")
        
        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()
