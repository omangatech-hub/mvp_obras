"""
Página de Gerenciamento de Insumos
"""
import flet as ft
from cadastro_insumo.insumo import Insumo


class PaginaInsumos:
    def __init__(self, page: ft.Page, cadastro_insumo, app=None):
        self.page = page
        self.cadastro = cadastro_insumo
        self.app = app
        self.dialog_aberto = None
        self.insumo_selecionado = None
        
        # Paginação
        self.pagina_atual = 0
        self.itens_por_pagina = 50
        self.termo_busca = ""
        
        # Campos do formulário
        self.txt_codigo = ft.TextField(label="Código", width=200)
        self.txt_classificacao = ft.TextField(label="Classificação (MATERIAL, SERVIÇOS, etc)", width=400)
        self.txt_nome = ft.TextField(label="Descrição do Insumo", width=400)
        self.txt_unidade = ft.TextField(label="Unidade (kg, m, m², L, UN)", width=200)
        self.txt_preco = ft.TextField(label="Preço Unitário (R$) - Opcional", width=200, keyboard_type=ft.KeyboardType.NUMBER, value="0")
        self.txt_fornecedor = ft.TextField(label="Fornecedor - Opcional", width=400)
    
    def criar_pagina(self):
        """Cria a página principal de insumos"""
        total = self.cadastro.contar_total()
        self.tabela_insumos = self.criar_tabela_insumos()
        self.txt_busca = ft.TextField(
            label="🔍 Buscar insumo (código, classificação ou descrição)",
            width=400,
            on_change=self.on_busca_change,
        )
        self.lbl_paginacao = self.criar_label_paginacao()
        
        return ft.Column(
            [
                # Cabeçalho
                ft.Row(
                    [
                        ft.Text("📦 Gerenciamento de Insumos", size=32, weight=ft.FontWeight.BOLD),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "➕ Novo Insumo",
                            on_click=self.abrir_dialog_cadastro,
                            bgcolor=ft.Colors.GREEN_700,
                            color=ft.Colors.WHITE,
                        ),
                    ],
                ),
                ft.Divider(height=20),
                
                # Cards de resumo
                ft.Row(
                    [
                        self.criar_card_resumo(
                            "Total de Insumos",
                            str(total),
                            ft.Icons.INVENTORY_2,
                            ft.Colors.GREEN_400,
                        ),
                    ],
                    spacing=15,
                ),
                ft.Container(height=20),
                
                # Barra de busca
                ft.Row([self.txt_busca]),
                ft.Container(height=10),
                
                # Tabela
                ft.Container(
                    content=self.tabela_insumos,
                    expand=True,
                ),
                
                # Controles de paginação
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            tooltip="Página anterior",
                            on_click=self.pagina_anterior,
                        ),
                        self.lbl_paginacao,
                        ft.IconButton(
                            icon=ft.Icons.ARROW_FORWARD,
                            tooltip="Próxima página",
                            on_click=self.proxima_pagina,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )
    
    def criar_card_resumo(self, titulo, valor, icone, cor):
        """Cria card de resumo"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icone, size=40, color=cor),
                    ft.Column(
                        [
                            ft.Text(valor, size=22, weight=ft.FontWeight.BOLD, color=cor),
                            ft.Text(titulo, size=14, color=ft.Colors.GREY_700),
                        ],
                        spacing=0,
                    ),
                ],
                spacing=15,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=15,
            width=280,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
        )
    
    def criar_tabela_insumos(self):
        """Cria a tabela de insumos"""
        # Buscar ou listar com paginação
        if self.termo_busca:
            insumos = self.cadastro.buscar_por_nome(self.termo_busca)
        else:
            offset = self.pagina_atual * self.itens_por_pagina
            insumos = self.cadastro.listar(limit=self.itens_por_pagina, offset=offset)
        
        linhas = []
        for insumo in insumos:
            linhas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(insumo.id))),
                        ft.DataCell(ft.Text(insumo.codigo if hasattr(insumo, 'codigo') else "")),
                        ft.DataCell(ft.Text(insumo.classificacao if hasattr(insumo, 'classificacao') else "")),
                        ft.DataCell(ft.Text(insumo.nome[:50] + "..." if len(insumo.nome) > 50 else insumo.nome)),
                        ft.DataCell(ft.Text(insumo.unidade)),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        icon_color=ft.Colors.BLUE_700,
                                        tooltip="Editar",
                                        on_click=lambda e, i=insumo: self.abrir_dialog_edicao(i),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        icon_color=ft.Colors.RED_700,
                                        tooltip="Excluir",
                                        on_click=lambda e, i=insumo: self.confirmar_exclusao(i),
                                    ),
                                ],
                                spacing=0,
                            )
                        ),
                    ],
                )
            )
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Código", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Classificação", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Descrição", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Unidade", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Ações", weight=ft.FontWeight.BOLD)),
            ],
            rows=linhas,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_200),
        )
    
    def abrir_dialog_cadastro(self, e):
        """Abre dialog para cadastrar novo insumo"""
        self.limpar_formulario()
        
        dialog = ft.AlertDialog(
            title=ft.Text("➕ Cadastrar Novo Insumo"),
            content=ft.Container(
                content=ft.Column(
                    [
                        self.txt_nome,
                        ft.Row([self.txt_unidade, self.txt_preco]),
                        self.txt_fornecedor,
                    ],
                    tight=True,
                ),
                width=600,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.fechar_dialog),
                ft.ElevatedButton("Salvar", on_click=self.salvar_insumo, bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.dialog_aberto = dialog
        self.page.update()
    
    def abrir_dialog_edicao(self, insumo):
        """Abre dialog para editar insumo"""
        self.insumo_selecionado = insumo
        self.txt_codigo.value = insumo.codigo if hasattr(insumo, 'codigo') else ""
        self.txt_classificacao.value = insumo.classificacao if hasattr(insumo, 'classificacao') else ""
        self.txt_nome.value = insumo.nome
        self.txt_unidade.value = insumo.unidade
        self.txt_preco.value = str(insumo.preco_unitario if hasattr(insumo, 'preco_unitario') else 0)
        self.txt_fornecedor.value = insumo.fornecedor if hasattr(insumo, 'fornecedor') else ""
        
        dialog = ft.AlertDialog(
            title=ft.Text("✏️ Editar Insumo"),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row([self.txt_codigo, self.txt_unidade]),
                        self.txt_classificacao,
                        self.txt_nome,
                        ft.Row([self.txt_preco, self.txt_fornecedor]),
                    ],
                    tight=True,
                ),
                width=600,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.fechar_dialog),
                ft.ElevatedButton("Atualizar", on_click=self.atualizar_insumo, bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.dialog_aberto = dialog
        self.page.update()
    
    def salvar_insumo(self, e):
        """Salva novo insumo"""
        try:
            preco = float(self.txt_preco.value.replace(",", ".")) if self.txt_preco.value else 0.0
            
            insumo = Insumo(
                nome=self.txt_nome.value,
                unidade=self.txt_unidade.value,
                codigo=self.txt_codigo.value,
                classificacao=self.txt_classificacao.value,
                preco_unitario=preco,
                fornecedor=self.txt_fornecedor.value
            )
            
            sucesso, msg = self.cadastro.adicionar(insumo)
            
            if sucesso:
                self.mostrar_snackbar(msg, ft.Colors.GREEN_700)
                self.atualizar_tabela()
                self.fechar_dialog(e)
            else:
                self.mostrar_snackbar(msg, ft.Colors.RED_700)
                
        except ValueError as ex:
            self.mostrar_snackbar(f"Erro nos dados: {str(ex)}", ft.Colors.RED_700)
    
    def atualizar_insumo(self, e):
        """Atualiza insumo existente"""
        try:
            preco = float(self.txt_preco.value.replace(",", ".")) if self.txt_preco.value else 0.0
            
            insumo_atualizado = Insumo(
                nome=self.txt_nome.value,
                unidade=self.txt_unidade.value,
                codigo=self.txt_codigo.value,
                classificacao=self.txt_classificacao.value,
                preco_unitario=preco,
                fornecedor=self.txt_fornecedor.value,
                quantidade_estoque=self.insumo_selecionado.quantidade_estoque if hasattr(self.insumo_selecionado, 'quantidade_estoque') else 0.0
            )
            
            sucesso, msg = self.cadastro.atualizar(self.insumo_selecionado.id, insumo_atualizado)
            
            if sucesso:
                self.mostrar_snackbar(msg, ft.Colors.GREEN_700)
                self.atualizar_tabela()
                self.fechar_dialog(e)
            else:
                self.mostrar_snackbar(msg, ft.Colors.RED_700)
                
        except ValueError as ex:
            self.mostrar_snackbar(f"Erro nos dados: {str(ex)}", ft.Colors.RED_700)
    
    def confirmar_exclusao(self, insumo):
        """Confirma exclusão de insumo"""
        def excluir(e):
            sucesso, msg = self.cadastro.remover(insumo.id)
            if sucesso:
                self.mostrar_snackbar(msg, ft.Colors.GREEN_700)
                self.atualizar_tabela()
            else:
                self.mostrar_snackbar(msg, ft.Colors.RED_700)
            self.fechar_dialog(e)
        
        dialog = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar Exclusão"),
            content=ft.Text(f"Deseja realmente excluir o insumo '{insumo.nome}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=self.fechar_dialog),
                ft.ElevatedButton("Excluir", on_click=excluir, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.dialog_aberto = dialog
        self.page.update()
    
    def criar_label_paginacao(self):
        """Cria o label de paginação"""
        total = self.cadastro.contar_total()
        total_paginas = (total + self.itens_por_pagina - 1) // self.itens_por_pagina
        return ft.Text(
            f"Página {self.pagina_atual + 1} de {total_paginas} ({total} insumos no total)",
            size=14,
        )
    
    def on_busca_change(self, e):
        """Quando o texto de busca muda"""
        self.termo_busca = e.control.value
        self.pagina_atual = 0  # Volta para primeira página
        self.atualizar_tabela()
    
    def pagina_anterior(self, e):
        """Vai para a página anterior"""
        if self.pagina_atual > 0:
            self.pagina_atual -= 1
            self.atualizar_tabela()
    
    def proxima_pagina(self, e):
        """Vai para a próxima página"""
        total = self.cadastro.contar_total()
        total_paginas = (total + self.itens_por_pagina - 1) // self.itens_por_pagina
        if self.pagina_atual < total_paginas - 1:
            self.pagina_atual += 1
            self.atualizar_tabela()
    
    def limpar_formulario(self):
        """Limpa os campos do formulário"""
        self.txt_codigo.value = ""
        self.txt_classificacao.value = ""
        self.txt_nome.value = ""
        self.txt_unidade.value = ""
        self.txt_preco.value = "0"
        self.txt_fornecedor.value = ""
        self.insumo_selecionado = None
    
    def fechar_dialog(self, e):
        """Fecha o dialog aberto"""
        if self.dialog_aberto:
            self.dialog_aberto.open = False
            self.page.update()
    
    def mostrar_snackbar(self, mensagem, cor):
        """Mostra mensagem na tela"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(mensagem, color=ft.Colors.WHITE),
            bgcolor=cor,
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def atualizar_tabela(self):
        """Atualiza a tabela de insumos"""
        if self.app:
            # Recarrega a página inteira incluindo cards de resumo
            self.app.recarregar_pagina_atual()
        else:
            # Fallback: apenas atualiza a tabela
            self.tabela_insumos.rows = self.criar_tabela_insumos().rows
            self.page.update()
