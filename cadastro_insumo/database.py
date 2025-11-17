"""
Módulo de gerenciamento do banco de dados SQLite para insumos
"""
import sqlite3
from typing import Optional, List
from pathlib import Path


class DatabaseInsumos:
    """Gerenciador do banco de dados SQLite para insumos"""
    
    def __init__(self, db_path: str = "insumos.db"):
        self.db_path = db_path
        self.criar_tabela()
    
    def conectar(self) -> sqlite3.Connection:
        """Cria conexão com o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
        return conn
    
    def criar_tabela(self):
        """Cria a tabela de insumos se não existir"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS insumos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT,
                classificacao TEXT,
                nome TEXT NOT NULL,
                unidade TEXT NOT NULL,
                preco_unitario REAL DEFAULT 0.0,
                fornecedor TEXT DEFAULT '',
                quantidade_estoque REAL DEFAULT 0.0
            )
        """)
        
        # Criar índices para melhor performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_codigo ON insumos(codigo)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_classificacao ON insumos(classificacao)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_nome ON insumos(nome)")
        
        conn.commit()
        conn.close()
    
    def inserir(self, codigo: str, classificacao: str, nome: str, unidade: str, 
                preco_unitario: float = 0.0, fornecedor: str = "", 
                quantidade_estoque: float = 0.0) -> int:
        """Insere um novo insumo e retorna o ID"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO insumos (codigo, classificacao, nome, unidade, preco_unitario, fornecedor, quantidade_estoque)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (codigo, classificacao, nome, unidade, preco_unitario, fornecedor, quantidade_estoque))
        
        insumo_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return insumo_id
    
    def buscar_por_id(self, insumo_id: int) -> Optional[dict]:
        """Busca um insumo por ID"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM insumos WHERE id = ?", (insumo_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def listar_todos(self, limit: int = None, offset: int = 0) -> List[dict]:
        """Lista todos os insumos com paginação opcional"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        if limit:
            cursor.execute("SELECT * FROM insumos ORDER BY id LIMIT ? OFFSET ?", (limit, offset))
        else:
            cursor.execute("SELECT * FROM insumos ORDER BY id")
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def contar_total(self) -> int:
        """Conta o total de insumos"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM insumos")
        total = cursor.fetchone()['total']
        
        conn.close()
        return total
    
    def buscar(self, texto: str, limit: int = 100) -> List[dict]:
        """Busca insumos por texto (código, classificação ou nome)"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        texto_busca = f"%{texto}%"
        cursor.execute("""
            SELECT * FROM insumos 
            WHERE codigo LIKE ? OR classificacao LIKE ? OR nome LIKE ?
            ORDER BY id
            LIMIT ?
        """, (texto_busca, texto_busca, texto_busca, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def atualizar(self, insumo_id: int, codigo: str, classificacao: str, nome: str, 
                  unidade: str, preco_unitario: float, fornecedor: str, 
                  quantidade_estoque: float) -> bool:
        """Atualiza um insumo existente"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE insumos 
            SET codigo = ?, classificacao = ?, nome = ?, unidade = ?, 
                preco_unitario = ?, fornecedor = ?, quantidade_estoque = ?
            WHERE id = ?
        """, (codigo, classificacao, nome, unidade, preco_unitario, fornecedor, 
              quantidade_estoque, insumo_id))
        
        linhas_afetadas = cursor.rowcount
        conn.commit()
        conn.close()
        
        return linhas_afetadas > 0
    
    def excluir(self, insumo_id: int) -> bool:
        """Exclui um insumo"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM insumos WHERE id = ?", (insumo_id,))
        
        linhas_afetadas = cursor.rowcount
        conn.commit()
        conn.close()
        
        return linhas_afetadas > 0
    
    def limpar_tabela(self):
        """Remove todos os registros (use com cuidado!)"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM insumos")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='insumos'")
        
        conn.commit()
        conn.close()
