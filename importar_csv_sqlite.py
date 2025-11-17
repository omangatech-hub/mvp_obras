"""
Script para importar insumos do CSV para o banco de dados SQLite
"""
import csv
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cadastro_insumo.database import DatabaseInsumos


def importar_csv_para_sqlite():
    """Importa insumos do arquivo CSV para o SQLite"""
    db = DatabaseInsumos("insumos.db")
    
    # Limpar tabela antes de importar
    print("Limpando tabela de insumos...")
    db.limpar_tabela()
    
    # Ler o CSV e importar os dados
    print("Importando insumos do CSV para SQLite...")
    total = 0
    erros = 0
    
    with open('insumos.csv', 'r', encoding='utf-8') as arquivo:
        # Criar leitor CSV com delimitador ;
        leitor = csv.DictReader(arquivo, delimiter=';')
        
        batch = []
        for linha in leitor:
            try:
                # Extrair dados da linha
                classificacao = linha.get('Classificação', '').strip()
                codigo = linha.get('Código do Insumo', '').strip()
                descricao = linha.get('Descrição do Insumo', '').strip()
                unidade = linha.get('Unidade', '').strip()
                
                # Pular linhas vazias
                if not descricao:
                    continue
                
                # Truncar descrição se muito longo (limite de 500 caracteres)
                if len(descricao) > 500:
                    descricao = descricao[:497] + "..."
                
                # Inserir no banco
                db.inserir(
                    codigo=codigo,
                    classificacao=classificacao,
                    nome=descricao,
                    unidade=unidade if unidade else "UN",
                    preco_unitario=0.0,
                    fornecedor="",
                    quantidade_estoque=0.0
                )
                
                total += 1
                if total % 500 == 0:
                    print(f"  Importados {total} insumos...")
                    
            except Exception as e:
                erros += 1
                print(f"  Erro ao importar linha: {e}")
                continue
    
    print(f"\n✅ Importação concluída!")
    print(f"  Total importado: {total}")
    print(f"  Erros: {erros}")
    print(f"  Banco de dados: insumos.db")
    
    # Verificar total no banco
    total_db = db.contar_total()
    print(f"  Registros no banco: {total_db}")


if __name__ == "__main__":
    importar_csv_para_sqlite()
