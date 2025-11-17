from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
import re


@dataclass
class Funcionario:
    """Classe para representar um funcionário"""
    nome: str
    cpf: str
    cargo: str
    salario: float
    data_admissao: datetime
    data_demissao: Optional[datetime] = None
    id: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Converte o funcionário para dicionário"""
        data = asdict(self)
        data['data_admissao'] = self.data_admissao.isoformat()
        if self.data_demissao:
            data['data_demissao'] = self.data_demissao.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Funcionario':
        """Cria um funcionário a partir de um dicionário"""
        data['data_admissao'] = datetime.fromisoformat(data['data_admissao'])
        if data.get('data_demissao'):
            data['data_demissao'] = datetime.fromisoformat(data['data_demissao'])
        return cls(**data)
    
    @staticmethod
    def validar_cpf(cpf: str) -> bool:
        """Valida formato de CPF"""
        # Remove caracteres não numéricos
        cpf = re.sub(r'[^0-9]', '', cpf)
        
        if len(cpf) != 11:
            return False
        
        # Verifica se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return False
        
        # Validação dos dígitos verificadores
        def calcular_digito(cpf_parcial, peso_inicial):
            soma = sum(int(cpf_parcial[i]) * (peso_inicial - i) for i in range(len(cpf_parcial)))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto
        
        digito1 = calcular_digito(cpf[:9], 10)
        digito2 = calcular_digito(cpf[:10], 11)
        
        return cpf[-2:] == f"{digito1}{digito2}"
    
    def validar(self) -> list[str]:
        """Valida os dados do funcionário e retorna lista de erros"""
        erros = []
        
        if not self.nome or len(self.nome.strip()) == 0:
            erros.append("Nome do funcionário é obrigatório")
        
        if not self.validar_cpf(self.cpf):
            erros.append("CPF inválido")
        
        if not self.cargo or len(self.cargo.strip()) == 0:
            erros.append("Cargo é obrigatório")
        
        if self.salario <= 0:
            erros.append("Salário deve ser maior que zero")
        
        if self.data_demissao and self.data_demissao < self.data_admissao:
            erros.append("Data de demissão não pode ser anterior à admissão")
        
        return erros
    
    def esta_ativo(self) -> bool:
        """Verifica se o funcionário está ativo"""
        return self.data_demissao is None
    
    def tempo_empresa(self) -> int:
        """Retorna tempo de empresa em dias"""
        data_final = self.data_demissao if self.data_demissao else datetime.now()
        return (data_final - self.data_admissao).days
    
    def formatar_cpf(self) -> str:
        """Retorna CPF formatado"""
        cpf_limpo = re.sub(r'[^0-9]', '', self.cpf)
        return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    
    def __str__(self) -> str:
        """Representação em string do funcionário"""
        status = "Ativo" if self.esta_ativo() else f"Demitido em {self.data_demissao.strftime('%d/%m/%Y')}"
        tempo = self.tempo_empresa()
        anos = tempo // 365
        meses = (tempo % 365) // 30
        
        return (f"Funcionário: {self.nome}\n"
                f"  CPF: {self.formatar_cpf()}\n"
                f"  Cargo: {self.cargo}\n"
                f"  Salário: R$ {self.salario:,.2f}\n"
                f"  Admissão: {self.data_admissao.strftime('%d/%m/%Y')}\n"
                f"  Status: {status}\n"
                f"  Tempo de empresa: {anos} ano(s) e {meses} mês(es)")
