"""
Sistema de Cadastro de Obras
"""
from datetime import datetime
from .cadastro import CadastroObra
from .obra import Obra


def menu():
    """Exibe o menu principal"""
    print("\n" + "="*50)
    print("SISTEMA DE CADASTRO DE OBRAS")
    print("="*50)
    print("1. Cadastrar nova obra")
    print("2. Listar todas as obras")
    print("3. Buscar obra por ID")
    print("4. Buscar obra por nome")
    print("5. Atualizar obra")
    print("6. Finalizar obra")
    print("7. Remover obra")
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


def cadastrar_obra(cadastro: CadastroObra):
    """Cadastra uma nova obra"""
    print("\n--- CADASTRAR NOVA OBRA ---")
    
    nome = input("Nome da obra: ").strip()
    inicio = ler_data("Data de início (DD/MM/AAAA): ")
    termino_previsto = ler_data("Término previsto (DD/MM/AAAA): ")
    custo_estimado = ler_float("Custo estimado (R$): ")
    
    obra = Obra(
        nome=nome,
        inicio=inicio,
        termino_previsto=termino_previsto,
        custo_estimado=custo_estimado
    )
    
    sucesso, mensagem = cadastro.adicionar(obra)
    print(f"\n{'✓' if sucesso else '✗'} {mensagem}")


def listar_obras(cadastro: CadastroObra):
    """Lista todas as obras"""
    obras = cadastro.listar()
    
    if not obras:
        print("\nNenhuma obra cadastrada.")
        return
    
    print(f"\n--- OBRAS CADASTRADAS ({len(obras)}) ---")
    for obra in obras:
        print(f"\n[ID: {obra.id}]")
        print(obra)


def buscar_por_id(cadastro: CadastroObra):
    """Busca obra por ID"""
    try:
        id = int(input("\nDigite o ID da obra: "))
        obra = cadastro.buscar_por_id(id)
        
        if obra:
            print(f"\n[ID: {obra.id}]")
            print(obra)
        else:
            print(f"\n✗ Obra com ID {id} não encontrada")
    except ValueError:
        print("\n✗ ID inválido!")


def buscar_por_nome(cadastro: CadastroObra):
    """Busca obras por nome"""
    nome = input("\nDigite o nome (ou parte do nome): ").strip()
    obras = cadastro.buscar_por_nome(nome)
    
    if not obras:
        print(f"\n✗ Nenhuma obra encontrada com '{nome}'")
        return
    
    print(f"\n--- RESULTADOS ({len(obras)}) ---")
    for obra in obras:
        print(f"\n[ID: {obra.id}]")
        print(obra)


def atualizar_obra(cadastro: CadastroObra):
    """Atualiza uma obra existente"""
    try:
        id = int(input("\nDigite o ID da obra a atualizar: "))
        obra = cadastro.buscar_por_id(id)
        
        if not obra:
            print(f"\n✗ Obra com ID {id} não encontrada")
            return
        
        print(f"\nObra atual:")
        print(obra)
        print("\n--- NOVOS DADOS (Enter para manter o atual) ---")
        
        nome = input(f"Nome [{obra.nome}]: ").strip() or obra.nome
        
        inicio_str = input(f"Data de início [{obra.inicio.strftime('%d/%m/%Y')}]: ").strip()
        inicio = datetime.strptime(inicio_str, '%d/%m/%Y') if inicio_str else obra.inicio
        
        termino_str = input(f"Término previsto [{obra.termino_previsto.strftime('%d/%m/%Y')}]: ").strip()
        termino_previsto = datetime.strptime(termino_str, '%d/%m/%Y') if termino_str else obra.termino_previsto
        
        custo_str = input(f"Custo estimado [{obra.custo_estimado:.2f}]: ").strip()
        custo_estimado = float(custo_str.replace(',', '.')) if custo_str else obra.custo_estimado
        
        obra_atualizada = Obra(
            nome=nome,
            inicio=inicio,
            termino_previsto=termino_previsto,
            custo_estimado=custo_estimado,
            termino_real=obra.termino_real,
            custo_real=obra.custo_real
        )
        
        sucesso, mensagem = cadastro.atualizar(id, obra_atualizada)
        print(f"\n{'✓' if sucesso else '✗'} {mensagem}")
        
    except ValueError as e:
        print(f"\n✗ Erro: {e}")


def finalizar_obra(cadastro: CadastroObra):
    """Finaliza uma obra"""
    try:
        id = int(input("\nDigite o ID da obra a finalizar: "))
        obra = cadastro.buscar_por_id(id)
        
        if not obra:
            print(f"\n✗ Obra com ID {id} não encontrada")
            return
        
        if obra.termino_real:
            print(f"\n✗ Obra '{obra.nome}' já foi finalizada em {obra.termino_real.strftime('%d/%m/%Y')}")
            return
        
        print(f"\nObra: {obra.nome}")
        termino_real = ler_data("Data de término real (DD/MM/AAAA): ")
        custo_real = ler_float("Custo real (R$): ")
        
        sucesso, mensagem = cadastro.finalizar_obra(id, termino_real, custo_real)
        print(f"\n{'✓' if sucesso else '✗'} {mensagem}")
        
    except ValueError:
        print("\n✗ ID inválido!")


def remover_obra(cadastro: CadastroObra):
    """Remove uma obra"""
    try:
        id = int(input("\nDigite o ID da obra a remover: "))
        obra = cadastro.buscar_por_id(id)
        
        if not obra:
            print(f"\n✗ Obra com ID {id} não encontrada")
            return
        
        print(f"\nObra: {obra.nome}")
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
    cadastro = CadastroObra()
    
    while True:
        menu()
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            cadastrar_obra(cadastro)
        elif opcao == '2':
            listar_obras(cadastro)
        elif opcao == '3':
            buscar_por_id(cadastro)
        elif opcao == '4':
            buscar_por_nome(cadastro)
        elif opcao == '5':
            atualizar_obra(cadastro)
        elif opcao == '6':
            finalizar_obra(cadastro)
        elif opcao == '7':
            remover_obra(cadastro)
        elif opcao == '0':
            print("\nEncerrando sistema...")
            break
        else:
            print("\n✗ Opção inválida!")
        
        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()
