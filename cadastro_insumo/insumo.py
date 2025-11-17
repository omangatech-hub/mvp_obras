from dataclasses import dataclass, asdict
from typing import Optional
import json


@dataclass
class Insumo:
    """Classe para representar um insumo"""
    nome: str
    unidade: str  # kg, m, m², m³, un, L, etc.
    classificacao: str = ""
    codigo: str = ""
    quantidade_estoque: float = 0.0
    preco_unitario: float = 0.0
    fornecedor: str = ""
    id: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Converte o insumo para dicionário"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Insumo':
        """Cria um insumo a partir de um dicionário"""
        return cls(**data)
    
    def validar(self) -> list[str]:
        """Valida os dados do insumo e retorna lista de erros"""
        erros = []
        
        if not self.nome or len(self.nome.strip()) == 0:
            erros.append("Nome do insumo é obrigatório")
        
        if not self.unidade or len(self.unidade.strip()) == 0:
            erros.append("Unidade de medida é obrigatória")
        
        # Campos opcionais: classificacao, codigo, quantidade_estoque, preco_unitario, fornecedor
        
        return erros
    
    def calcular_valor_estoque(self) -> float:
        """Calcula o valor total do estoque"""
        return self.quantidade_estoque * self.preco_unitario
    
    def adicionar_estoque(self, quantidade: float) -> bool:
        """Adiciona quantidade ao estoque"""
        if quantidade <= 0:
            return False
        self.quantidade_estoque += quantidade
        return True
    
    def remover_estoque(self, quantidade: float) -> bool:
        """Remove quantidade do estoque"""
        if quantidade <= 0 or quantidade > self.quantidade_estoque:
            return False
        self.quantidade_estoque -= quantidade
        return True
    
    def __str__(self) -> str:
        """Representação em string do insumo"""
        valor_total = self.calcular_valor_estoque()
        return (f"Insumo: {self.nome}\n"
                f"  Unidade: {self.unidade}\n"
                f"  Quantidade em Estoque: {self.quantidade_estoque:,.2f} {self.unidade}\n"
                f"  Preço Unitário: R$ {self.preco_unitario:,.2f}\n"
                f"  Valor Total em Estoque: R$ {valor_total:,.2f}\n"
                f"  Fornecedor: {self.fornecedor}")
