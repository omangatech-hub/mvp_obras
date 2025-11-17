import json
import os
from datetime import datetime
from typing import List, Optional
from .obra import Obra


class CadastroObra:
    """Gerenciador de cadastro de obras"""
    
    def __init__(self, arquivo: str = "obras.json"):
        self.arquivo = arquivo
        self.obras: List[Obra] = []
        self.proximo_id = 1
        self.carregar()
    
    def carregar(self):
        """Carrega obras do arquivo JSON"""
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.obras = [Obra.from_dict(obra) for obra in dados.get('obras', [])]
                    self.proximo_id = dados.get('proximo_id', 1)
            except Exception as e:
                print(f"Erro ao carregar obras: {e}")
                self.obras = []
                self.proximo_id = 1
    
    def salvar(self):
        """Salva obras no arquivo JSON"""
        try:
            dados = {
                'obras': [obra.to_dict() for obra in self.obras],
                'proximo_id': self.proximo_id
            }
            with open(self.arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar obras: {e}")
            return False
    
    def adicionar(self, obra: Obra) -> tuple[bool, str]:
        """Adiciona uma nova obra"""
        erros = obra.validar()
        if erros:
            return False, '\n'.join(erros)
        
        obra.id = self.proximo_id
        self.proximo_id += 1
        self.obras.append(obra)
        
        if self.salvar():
            return True, f"Obra '{obra.nome}' cadastrada com sucesso! ID: {obra.id}"
        else:
            return False, "Erro ao salvar a obra"
    
    def listar(self) -> List[Obra]:
        """Lista todas as obras"""
        return self.obras
    
    def buscar_por_id(self, id: int) -> Optional[Obra]:
        """Busca uma obra por ID"""
        for obra in self.obras:
            if obra.id == id:
                return obra
        return None
    
    def buscar_por_nome(self, nome: str) -> List[Obra]:
        """Busca obras por nome (busca parcial)"""
        nome_lower = nome.lower()
        return [obra for obra in self.obras if nome_lower in obra.nome.lower()]
    
    def atualizar(self, id: int, obra_atualizada: Obra) -> tuple[bool, str]:
        """Atualiza uma obra existente"""
        obra = self.buscar_por_id(id)
        if not obra:
            return False, f"Obra com ID {id} não encontrada"
        
        erros = obra_atualizada.validar()
        if erros:
            return False, '\n'.join(erros)
        
        obra_atualizada.id = id
        index = self.obras.index(obra)
        self.obras[index] = obra_atualizada
        
        if self.salvar():
            return True, f"Obra '{obra_atualizada.nome}' atualizada com sucesso!"
        else:
            return False, "Erro ao salvar a obra"
    
    def remover(self, id: int) -> tuple[bool, str]:
        """Remove uma obra"""
        obra = self.buscar_por_id(id)
        if not obra:
            return False, f"Obra com ID {id} não encontrada"
        
        self.obras.remove(obra)
        if self.salvar():
            return True, f"Obra '{obra.nome}' removida com sucesso!"
        else:
            return False, "Erro ao salvar as alterações"
    
    def finalizar_obra(self, id: int, termino_real: datetime, custo_real: float) -> tuple[bool, str]:
        """Finaliza uma obra, registrando término real e custo real"""
        obra = self.buscar_por_id(id)
        if not obra:
            return False, f"Obra com ID {id} não encontrada"
        
        if obra.termino_real:
            return False, f"Obra '{obra.nome}' já foi finalizada"
        
        obra.termino_real = termino_real
        obra.custo_real = custo_real
        
        erros = obra.validar()
        if erros:
            obra.termino_real = None
            obra.custo_real = None
            return False, '\n'.join(erros)
        
        if self.salvar():
            return True, f"Obra '{obra.nome}' finalizada com sucesso!"
        else:
            return False, "Erro ao salvar a obra"
