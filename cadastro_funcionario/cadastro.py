import json
import os
from datetime import datetime
from typing import List, Optional
from .funcionario import Funcionario


class CadastroFuncionario:
    """Gerenciador de cadastro de funcionários"""
    
    def __init__(self, arquivo: str = "funcionarios.json"):
        self.arquivo = arquivo
        self.funcionarios: List[Funcionario] = []
        self.proximo_id = 1
        self.carregar()
    
    def carregar(self):
        """Carrega funcionários do arquivo JSON"""
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.funcionarios = [Funcionario.from_dict(func) for func in dados.get('funcionarios', [])]
                    self.proximo_id = dados.get('proximo_id', 1)
            except Exception as e:
                print(f"Erro ao carregar funcionários: {e}")
                self.funcionarios = []
                self.proximo_id = 1
    
    def salvar(self):
        """Salva funcionários no arquivo JSON"""
        try:
            dados = {
                'funcionarios': [func.to_dict() for func in self.funcionarios],
                'proximo_id': self.proximo_id
            }
            with open(self.arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar funcionários: {e}")
            return False
    
    def adicionar(self, funcionario: Funcionario) -> tuple[bool, str]:
        """Adiciona um novo funcionário"""
        erros = funcionario.validar()
        if erros:
            return False, '\n'.join(erros)
        
        # Verifica se CPF já existe
        if self.buscar_por_cpf(funcionario.cpf):
            return False, f"CPF {funcionario.formatar_cpf()} já cadastrado"
        
        funcionario.id = self.proximo_id
        self.proximo_id += 1
        self.funcionarios.append(funcionario)
        
        if self.salvar():
            return True, f"Funcionário '{funcionario.nome}' cadastrado com sucesso! ID: {funcionario.id}"
        else:
            return False, "Erro ao salvar o funcionário"
    
    def listar(self, apenas_ativos: bool = False) -> List[Funcionario]:
        """Lista todos os funcionários ou apenas ativos"""
        if apenas_ativos:
            return [f for f in self.funcionarios if f.esta_ativo()]
        return self.funcionarios
    
    def buscar_por_id(self, id: int) -> Optional[Funcionario]:
        """Busca um funcionário por ID"""
        for funcionario in self.funcionarios:
            if funcionario.id == id:
                return funcionario
        return None
    
    def buscar_por_cpf(self, cpf: str) -> Optional[Funcionario]:
        """Busca um funcionário por CPF"""
        import re
        cpf_limpo = re.sub(r'[^0-9]', '', cpf)
        for funcionario in self.funcionarios:
            func_cpf_limpo = re.sub(r'[^0-9]', '', funcionario.cpf)
            if func_cpf_limpo == cpf_limpo:
                return funcionario
        return None
    
    def buscar_por_nome(self, nome: str) -> List[Funcionario]:
        """Busca funcionários por nome (busca parcial)"""
        nome_lower = nome.lower()
        return [func for func in self.funcionarios if nome_lower in func.nome.lower()]
    
    def buscar_por_cargo(self, cargo: str) -> List[Funcionario]:
        """Busca funcionários por cargo"""
        cargo_lower = cargo.lower()
        return [func for func in self.funcionarios if cargo_lower in func.cargo.lower()]
    
    def atualizar(self, id: int, funcionario_atualizado: Funcionario) -> tuple[bool, str]:
        """Atualiza um funcionário existente"""
        funcionario = self.buscar_por_id(id)
        if not funcionario:
            return False, f"Funcionário com ID {id} não encontrado"
        
        erros = funcionario_atualizado.validar()
        if erros:
            return False, '\n'.join(erros)
        
        # Verifica se o CPF não está sendo usado por outro funcionário
        func_cpf = self.buscar_por_cpf(funcionario_atualizado.cpf)
        if func_cpf and func_cpf.id != id:
            return False, f"CPF {funcionario_atualizado.formatar_cpf()} já cadastrado para outro funcionário"
        
        funcionario_atualizado.id = id
        index = self.funcionarios.index(funcionario)
        self.funcionarios[index] = funcionario_atualizado
        
        if self.salvar():
            return True, f"Funcionário '{funcionario_atualizado.nome}' atualizado com sucesso!"
        else:
            return False, "Erro ao salvar o funcionário"
    
    def remover(self, id: int) -> tuple[bool, str]:
        """Remove um funcionário"""
        funcionario = self.buscar_por_id(id)
        if not funcionario:
            return False, f"Funcionário com ID {id} não encontrado"
        
        self.funcionarios.remove(funcionario)
        if self.salvar():
            return True, f"Funcionário '{funcionario.nome}' removido com sucesso!"
        else:
            return False, "Erro ao salvar as alterações"
    
    def demitir(self, id: int, data_demissao: datetime) -> tuple[bool, str]:
        """Registra demissão de um funcionário"""
        funcionario = self.buscar_por_id(id)
        if not funcionario:
            return False, f"Funcionário com ID {id} não encontrado"
        
        if not funcionario.esta_ativo():
            return False, f"Funcionário '{funcionario.nome}' já foi demitido"
        
        funcionario.data_demissao = data_demissao
        
        erros = funcionario.validar()
        if erros:
            funcionario.data_demissao = None
            return False, '\n'.join(erros)
        
        if self.salvar():
            return True, f"Demissão de '{funcionario.nome}' registrada com sucesso!"
        else:
            return False, "Erro ao salvar"
    
    def folha_pagamento(self, apenas_ativos: bool = True) -> float:
        """Calcula o total da folha de pagamento"""
        funcionarios = self.listar(apenas_ativos)
        return sum(func.salario for func in funcionarios)
    
    def relatorio_por_cargo(self) -> dict:
        """Retorna relatório agrupado por cargo"""
        relatorio = {}
        for func in self.funcionarios:
            if func.cargo not in relatorio:
                relatorio[func.cargo] = {
                    'quantidade': 0,
                    'ativos': 0,
                    'total_salarios': 0.0
                }
            
            relatorio[func.cargo]['quantidade'] += 1
            relatorio[func.cargo]['total_salarios'] += func.salario
            if func.esta_ativo():
                relatorio[func.cargo]['ativos'] += 1
        
        return relatorio
