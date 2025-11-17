"""
Sistema Integrado de Gestão de Obras
Gerencia obras, insumos e funcionários
"""
import sys
import os

# Adiciona os diretórios dos módulos ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cadastro_obra'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cadastro_insumo'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cadastro_funcionario'))

from cadastro_obra.cadastro import CadastroObra
from cadastro_insumo.cadastro import CadastroInsumo
from cadastro_funcionario.cadastro import CadastroFuncionario


def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_principal():
    """Exibe o menu principal do sistema"""
    print("\n" + "="*60)
    print(" " * 15 + "SISTEMA DE GESTÃO DE OBRAS")
    print("="*60)
    print("1. 🏗️  Gerenciar Obras")
    print("2. 📦 Gerenciar Insumos")
    print("3. 👷 Gerenciar Funcionários")
    print("4. 📊 Relatórios Gerais")
    print("5. ℹ️  Sobre o Sistema")
    print("0. 🚪 Sair")
    print("="*60)


def menu_obras():
    """Exibe o menu de obras"""
    print("\n" + "="*60)
    print(" " * 20 + "GERENCIAR OBRAS")
    print("="*60)
    print("1. Cadastrar nova obra")
    print("2. Listar todas as obras")
    print("3. Buscar obra")
    print("4. Atualizar obra")
    print("5. Finalizar obra")
    print("6. Remover obra")
    print("0. Voltar ao menu principal")
    print("="*60)


def menu_insumos():
    """Exibe o menu de insumos"""
    print("\n" + "="*60)
    print(" " * 20 + "GERENCIAR INSUMOS")
    print("="*60)
    print("1. Cadastrar novo insumo")
    print("2. Listar todos os insumos")
    print("3. Buscar insumo")
    print("4. Atualizar insumo")
    print("5. Entrada de estoque")
    print("6. Saída de estoque")
    print("7. Relatório de estoque baixo")
    print("8. Remover insumo")
    print("0. Voltar ao menu principal")
    print("="*60)


def menu_funcionarios():
    """Exibe o menu de funcionários"""
    print("\n" + "="*60)
    print(" " * 18 + "GERENCIAR FUNCIONÁRIOS")
    print("="*60)
    print("1. Cadastrar novo funcionário")
    print("2. Listar todos os funcionários")
    print("3. Listar apenas ativos")
    print("4. Buscar funcionário")
    print("5. Atualizar funcionário")
    print("6. Demitir funcionário")
    print("7. Folha de pagamento")
    print("8. Relatório por cargo")
    print("9. Remover funcionário")
    print("0. Voltar ao menu principal")
    print("="*60)


def pausar():
    """Pausa a execução aguardando Enter"""
    input("\n⏸️  Pressione Enter para continuar...")


def gerenciar_obras(cadastro_obra):
    """Submenu para gerenciar obras"""
    from cadastro_obra import main_obra
    
    while True:
        menu_obras()
        opcao = input("\n👉 Escolha uma opção: ").strip()
        
        if opcao == '1':
            main_obra.cadastrar_obra(cadastro_obra)
            pausar()
        elif opcao == '2':
            main_obra.listar_obras(cadastro_obra)
            pausar()
        elif opcao == '3':
            print("\n--- BUSCAR OBRA ---")
            print("1. Por ID")
            print("2. Por nome")
            sub = input("Escolha: ").strip()
            if sub == '1':
                main_obra.buscar_por_id(cadastro_obra)
            elif sub == '2':
                main_obra.buscar_por_nome(cadastro_obra)
            pausar()
        elif opcao == '4':
            main_obra.atualizar_obra(cadastro_obra)
            pausar()
        elif opcao == '5':
            main_obra.finalizar_obra(cadastro_obra)
            pausar()
        elif opcao == '6':
            main_obra.remover_obra(cadastro_obra)
            pausar()
        elif opcao == '0':
            break
        else:
            print("\n❌ Opção inválida!")
            pausar()


def gerenciar_insumos(cadastro_insumo):
    """Submenu para gerenciar insumos"""
    from cadastro_insumo import main_insumo
    
    while True:
        menu_insumos()
        opcao = input("\n👉 Escolha uma opção: ").strip()
        
        if opcao == '1':
            main_insumo.cadastrar_insumo(cadastro_insumo)
            pausar()
        elif opcao == '2':
            main_insumo.listar_insumos(cadastro_insumo)
            pausar()
        elif opcao == '3':
            print("\n--- BUSCAR INSUMO ---")
            print("1. Por ID")
            print("2. Por nome")
            sub = input("Escolha: ").strip()
            if sub == '1':
                main_insumo.buscar_por_id(cadastro_insumo)
            elif sub == '2':
                main_insumo.buscar_por_nome(cadastro_insumo)
            pausar()
        elif opcao == '4':
            main_insumo.atualizar_insumo(cadastro_insumo)
            pausar()
        elif opcao == '5':
            main_insumo.entrada_estoque(cadastro_insumo)
            pausar()
        elif opcao == '6':
            main_insumo.saida_estoque(cadastro_insumo)
            pausar()
        elif opcao == '7':
            main_insumo.relatorio_estoque_baixo(cadastro_insumo)
            pausar()
        elif opcao == '8':
            main_insumo.remover_insumo(cadastro_insumo)
            pausar()
        elif opcao == '0':
            break
        else:
            print("\n❌ Opção inválida!")
            pausar()


def gerenciar_funcionarios(cadastro_funcionario):
    """Submenu para gerenciar funcionários"""
    from cadastro_funcionario import main_funcionario
    
    while True:
        menu_funcionarios()
        opcao = input("\n👉 Escolha uma opção: ").strip()
        
        if opcao == '1':
            main_funcionario.cadastrar_funcionario(cadastro_funcionario)
            pausar()
        elif opcao == '2':
            main_funcionario.listar_funcionarios(cadastro_funcionario, False)
            pausar()
        elif opcao == '3':
            main_funcionario.listar_funcionarios(cadastro_funcionario, True)
            pausar()
        elif opcao == '4':
            print("\n--- BUSCAR FUNCIONÁRIO ---")
            print("1. Por ID")
            print("2. Por CPF")
            print("3. Por nome")
            print("4. Por cargo")
            sub = input("Escolha: ").strip()
            if sub == '1':
                main_funcionario.buscar_por_id(cadastro_funcionario)
            elif sub == '2':
                main_funcionario.buscar_por_cpf(cadastro_funcionario)
            elif sub == '3':
                main_funcionario.buscar_por_nome(cadastro_funcionario)
            elif sub == '4':
                main_funcionario.buscar_por_cargo(cadastro_funcionario)
            pausar()
        elif opcao == '5':
            main_funcionario.atualizar_funcionario(cadastro_funcionario)
            pausar()
        elif opcao == '6':
            main_funcionario.demitir_funcionario(cadastro_funcionario)
            pausar()
        elif opcao == '7':
            main_funcionario.folha_pagamento(cadastro_funcionario)
            pausar()
        elif opcao == '8':
            main_funcionario.relatorio_por_cargo(cadastro_funcionario)
            pausar()
        elif opcao == '9':
            main_funcionario.remover_funcionario(cadastro_funcionario)
            pausar()
        elif opcao == '0':
            break
        else:
            print("\n❌ Opção inválida!")
            pausar()


def relatorios_gerais(cadastro_obra, cadastro_insumo, cadastro_funcionario):
    """Exibe relatórios gerais consolidados"""
    print("\n" + "="*60)
    print(" " * 18 + "RELATÓRIO GERAL DO SISTEMA")
    print("="*60)
    
    # Obras
    obras = cadastro_obra.listar()
    obras_ativas = [o for o in obras if o.termino_real is None]
    obras_finalizadas = [o for o in obras if o.termino_real is not None]
    custo_total_estimado = sum(o.custo_estimado for o in obras)
    custo_total_real = sum(o.custo_real for o in obras if o.custo_real)
    
    print("\n📊 OBRAS:")
    print(f"  Total: {len(obras)}")
    print(f"  Em andamento: {len(obras_ativas)}")
    print(f"  Finalizadas: {len(obras_finalizadas)}")
    print(f"  Custo estimado total: R$ {custo_total_estimado:,.2f}")
    if custo_total_real > 0:
        print(f"  Custo real total: R$ {custo_total_real:,.2f}")
    
    # Insumos
    insumos = cadastro_insumo.listar()
    valor_estoque = cadastro_insumo.valor_total_estoque()
    estoque_baixo = cadastro_insumo.relatorio_estoque_baixo(10)
    
    print("\n📦 INSUMOS:")
    print(f"  Total cadastrados: {len(insumos)}")
    print(f"  Valor total em estoque: R$ {valor_estoque:,.2f}")
    print(f"  Itens com estoque baixo (<10): {len(estoque_baixo)}")
    
    # Funcionários
    funcionarios = cadastro_funcionario.listar()
    funcionarios_ativos = cadastro_funcionario.listar(apenas_ativos=True)
    folha = cadastro_funcionario.folha_pagamento(True)
    
    print("\n👷 FUNCIONÁRIOS:")
    print(f"  Total: {len(funcionarios)}")
    print(f"  Ativos: {len(funcionarios_ativos)}")
    print(f"  Inativos: {len(funcionarios) - len(funcionarios_ativos)}")
    print(f"  Folha de pagamento mensal: R$ {folha:,.2f}")
    if len(funcionarios_ativos) > 0:
        print(f"  Salário médio: R$ {folha / len(funcionarios_ativos):,.2f}")
    
    print("\n" + "="*60)


def sobre_sistema():
    """Exibe informações sobre o sistema"""
    print("\n" + "="*60)
    print(" " * 18 + "SOBRE O SISTEMA")
    print("="*60)
    print("""
📋 SISTEMA DE GESTÃO DE OBRAS v1.0

Desenvolvido para gerenciar de forma integrada:
  • Obras (planejamento, custos, prazos)
  • Insumos (estoque, fornecedores, valores)
  • Funcionários (cadastro, folha, cargos)

🔧 FUNCIONALIDADES PRINCIPAIS:
  ✅ CRUD completo para todas as entidades
  ✅ Validações de dados
  ✅ Persistência em JSON
  ✅ Relatórios consolidados
  ✅ Controle de estoque
  ✅ Gestão de pessoal
  ✅ Acompanhamento financeiro

📁 ESTRUTURA DE ARQUIVOS:
  • cadastro_obra/ - Módulo de obras
  • cadastro_insumo/ - Módulo de insumos
  • cadastro_funcionario/ - Módulo de funcionários
  • *.json - Arquivos de dados

💾 Os dados são salvos automaticamente em arquivos JSON
   na raiz do projeto.
    """)
    print("="*60)


def main():
    """Função principal do sistema integrado"""
    # Inicializa os cadastros
    cadastro_obra = CadastroObra("obras.json")
    cadastro_insumo = CadastroInsumo("insumos.json")
    cadastro_funcionario = CadastroFuncionario("funcionarios.json")
    
    print("\n" + "="*60)
    print(" " * 10 + "🏗️  SISTEMA DE GESTÃO DE OBRAS  🏗️")
    print("="*60)
    print("\n✨ Sistema inicializado com sucesso!")
    
    while True:
        menu_principal()
        opcao = input("\n👉 Escolha uma opção: ").strip()
        
        if opcao == '1':
            gerenciar_obras(cadastro_obra)
        elif opcao == '2':
            gerenciar_insumos(cadastro_insumo)
        elif opcao == '3':
            gerenciar_funcionarios(cadastro_funcionario)
        elif opcao == '4':
            relatorios_gerais(cadastro_obra, cadastro_insumo, cadastro_funcionario)
            pausar()
        elif opcao == '5':
            sobre_sistema()
            pausar()
        elif opcao == '0':
            print("\n" + "="*60)
            print(" " * 15 + "👋 Encerrando sistema...")
            print(" " * 10 + "Obrigado por usar o sistema!")
            print("="*60 + "\n")
            break
        else:
            print("\n❌ Opção inválida!")
            pausar()


if __name__ == "__main__":
    main()
