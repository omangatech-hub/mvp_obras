"""
Script para importar insumos do CSV para o banco de dados
"""
import csv
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cadastro_insumo.cadastro import CadastroInsumo
from cadastro_insumo.insumo import Insumo


def importar_insumos_csv():
    """Importa insumos do arquivo CSV para o sistema"""
    cadastro = CadastroInsumo("insumos.json")
    
    # Limpar lista de insumos antes de importar
    print("Limpando lista de insumos...")
    cadastro.insumos = []
    cadastro.proximo_id = 1
    
    # Ler o CSV e importar os dados
    print("Importando insumos do CSV...")
    total = 0
    erros = 0
    
    with open('insumos.csv', 'r', encoding='utf-8') as arquivo:
        # Criar leitor CSV com delimitador ;
        leitor = csv.DictReader(arquivo, delimiter=';')
        
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
                
                # Truncar descrição se muito longo (limite de 200 caracteres)
                if len(descricao) > 200:
                    descricao = descricao[:197] + "..."
                
                # Criar insumo com campos separados
                insumo = Insumo(
                    nome=descricao,
                    unidade=unidade if unidade else "UN",
                    classificacao=classificacao,
                    codigo=codigo
                )
                
                # Adicionar ao cadastro
                sucesso, mensagem = cadastro.adicionar(insumo)
                if sucesso:
                    total += 1
                    if total % 100 == 0:
                        print(f"  Importados {total} insumos...")
                else:
                    erros += 1
                    print(f"  Erro ao importar: {mensagem}")
                    
            except Exception as e:
                erros += 1
                print(f"  Erro ao processar linha: {e}")
                continue
    
    # Salvar todos os insumos no arquivo JSON
    print("\nSalvando insumos no arquivo...")
    if cadastro.salvar():
        print(f"\nImportação concluída!")
        print(f"  Total importado: {total}")
        print(f"  Erros: {erros}")
        print(f"\nInsumos cadastrados com sucesso!")
    else:
        print("\nErro ao salvar insumos no arquivo!")


if __name__ == "__main__":
    importar_insumos_csv()
