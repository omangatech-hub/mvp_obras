from typing import List, Optional, Tuple
from .insumo import Insumo
from .database import DatabaseInsumos


class CadastroInsumo:
    """Gerenciador de cadastro de insumos usando SQLite"""
    
    def __init__(self, arquivo: str = "insumos.db"):
        self.db = DatabaseInsumos(arquivo)
    
    def adicionar(self, insumo: Insumo) -> tuple[bool, str]:
        """Adiciona um novo insumo"""
        erros = insumo.validar()
        if erros:
            return False, '\n'.join(erros)
        
        try:
            novo_id = self.db.inserir(
                codigo=insumo.codigo,
                classificacao=insumo.classificacao,
                nome=insumo.nome,
                unidade=insumo.unidade,
                preco_unitario=insumo.preco_unitario,
                fornecedor=insumo.fornecedor,
                quantidade_estoque=insumo.quantidade_estoque
            )
            return True, f"Insumo '{insumo.nome}' cadastrado com sucesso! ID: {novo_id}"
        except Exception as e:
            return False, f"Erro ao salvar o insumo: {e}"
    
    def listar(self, limit: Optional[int] = None, offset: int = 0) -> List[Insumo]:
        """Lista insumos com paginação opcional"""
        dados = self.db.listar_todos(limit=limit, offset=offset)
        return [Insumo.from_dict(d) for d in dados]
    
    def contar_total(self) -> int:
        """Conta o total de insumos cadastrados"""
        return self.db.contar_total()
    
    def buscar_por_id(self, id: int) -> Optional[Insumo]:
        """Busca um insumo por ID"""
        dados = self.db.buscar_por_id(id)
        if dados:
            return Insumo.from_dict(dados)
        return None
    
    def buscar_por_nome(self, nome: str) -> List[Insumo]:
        """Busca insumos por nome (busca parcial)"""
        dados = self.db.buscar(nome)
        return [Insumo.from_dict(d) for d in dados]
    
    def atualizar(self, id: int, insumo_atualizado: Insumo) -> tuple[bool, str]:
        """Atualiza um insumo existente"""
        insumo = self.buscar_por_id(id)
        if not insumo:
            return False, f"Insumo com ID {id} não encontrado"
        
        erros = insumo_atualizado.validar()
        if erros:
            return False, '\n'.join(erros)
        
        try:
            self.db.atualizar(
                insumo_id=id,
                codigo=insumo_atualizado.codigo,
                classificacao=insumo_atualizado.classificacao,
                nome=insumo_atualizado.nome,
                unidade=insumo_atualizado.unidade,
                preco_unitario=insumo_atualizado.preco_unitario,
                fornecedor=insumo_atualizado.fornecedor,
                quantidade_estoque=insumo_atualizado.quantidade_estoque
            )
            return True, f"Insumo '{insumo_atualizado.nome}' atualizado com sucesso!"
        except Exception as e:
            return False, f"Erro ao atualizar o insumo: {e}"
    
    def remover(self, id: int) -> tuple[bool, str]:
        """Remove um insumo"""
        insumo = self.buscar_por_id(id)
        if not insumo:
            return False, f"Insumo com ID {id} não encontrado"
        
        try:
            self.db.excluir(id)
            return True, f"Insumo '{insumo.nome}' removido com sucesso!"
        except Exception as e:
            return False, f"Erro ao remover o insumo: {e}"
    
    def movimentar_estoque(self, id: int, quantidade: float, tipo: str) -> tuple[bool, str]:
        """Adiciona ou remove quantidade do estoque"""
        insumo = self.buscar_por_id(id)
        if not insumo:
            return False, f"Insumo com ID {id} não encontrado"
        
        if tipo.lower() == 'entrada':
            if insumo.adicionar_estoque(quantidade):
                sucesso, msg = self.atualizar(id, insumo)
                if sucesso:
                    return True, f"Entrada de {quantidade} {insumo.unidade} registrada. Estoque atual: {insumo.quantidade_estoque}"
                else:
                    return False, "Erro ao salvar"
            else:
                return False, "Quantidade inválida para entrada"
        
        elif tipo.lower() == 'saida':
            if insumo.remover_estoque(quantidade):
                sucesso, msg = self.atualizar(id, insumo)
                if sucesso:
                    return True, f"Saída de {quantidade} {insumo.unidade} registrada. Estoque atual: {insumo.quantidade_estoque}"
                else:
                    return False, "Erro ao salvar"
            else:
                return False, f"Quantidade inválida ou insuficiente (estoque: {insumo.quantidade_estoque})"
        
        else:
            return False, "Tipo deve ser 'entrada' ou 'saida'"
    
    def relatorio_estoque_baixo(self, limite: float = 10.0) -> List[Insumo]:
        """Retorna insumos com estoque abaixo do limite"""
        todos = self.listar()
        return [insumo for insumo in todos if insumo.quantidade_estoque < limite]
    
    def valor_total_estoque(self) -> float:
        """Calcula o valor total de todos os insumos em estoque"""
        todos = self.listar()
        return sum(insumo.calcular_valor_estoque() for insumo in todos)
