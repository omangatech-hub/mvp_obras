"""
Script para popular o banco de dados com dados de exemplo
Execute este script para ter dados de teste no sistema
"""
from datetime import datetime, timedelta
from cadastro_obra.cadastro import CadastroObra
from cadastro_obra.obra import Obra
from cadastro_insumo.cadastro import CadastroInsumo
from cadastro_insumo.insumo import Insumo
from cadastro_funcionario.cadastro import CadastroFuncionario
from cadastro_funcionario.funcionario import Funcionario


def popular_obras():
    """Adiciona obras de exemplo"""
    print("\n📋 Populando obras...")
    cadastro = CadastroObra("obras.json")
    
    obras_exemplo = [
        Obra(
            nome="Edifício Residencial Vila Nova",
            inicio=datetime(2025, 1, 15),
            termino_previsto=datetime(2026, 6, 30),
            custo_estimado=2500000.00
        ),
        Obra(
            nome="Shopping Center Norte",
            inicio=datetime(2024, 8, 1),
            termino_previsto=datetime(2025, 12, 31),
            custo_estimado=8500000.00,
            termino_real=datetime(2025, 11, 15),
            custo_real=8750000.00
        ),
        Obra(
            nome="Ponte sobre Rio Verde",
            inicio=datetime(2025, 3, 1),
            termino_previsto=datetime(2025, 11, 30),
            custo_estimado=1200000.00
        ),
    ]
    
    for obra in obras_exemplo:
        sucesso, msg = cadastro.adicionar(obra)
        if sucesso:
            print(f"  ✓ {obra.nome}")
        else:
            print(f"  ✗ {obra.nome}: {msg}")


def popular_insumos():
    """Adiciona insumos de exemplo"""
    print("\n📦 Populando insumos...")
    cadastro = CadastroInsumo("insumos.json")
    
    insumos_exemplo = [
        Insumo(nome="Cimento CP-II", unidade="kg", quantidade_estoque=5000, preco_unitario=0.85, fornecedor="Cimentos Brasil Ltda"),
        Insumo(nome="Areia Média", unidade="m³", quantidade_estoque=120, preco_unitario=85.00, fornecedor="Areias São Paulo"),
        Insumo(nome="Brita 1", unidade="m³", quantidade_estoque=80, preco_unitario=95.00, fornecedor="Pedreira Central"),
        Insumo(nome="Ferro 10mm", unidade="kg", quantidade_estoque=3500, preco_unitario=5.50, fornecedor="Aço & Ferro SA"),
        Insumo(nome="Tijolo Cerâmico", unidade="un", quantidade_estoque=8000, preco_unitario=1.20, fornecedor="Cerâmica Vermelha"),
        Insumo(nome="Tinta Acrílica Branca", unidade="L", quantidade_estoque=250, preco_unitario=45.00, fornecedor="Tintas Master"),
        Insumo(nome="Piso Cerâmico 45x45", unidade="m²", quantidade_estoque=450, preco_unitario=32.00, fornecedor="Cerâmica Premium"),
        Insumo(nome="Tubos PVC 100mm", unidade="m", quantidade_estoque=5, preco_unitario=18.50, fornecedor="Tubos & Conexões"),
    ]
    
    for insumo in insumos_exemplo:
        sucesso, msg = cadastro.adicionar(insumo)
        if sucesso:
            print(f"  ✓ {insumo.nome}")
        else:
            print(f"  ✗ {insumo.nome}: {msg}")


def popular_funcionarios():
    """Adiciona funcionários de exemplo"""
    print("\n👷 Populando funcionários...")
    cadastro = CadastroFuncionario("funcionarios.json")
    
    funcionarios_exemplo = [
        Funcionario(nome="João Silva Santos", cpf="12345678901", cargo="Engenheiro Civil", salario=8500.00, data_admissao=datetime(2023, 1, 10)),
        Funcionario(nome="Maria Oliveira Costa", cpf="98765432109", cargo="Mestre de Obras", salario=4500.00, data_admissao=datetime(2022, 5, 15)),
        Funcionario(nome="Pedro Souza Lima", cpf="11122233344", cargo="Pedreiro", salario=3200.00, data_admissao=datetime(2024, 3, 20)),
        Funcionario(nome="Ana Paula Ferreira", cpf="55566677788", cargo="Arquiteta", salario=7500.00, data_admissao=datetime(2023, 8, 1)),
        Funcionario(nome="Carlos Eduardo Alves", cpf="99988877766", cargo="Eletricista", salario=3500.00, data_admissao=datetime(2024, 1, 15)),
        Funcionario(nome="Juliana Mendes Rocha", cpf="44433322211", cargo="Encanador", salario=3000.00, data_admissao=datetime(2023, 11, 5), data_demissao=datetime(2025, 10, 30)),
        Funcionario(nome="Roberto Carlos Dias", cpf="66677788899", cargo="Servente", salario=2200.00, data_admissao=datetime(2024, 6, 1)),
        Funcionario(nome="Fernanda Lima Santos", cpf="33344455566", cargo="Auxiliar Administrativo", salario=2800.00, data_admissao=datetime(2024, 2, 10)),
    ]
    
    for funcionario in funcionarios_exemplo:
        sucesso, msg = cadastro.adicionar(funcionario)
        if sucesso:
            print(f"  ✓ {funcionario.nome}")
        else:
            print(f"  ✗ {funcionario.nome}: {msg}")


def main():
    """Executa a população do banco de dados"""
    print("="*60)
    print(" " * 10 + "POPULAR BANCO DE DADOS COM EXEMPLOS")
    print("="*60)
    
    resposta = input("\n⚠️  Isso irá adicionar dados de exemplo. Continuar? (S/N): ").strip().upper()
    
    if resposta != 'S':
        print("\n❌ Operação cancelada.")
        return
    
    try:
        popular_obras()
        popular_insumos()
        popular_funcionarios()
        
        print("\n" + "="*60)
        print(" " * 15 + "✅ DADOS POPULADOS COM SUCESSO!")
        print("="*60)
        print("\nAgora você pode executar o sistema com:")
        print("  python main.py")
        print("\nOu usar os scripts de atalho:")
        print("  PowerShell: .\\run.ps1")
        print("  CMD: run.bat")
        
    except Exception as e:
        print(f"\n❌ Erro ao popular dados: {e}")


if __name__ == "__main__":
    main()
