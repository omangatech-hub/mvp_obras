"""
Sistema de Cadastro de Insumos
"""
from .cadastro import CadastroInsumo
from .insumo import Insumo


def menu():
    """Exibe o menu principal"""
    print("\n" + "="*50)
    print("SISTEMA DE CADASTRO DE INSUMOS")
    print("="*50)
    print("1. Cadastrar novo insumo")
    print("2. Listar todos os insumos")
    print("3. Buscar insumo por ID")
    print("4. Buscar insumo por nome")
    print("5. Atualizar insumo")
    print("6. Entrada de estoque")
    print("7. Saída de estoque")
    print("8. Relatório de estoque baixo")
    print("9. Valor total em estoque")
    print("10. Remover insumo")
    print("0. Sair")
    print("="*50)


def ler_float(mensagem: str) -> float:
    """Lê um valor float do usuário"""
    while True:
        try:
            return float(input(mensagem).replace(',', '.'))
        except ValueError:
            print("Valor inválido! Digite um número")


def cadastrar_insumo(cadastro: CadastroInsumo):
    """Cadastra um novo insumo"""
    print("\n--- CADASTRAR NOVO INSUMO ---")
    
    nome = input("Nome do insumo: ").strip()
    unidade = input("Unidade (kg, m, m², m³, un, L, etc): ").strip()
    quantidade = ler_float("Quantidade em estoque: ")
    preco = ler_float("Preço unitário (R$): ")
    fornecedor = input("Fornecedor: ").strip()
    
    insumo = Insumo(
        nome=nome,
        unidade=unidade,
        quantidade_estoque=quantidade,
        preco_unitario=preco,
        fornecedor=fornecedor
    )
    
    sucesso, mensagem = cadastro.adicionar(insumo)
    print(f"\n{'✓' if sucesso else '✗'} {mensagem}")


def listar_insumos(cadastro: CadastroInsumo):
    """Lista todos os insumos"""
    insumos = cadastro.listar()
    
    if not insumos:
        print("\nNenhum insumo cadastrado.")
        return
    
    valor_total = cadastro.valor_total_estoque()
    print(f"\n--- INSUMOS CADASTRADOS ({len(insumos)}) ---")
    for insumo in insumos:
        print(f"\n[ID: {insumo.id}]")
        print(insumo)
    
    print(f"\n{'='*50}")
    print(f"VALOR TOTAL EM ESTOQUE: R$ {valor_total:,.2f}")
    print(f"{'='*50}")


def buscar_por_id(cadastro: CadastroInsumo):
    """Busca insumo por ID"""
    try:
        id = int(input("\nDigite o ID do insumo: "))
        insumo = cadastro.buscar_por_id(id)
        
        if insumo:
            print(f"\n[ID: {insumo.id}]")
            print(insumo)
        else:
            print(f"\n✗ Insumo com ID {id} não encontrado")
    except ValueError:
        print("\n✗ ID inválido!")


def buscar_por_nome(cadastro: CadastroInsumo):
    """Busca insumos por nome"""
    nome = input("\nDigite o nome (ou parte do nome): ").strip()
    insumos = cadastro.buscar_por_nome(nome)
    
    if not insumos:
        print(f"\n✗ Nenhum insumo encontrado com '{nome}'")
        return
    
    print(f"\n--- RESULTADOS ({len(insumos)}) ---")
    for insumo in insumos:
        print(f"\n[ID: {insumo.id}]")
        print(insumo)


def atualizar_insumo(cadastro: CadastroInsumo):
    """Atualiza um insumo existente"""
    try:
        id = int(input("\nDigite o ID do insumo a atualizar: "))
        insumo = cadastro.buscar_por_id(id)
        
        if not insumo:
            print(f"\n✗ Insumo com ID {id} não encontrado")
            return
        
        print(f"\nInsumo atual:")
        print(insumo)
        print("\n--- NOVOS DADOS (Enter para manter o atual) ---")
        
        nome = input(f"Nome [{insumo.nome}]: ").strip() or insumo.nome
        unidade = input(f"Unidade [{insumo.unidade}]: ").strip() or insumo.unidade
        
        qtd_str = input(f"Quantidade [{insumo.quantidade_estoque}]: ").strip()
        quantidade = float(qtd_str.replace(',', '.')) if qtd_str else insumo.quantidade_estoque
        
        preco_str = input(f"Preço unitário [{insumo.preco_unitario:.2f}]: ").strip()
        preco = float(preco_str.replace(',', '.')) if preco_str else insumo.preco_unitario
        
        fornecedor = input(f"Fornecedor [{insumo.fornecedor}]: ").strip() or insumo.fornecedor
        
        insumo_atualizado = Insumo(
            nome=nome,
            unidade=unidade,
            quantidade_estoque=quantidade,
            preco_unitario=preco,
            fornecedor=fornecedor
        )
        
        sucesso, mensagem = cadastro.atualizar(id, insumo_atualizado)
        print(f"\n{'✓' if sucesso else '✗'} {mensagem}")
        
    except ValueError as e:
        print(f"\n✗ Erro: {e}")


def entrada_estoque(cadastro: CadastroInsumo):
    """Registra entrada de estoque"""
    try:
        id = int(input("\nDigite o ID do insumo: "))
        insumo = cadastro.buscar_por_id(id)
        
        if not insumo:
            print(f"\n✗ Insumo com ID {id} não encontrado")
            return
        
        print(f"\nInsumo: {insumo.nome}")
        print(f"Estoque atual: {insumo.quantidade_estoque} {insumo.unidade}")
        
        quantidade = ler_float(f"Quantidade a adicionar ({insumo.unidade}): ")
        
        sucesso, mensagem = cadastro.movimentar_estoque(id, quantidade, 'entrada')
        print(f"\n{'✓' if sucesso else '✗'} {mensagem}")
        
    except ValueError:
        print("\n✗ ID inválido!")


def saida_estoque(cadastro: CadastroInsumo):
    """Registra saída de estoque"""
    try:
        id = int(input("\nDigite o ID do insumo: "))
        insumo = cadastro.buscar_por_id(id)
        
        if not insumo:
            print(f"\n✗ Insumo com ID {id} não encontrado")
            return
        
        print(f"\nInsumo: {insumo.nome}")
        print(f"Estoque atual: {insumo.quantidade_estoque} {insumo.unidade}")
        
        quantidade = ler_float(f"Quantidade a retirar ({insumo.unidade}): ")
        
        sucesso, mensagem = cadastro.movimentar_estoque(id, quantidade, 'saida')
        print(f"\n{'✓' if sucesso else '✗'} {mensagem}")
        
    except ValueError:
        print("\n✗ ID inválido!")


def relatorio_estoque_baixo(cadastro: CadastroInsumo):
    """Exibe relatório de estoque baixo"""
    try:
        limite = ler_float("\nDefinir limite de estoque baixo: ")
        insumos = cadastro.relatorio_estoque_baixo(limite)
        
        if not insumos:
            print(f"\n✓ Nenhum insumo com estoque abaixo de {limite}")
            return
        
        print(f"\n--- INSUMOS COM ESTOQUE BAIXO ({len(insumos)}) ---")
        for insumo in insumos:
            print(f"\n[ID: {insumo.id}] ⚠️")
            print(f"  {insumo.nome}: {insumo.quantidade_estoque} {insumo.unidade}")
            print(f"  Fornecedor: {insumo.fornecedor}")
    
    except ValueError as e:
        print(f"\n✗ Erro: {e}")


def valor_total_estoque(cadastro: CadastroInsumo):
    """Exibe valor total em estoque"""
    valor = cadastro.valor_total_estoque()
    print(f"\n{'='*50}")
    print(f"VALOR TOTAL EM ESTOQUE: R$ {valor:,.2f}")
    print(f"{'='*50}")


def remover_insumo(cadastro: CadastroInsumo):
    """Remove um insumo"""
    try:
        id = int(input("\nDigite o ID do insumo a remover: "))
        insumo = cadastro.buscar_por_id(id)
        
        if not insumo:
            print(f"\n✗ Insumo com ID {id} não encontrado")
            return
        
        print(f"\nInsumo: {insumo.nome}")
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
    cadastro = CadastroInsumo()
    
    while True:
        menu()
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            cadastrar_insumo(cadastro)
        elif opcao == '2':
            listar_insumos(cadastro)
        elif opcao == '3':
            buscar_por_id(cadastro)
        elif opcao == '4':
            buscar_por_nome(cadastro)
        elif opcao == '5':
            atualizar_insumo(cadastro)
        elif opcao == '6':
            entrada_estoque(cadastro)
        elif opcao == '7':
            saida_estoque(cadastro)
        elif opcao == '8':
            relatorio_estoque_baixo(cadastro)
        elif opcao == '9':
            valor_total_estoque(cadastro)
        elif opcao == '10':
            remover_insumo(cadastro)
        elif opcao == '0':
            print("\nEncerrando sistema...")
            break
        else:
            print("\n✗ Opção inválida!")
        
        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()
