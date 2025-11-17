from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
import json
import os


@dataclass
class Obra:
    """Classe para representar uma obra"""
    nome: str
    inicio: datetime
    termino_previsto: datetime
    custo_estimado: float
    termino_real: Optional[datetime] = None
    custo_real: Optional[float] = None
    id: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Converte a obra para dicionário"""
        data = asdict(self)
        data['inicio'] = self.inicio.isoformat()
        data['termino_previsto'] = self.termino_previsto.isoformat()
        if self.termino_real:
            data['termino_real'] = self.termino_real.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Obra':
        """Cria uma obra a partir de um dicionário"""
        data['inicio'] = datetime.fromisoformat(data['inicio'])
        data['termino_previsto'] = datetime.fromisoformat(data['termino_previsto'])
        if data.get('termino_real'):
            data['termino_real'] = datetime.fromisoformat(data['termino_real'])
        return cls(**data)
    
    def validar(self) -> list[str]:
        """Valida os dados da obra e retorna lista de erros"""
        erros = []
        
        if not self.nome or len(self.nome.strip()) == 0:
            erros.append("Nome da obra é obrigatório")
        
        if self.termino_previsto <= self.inicio:
            erros.append("Término previsto deve ser posterior ao início")
        
        if self.custo_estimado <= 0:
            erros.append("Custo estimado deve ser maior que zero")
        
        if self.termino_real and self.termino_real < self.inicio:
            erros.append("Término real não pode ser anterior ao início")
        
        if self.custo_real is not None and self.custo_real < 0:
            erros.append("Custo real não pode ser negativo")
        
        return erros
    
    def __str__(self) -> str:
        """Representação em string da obra"""
        termino = self.termino_real.strftime('%d/%m/%Y') if self.termino_real else 'Em andamento'
        custo = f'R$ {self.custo_real:,.2f}' if self.custo_real else 'N/A'
        
        return (f"Obra: {self.nome}\n"
                f"  Início: {self.inicio.strftime('%d/%m/%Y')}\n"
                f"  Término Previsto: {self.termino_previsto.strftime('%d/%m/%Y')}\n"
                f"  Término Real: {termino}\n"
                f"  Custo Estimado: R$ {self.custo_estimado:,.2f}\n"
                f"  Custo Real: {custo}")
